import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")

def ingest_pdf():
    docs = PyPDFLoader(str(PDF_PATH)).load()
    splits = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150, add_start_index=False).split_documents(docs)
    if not splits:
        raise SystemExit(0)
    
    # Gerar IDs para os documentos
    ids = [f"doc-{i}" for i in range(len(splits))]
    
    # Configurar embeddings - usar local por padrão
    embedding_provider = os.getenv("EMBEDDING_PROVIDER", "local")
    
    if embedding_provider == "gemini":
        embeddings = GoogleGenerativeAIEmbeddings(
            model=os.getenv("GEMINI_EMBEDDING_MODEL", "models/embedding-001"),
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        print("🔗 Usando Gemini Embeddings")
    elif embedding_provider == "openai":
        embeddings = OpenAIEmbeddings(
            model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
            api_key=os.getenv("OPENAI_API_KEY")
        )
        print("🔗 Usando OpenAI Embeddings")        
    else:
        # Usar embeddings locais (HuggingFace)
        embeddings = HuggingFaceEmbeddings(
            model_name=os.getenv("LOCAL_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"),
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        print("🏠 Usando Embeddings Locais (HuggingFace)")
    
    # Configurar o vector store
    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )
    
    # Adicionar documentos ao vector store
    store.add_documents(documents=splits, ids=ids)
    print(f"✅ {len(splits)} documentos inseridos com sucesso no vector store!")


if __name__ == "__main__":
    ingest_pdf()