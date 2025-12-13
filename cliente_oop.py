import socket
from comuns import Jogador

class ClienteJogo:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 50000
        self.jogador1 = Jogador() 

    def conectar(self):
        self.host = input("Digite o IP do Servidor (ex: 10.13... ou localhost): ").strip()
        # Se deixar em branco, assume localhost para facilitar testes
        if not self.host: 
            self.host = 'localhost'
            
        try:
            print(f"Tentando conectar a {self.host}...")
            self.client_socket.connect((self.host, self.port))
            print("Conectado com sucesso!")
        except:
            print("Erro ao conectar. Verifique se o IP está correto e o servidor ligado.")
            # [AJUSTE] Lança um erro para o MENU tratar, em vez de fechar o programa com exit()
            raise Exception("Falha na conexão")

    def jogar(self):
        print("\n--- Início do Jogo ---")
        
        # 1. Preenche os dados do objeto Jogador 1 (Cliente)
        self.jogador1.nome = input("Digite seu nome: ").strip().upper()
        self.jogador1.escolha = input("Escolha (P)ar ou (I)mpar: ").strip().upper()
        self.jogador1.numero = input("Digite seu número (0-10): ") 

        # 2. Envia os dados usando os atributos do objeto
        self.client_socket.send(self.jogador1.nome.encode())
        self.client_socket.recv(1024) # Aguarda ACK do nome

        self.client_socket.send(self.jogador1.escolha.encode())
        self.client_socket.recv(1024) # Aguarda ACK da escolha

        self.client_socket.send(self.jogador1.numero.encode())

        print("\nAguardando jogada do Servidor...")

        # 3. Recebe resposta
        nome_servidor = self.client_socket.recv(1024).decode()
        print(f"Você está jogando contra: {nome_servidor}")

        # Recebe a mensagem completa (com o número do oponente e resultado)
        resultado = self.client_socket.recv(1024).decode()
        
        print(resultado) 

        self.client_socket.close()