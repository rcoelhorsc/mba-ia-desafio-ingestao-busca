# Sistema RAG (Retrieval-Augmented Generation) com Chat CLI

Este projeto implementa um sistema completo de Retrieval-Augmented Generation (RAG) que permite fazer perguntas sobre documentos PDF usando um chat interativo no terminal. O sistema vetoriza documentos, armazena em um banco vetorial PostgreSQL e responde perguntas baseadas exclusivamente no conteúdo dos documentos.

## 📋 Índice

- [Arquitetura do Projeto](#-arquitetura-do-projeto)
- [Tecnologias e Dependências](#-tecnologias-e-dependências)
- [Configuração do Ambiente](#-configuração-do-ambiente)
- [Configuração de APIs](#-configuração-de-apis)
- [Configuração do Docker](#-configuração-do-docker)
- [Variáveis de Ambiente](#-variáveis-de-ambiente)
- [Como Usar](#-como-usar)
- [Recursos do Chat](#-recursos-do-chat)
- [Configurações Avançadas](#-configurações-avançadas)
- [Resolução de Problemas](#-resolução-de-problemas)

## 🏗️ Arquitetura do Projeto

O sistema é composto por três componentes principais:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Ingestão      │    │  Banco Vetorial │    │      Chat       │
│   (ingest.py)   │───▶│   PostgreSQL    │◄───│   (chat.py)     │
│                 │    │   + pgvector    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  PDF Loader     │    │   Embeddings    │    │  Search Engine  │
│  Text Splitter  │    │   Vector Store  │    │  LLM Integration│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Fluxo de Dados

1. **Ingestão**: PDFs são carregados, divididos em chunks e vetorizados
2. **Armazenamento**: Embeddings são salvos no PostgreSQL com pgvector
3. **Consulta**: Perguntas são vetorizadas e buscam documentos similares
4. **Resposta**: LLM gera respostas baseadas apenas no contexto encontrado

## 🛠️ Tecnologias e Dependências

### Frameworks Principais
- **LangChain**: Framework para aplicações com LLM
- **LangChain Community**: Extensões e integrações
- **LangChain Text Splitters**: Divisão de documentos

### Modelos de LLM e Embeddings
- **Google Gemini**: Embeddings e modelos de linguagem
- **OpenAI**: GPT e embeddings da OpenAI
- **HuggingFace**: Embeddings locais (Sentence Transformers)

### Banco de Dados e Vetorial
- **PostgreSQL**: Banco de dados principal
- **pgvector**: Extensão para busca vetorial
- **psycopg**: Driver Python para PostgreSQL

### Processamento de Documentos
- **PyPDF**: Carregamento de arquivos PDF
- **Sentence Transformers**: Embeddings locais
- **torch**: Framework de deep learning

### Infraestrutura
- **Docker**: Containerização do PostgreSQL
- **python-dotenv**: Gerenciamento de variáveis de ambiente

## ⚙️ Configuração do Ambiente

### 1. Pré-requisitos
- Python 3.8 ou superior
- Docker e Docker Compose
- Git

### 2. Clone do Repositório
```bash
git clone <url-do-repositorio>
cd mba-ia-desafio-ingestao-busca
```

### 3. Ambiente Virtual
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 4. Instalação de Dependências
```bash
pip install -r requirements.txt
```

## 🔑 Configuração de APIs

### OpenAI API Key

1. **Acesse o site da OpenAI:**
   - [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)

2. **Faça login ou crie uma conta:**
   - Se já possui conta, faça login
   - Caso contrário, crie uma nova conta

3. **Crie uma nova API Key:**
   - Clique em "Create new secret key"
   - Dê um nome identificável para a chave
   - Clique em "Create secret key"

4. **Copie e armazene sua API Key:**
   - A chave será exibida apenas uma vez
   - Copie e adicione no arquivo `.env`

**Tutorial completo:** [Como Gerar uma API Key na OpenAI](https://hub.asimov.academy/tutorial/como-gerar-uma-api-key-na-openai/)

### Google Gemini API Key

1. **Acesse o Google AI Studio:**
   - [https://ai.google.dev/gemini-api/docs/api-key?hl=pt-BR](https://ai.google.dev/gemini-api/docs/api-key?hl=pt-BR)

2. **Faça login com sua conta Google:**
   - Use sua conta Google existente

3. **Crie uma nova API Key:**
   - Clique em "Create API Key" ou "Criar chave de API"
   - Dê um nome identificável
   - A chave será gerada e exibida

4. **Copie e armazene sua API Key:**
   - Copie a chave e adicione no arquivo `.env`

**Documentação oficial:** [Como usar chaves da API Gemini](https://ai.google.dev/gemini-api/docs/api-key?hl=pt-BR)

## 🐳 Configuração do Docker

### 1. Iniciar PostgreSQL com pgvector
```bash
# Subir o banco de dados
docker-compose up -d

# Verificar se está rodando
docker-compose ps
```

### 2. Configuração do docker-compose.yml
O arquivo já está configurado com:
- PostgreSQL 15 com extensão pgvector
- Porta 5432 exposta
- Volume persistente para dados
- Variáveis de ambiente pré-configuradas

### 3. Parar os serviços
```bash
# Parar serviços
docker-compose down

# Parar e remover volumes (ATENÇÃO: apaga dados)
docker-compose down -v
```

## 🔧 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes configurações:

### Configuração Básica
```env
# Banco de Dados PostgreSQL
DATABASE_URL=postgresql://langchain:langchain@localhost:5432/langchain
PG_VECTOR_COLLECTION_NAME=documents

# Arquivo PDF
PDF_PATH=document.pdf
```

### Configuração de Embeddings
```env
# Provedor de Embeddings: local, gemini, openai
EMBEDDING_PROVIDER=local

# Para embeddings locais (HuggingFace)
LOCAL_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Para Google Gemini
GOOGLE_API_KEY=sua_chave_api_google_aqui
GEMINI_EMBEDDING_MODEL=models/embedding-001

# Para OpenAI
OPENAI_API_KEY=sua_chave_api_openai_aqui
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

### Configuração de LLM
```env
# Provedor de LLM: gemini, openai
LLM_PROVIDER=gemini

# Modelos específicos
GEMINI_MODEL=gemini-1.5-flash
OPENAI_MODEL=gpt-3.5-turbo
```

## 🚀 Como Usar

### 1. Preparação do Ambiente
```bash
# 1. Ativar ambiente virtual
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac

# 2. Subir banco de dados
docker-compose up -d

# 3. Verificar se PDF existe
ls document.pdf
```

### 2. Ingestão de Documentos
```bash
cd src
python ingest.py
```

**O que acontece na ingestão:**
- ✅ Carrega o PDF especificado em `PDF_PATH`
- ✅ Divide o documento em chunks de 1000 caracteres com overlap de 150
- ✅ Gera embeddings para cada chunk usando o provedor configurado
- ✅ Armazena no PostgreSQL com pgvector
- ✅ Cria índices para busca eficiente

**Saída esperada:**
```
🏠 Usando Embeddings Locais (HuggingFace)
✅ 45 documentos inseridos com sucesso no vector store!
```

### 3. Iniciar Chat Interativo
```bash
cd src
python chat.py
```

## 🎯 Recursos do Chat

### Interface do Chat
```
🤖 CHAT RAG - Consulta Baseada em Documentos
================================================================================
Digite suas perguntas e eu responderei baseado no conteúdo dos documentos.
Comandos especiais:
  - 'sair' ou 'quit': encerra o chat
  - 'limpar' ou 'clear': limpa a tela
  - 'ajuda' ou 'help': mostra esta mensagem
--------------------------------------------------------------------------------
🔧 Inicializando sistema...
✅ Sistema inicializado com sucesso!

Digite 'ajuda' para ver os comandos disponíveis.

👤 Você: _
```

### Comandos Especiais
| Comando | Aliases | Descrição |
|---------|---------|-----------|
| `ajuda` | `help` | Mostra comandos disponíveis e dicas |
| `sair` | `quit`, `exit` | Encerra o chat |
| `limpar` | `clear` | Limpa a tela do terminal |

### Funcionalidades Técnicas
- ✅ **Busca Semântica**: Vetoriza pergunta e busca top 10 resultados
- ✅ **Contexto Relevante**: Concatena documentos encontrados
- ✅ **Prompt Rigoroso**: Template que evita alucinações
- ✅ **Respostas Controladas**: Baseadas exclusivamente no contexto
- ✅ **Tratamento de Erros**: Mensagens informativas para problemas
- ✅ **Interface Amigável**: Emojis e formatação clara


## ⚙️ Configurações Avançadas

### Provedores de Embeddings

#### 1. Embeddings Locais (Recomendado para Desenvolvimento)
```env
EMBEDDING_PROVIDER=local
LOCAL_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

**Vantagens:**
- ✅ Gratuito e sem limite de uso
- ✅ Funciona offline
- ✅ Boa qualidade para documentos em português/inglês
- ✅ Rápido após o primeiro carregamento

**Desvantagens:**
- ❌ Primeiro uso demora (download do modelo ~90MB)
- ❌ Usa CPU (mais lento que GPU)
- ❌ Ocupa espaço em disco

#### 2. Google Gemini Embeddings
```env
EMBEDDING_PROVIDER=gemini
GOOGLE_API_KEY=sua_chave_aqui
GEMINI_EMBEDDING_MODEL=models/embedding-001
```

**Vantagens:**
- ✅ Alta qualidade e otimizado para multilingual
- ✅ Rápido (processamento na nuvem)
- ✅ Sem uso de recursos locais

**Desvantagens:**
- ❌ Requer chave de API
- ❌ Custo por uso (verificar pricing)
- ❌ Requer conexão com internet

#### 3. OpenAI Embeddings
```env
EMBEDDING_PROVIDER=openai
OPENAI_API_KEY=sua_chave_aqui
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

**Vantagens:**
- ✅ Excelente qualidade
- ✅ Muito rápido
- ✅ Otimizado para RAG

**Desvantagens:**
- ❌ Requer chave de API
- ❌ Custo por token
- ❌ Requer conexão com internet

### Modelos de Embeddings Disponíveis

| Provedor | Modelo | Dimensões | Contexto | Observações |
|----------|--------|-----------|----------|-------------|
| Local | all-MiniLM-L6-v2 | 384 | 256 tokens | Recomendado para início |
| Local | all-mpnet-base-v2 | 768 | 384 tokens | Maior qualidade |
| Gemini | embedding-001 | 768 | 2048 tokens | Multilingual |
| OpenAI | text-embedding-3-small | 1536 | 8191 tokens | Custo/benefício |
| OpenAI | text-embedding-3-large | 3072 | 8191 tokens | Máxima qualidade |

### Configurações de Chunking

Para documentos muito grandes ou muito técnicos, você pode ajustar as configurações no `ingest.py`:

```python
splits = RecursiveCharacterTextSplitter(
    chunk_size=1500,        # Aumentar para documentos técnicos
    chunk_overlap=200,      # Mais overlap para melhor contexto
    add_start_index=False
).split_documents(docs)
```

### Configurações de Busca

Para ajustar a quantidade de documentos retornados, modifique em `search.py`:

```python
docs = vector_store.similarity_search(question, k=15)  # Mais contexto
```

## 🛠️ Resolução de Problemas

### Problema: Erro de Conexão com Banco
```
psycopg2.OperationalError: could not connect to server
```

**Solução:**
```bash
# Verificar se Docker está rodando
docker --version
docker-compose ps

# Reiniciar serviços
docker-compose down
docker-compose up -d

# Verificar logs
docker-compose logs postgres
```

### Problema: Módulo não encontrado
```
ModuleNotFoundError: No module named 'langchain_huggingface'
```

**Solução:**
```bash
# Ativar ambiente virtual
venv\Scripts\activate

# Reinstalar dependências
pip install -r requirements.txt
```

### Problema: Erro de API Key
```
Error: Invalid API key provided
```

**Solução:**
1. Verificar se `.env` existe e tem as chaves corretas
2. Verificar se chaves não expiraram
3. Verificar cotas/billing das APIs

### Problema: PDF não encontrado
```
FileNotFoundError: document.pdf not found
```

**Solução:**
```bash
# Verificar caminho do PDF no .env
PDF_PATH=./document.pdf

# Ou usar caminho absoluto
PDF_PATH=/caminho/completo/para/document.pdf
```

### Problema: Embeddings muito lentos (Local)
**Solução:**
```env
# Usar modelo menor
LOCAL_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Ou mudar para embeddings na nuvem
EMBEDDING_PROVIDER=gemini
```

### Problema: Respostas de baixa qualidade
**Soluções:**
1. **Melhorar chunking**: Aumentar `chunk_size` e `chunk_overlap`
2. **Mais contexto**: Aumentar `k` na busca vetorial
3. **Melhor embedding**: Usar OpenAI ou modelo local maior
4. **Melhor LLM**: Usar GPT-4 ou Gemini Pro

### Logs e Debug

Para debug avançado, adicione prints nos arquivos:

```python
# Em search.py, na função search_documents
print(f"Pergunta: {question}")
print(f"Documentos encontrados: {len(docs)}")
for i, doc in enumerate(docs):
    print(f"Doc {i}: {doc.page_content[:100]}...")
```

---

## 📞 Suporte

Para dúvidas ou problemas não cobertos neste guia:

1. Verifique os logs do Docker: `docker-compose logs`
2. Ative debug nos scripts Python
3. Consulte a documentação oficial do LangChain
4. Verifique status das APIs (OpenAI/Google)

---

**Nota de Segurança:** 🔒 Nunca compartilhe suas chaves de API publicamente. Mantenha o arquivo `.env` sempre no `.gitignore`.
