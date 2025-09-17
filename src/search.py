import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def get_embeddings():
    """Configura e retorna o modelo de embeddings baseado na configuração do ambiente"""
    embedding_provider = os.getenv("EMBEDDING_PROVIDER", "local")
    
    if embedding_provider == "gemini":
        return GoogleGenerativeAIEmbeddings(
            model=os.getenv("GEMINI_EMBEDDING_MODEL", "models/embedding-001"),
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
    elif embedding_provider == "openai":
        return OpenAIEmbeddings(
            model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
            api_key=os.getenv("OPENAI_API_KEY")
        )
    else:
        # Usar embeddings locais (HuggingFace)
        return HuggingFaceEmbeddings(
            model_name=os.getenv("LOCAL_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"),
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )

def get_llm():
    """Configura e retorna o modelo de LLM baseado na configuração do ambiente"""
    llm_provider = os.getenv("LLM_PROVIDER", "gemini")
    
    if llm_provider == "gemini":
        return ChatGoogleGenerativeAI(
            model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.1
        )
    elif llm_provider == "openai":
        return ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.1
        )
    else:
        raise ValueError(f"Provedor de LLM não suportado: {llm_provider}")

def get_vector_store():
    """Configura e retorna o vector store"""
    embeddings = get_embeddings()
    
    return PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )

def search_documents(question, k=10):
    """Busca documentos relevantes no banco vetorial"""
    try:
        vector_store = get_vector_store()
        docs = vector_store.similarity_search(question, k=k)
        return docs
    except Exception as e:
        print(f"Erro ao buscar documentos: {e}")
        return []

def format_context(docs):
    """Formata os documentos encontrados em um contexto concatenado"""
    if not docs:
        return "Nenhum contexto relevante encontrado."
    
    context_parts = []
    for i, doc in enumerate(docs, 1):
        context_parts.append(f"Documento {i}:\n{doc.page_content}")
    
    return "\n\n".join(context_parts)

def search_prompt():
    """Configura e retorna a chain de busca e resposta"""
    try:
        # Configurar componentes
        llm = get_llm()
        prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
        
        # Configurar chain
        def get_context_and_question(inputs):
            question = inputs["pergunta"]
            docs = search_documents(question, k=10)
            context = format_context(docs)
            return {"contexto": context, "pergunta": question}
        
        chain = (
            get_context_and_question
            | prompt
            | llm
        )
        
        return chain
        
    except Exception as e:
        print(f"Erro ao configurar a chain: {e}")
        return None