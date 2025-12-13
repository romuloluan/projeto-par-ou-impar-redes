from servidor_oop import ServidorJogo
from cliente_oop import ClienteJogo


def menu_principal():
    while True:
        print("="*40)
        print("     PROJETO REDES: PAR OU ÍMPAR      ")
        print("="*40)
        print(" [1] - CRIAR SALA (SER SERVIDOR)")
        print(" [2] - ENTRAR EM SALA (SER CLIENTE)")
        print(" [3] - SAIR")
        print("="*40)
        
        opcao = input(" >> Escolha uma opção: ").strip()

        if opcao == "1":
            try:
                # Instancia e roda a lógica do Servidor
                print("\nIniciando Servidor...")
                jogo = ServidorJogo()
                jogo.iniciar()
                jogo.jogar()
                
                input("\nPartida finalizada. Pressione Enter para voltar ao menu...")
                # Fecha o socket do servidor explicitamente para liberar a porta
                jogo.server_socket.close() 
            except Exception as e:
                print(f"Erro no servidor: {e}")
                input("Pressione Enter...")

        elif opcao == "2":
            try:
                # Instancia e roda a lógica do Cliente
                print("\nIniciando Cliente...")
                c = ClienteJogo()
                c.conectar()
                c.jogar()
                
                input("\nPartida finalizada. Pressione Enter para voltar ao menu...")
            except Exception as e:
                # O próprio cliente trata erros de conexão, mas aqui pegamos erros gerais
                print(f"\nErro: {e}")
                input("Pressione Enter...")

        elif opcao == "3":
            print("Saindo do sistema...")
            break
        
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    menu_principal()