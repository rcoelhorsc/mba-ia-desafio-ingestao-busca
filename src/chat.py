import sys
from search import search_prompt

def print_welcome():
    """Exibe mensagem de boas-vindas do chat"""
    print("=" * 80)
    print("🤖 CHAT RAG - Consulta Baseada em Documentos")
    print("=" * 80)
    print("Digite suas perguntas e eu responderei baseado no conteúdo dos documentos.")
    print("Comandos especiais:")
    print("  - 'sair' ou 'quit': encerra o chat")
    print("  - 'limpar' ou 'clear': limpa a tela")
    print("  - 'ajuda' ou 'help': mostra esta mensagem")
    print("-" * 80)

def print_help():
    """Exibe mensagem de ajuda"""
    print("\n📋 AJUDA:")
    print("- Digite qualquer pergunta sobre o conteúdo dos documentos")
    print("- O sistema buscará as informações mais relevantes (top 10)")
    print("- A resposta será baseada exclusivamente no contexto encontrado")
    print("- Se a informação não estiver nos documentos, será informado")
    print("\n💡 Dicas:")
    print("- Seja específico em suas perguntas")
    print("- Use palavras-chave relacionadas ao conteúdo que você busca")
    print("- Evite perguntas muito genéricas ou fora do escopo dos documentos")

def clear_screen():
    """Limpa a tela do terminal"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def process_question(chain, question):
    """Processa uma pergunta usando a chain RAG"""
    try:
        print("\n🔍 Buscando informações relevantes...")
        
        # Invocar a chain com a pergunta
        response = chain.invoke({"pergunta": question})
        
        # Extrair o conteúdo da resposta
        if hasattr(response, 'content'):
            answer = response.content
        else:
            answer = str(response)
        
        return answer.strip()
        
    except Exception as e:
        return f"❌ Erro ao processar a pergunta: {str(e)}"

def main():
    """Função principal do chat"""
    print_welcome()
    
    # Inicializar a chain RAG
    print("🔧 Inicializando sistema...")
    chain = search_prompt()

    if not chain:
        print("❌ Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        print("Certifique-se de que:")
        print("- As variáveis de ambiente estão configuradas")
        print("- O banco de dados PostgreSQL está rodando") 
        print("- Os documentos foram ingeridos no banco vetorial")
        return
    
    print("✅ Sistema inicializado com sucesso!")
    print("\nDigite 'ajuda' para ver os comandos disponíveis.\n")
    
    # Loop principal do chat
    while True:
        try:
            # Obter entrada do usuário
            question = input("👤 Você: ").strip()
            
            # Verificar comandos especiais
            if question.lower() in ['sair', 'quit', 'exit']:
                print("\n👋 Obrigado por usar o chat! Até logo!")
                break
                
            elif question.lower() in ['limpar', 'clear']:
                clear_screen()
                print_welcome()
                continue
                
            elif question.lower() in ['ajuda', 'help']:
                print_help()
                continue
                
            elif not question:
                print("⚠️  Por favor, digite uma pergunta ou 'ajuda' para ver os comandos.")
                continue
            
            # Processar a pergunta
            print("\n🤖 Assistente: ", end="", flush=True)
            answer = process_question(chain, question)
            print(answer)
            print("-" * 80)
            
        except KeyboardInterrupt:
            print("\n\n👋 Chat interrompido pelo usuário. Até logo!")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            print("Digite 'ajuda' para ver os comandos disponíveis.")

if __name__ == "__main__":
    main()