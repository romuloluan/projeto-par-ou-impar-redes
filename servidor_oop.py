import socket

class ServidorJogo:
    def __init__(self):

        #Atributos
        self.host=''

        #Define a porta no qual usaremos para o programa
        self.port=50000

        #AF_INET: Define que usaremos IP versão 4.  SOCK_STREAM: Define que usaremos TCP.
        self.server_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

        # Já faz o bind e o listen assim que cria o objeto

        #INFORMA AO COMPUTADOR QUE O QUE CHEGAR NESSA PORTA PERTENCE AO PROGRAMA
        self.server_socket.bind((self.host, self.port)) 

        #Diz ao servidor quantos clientes (usuários) podem ficar aguardando uma conexão.
        self.server_socket.listen(1)

        print(f"Servidor iniciado na porta {self.port}. Aguardando...")


    def inicinar(self):
        print("Aguardando Conexão...")
        #O método self.server_socket.accept() vai receber duas informações
        #1° o novo socket (onde a comunicação vai acontecer)
        #2° o endereço do cliente, quem se conectou (IP, PORTA) EX: ("10.13.134.1", 49523)
        self.socket_cliente, self.endereco_cliente = self.server_socket.accept()
        print(f"Conectado em {self.endereco_cliente}")



    def jogar(self):
        # O .recv(1024) recebe os dados brutos enviados pelo jogador 1 --  O 1024 é o tamanho máximo do pacote (em bytes) que vamos ler de uma vez.
        # O decode() decodifica esses dados recebidos
        self.nome_jogador1= self.socket_cliente.recv(1024).decode() #armazena o nome do jogador1 (que se conectou)
        
        #Recebe e armazena a opção escolhida (par ou impar)
        self.opcao_jogador1= self.socket_cliente.recv(1024).decode()

        #Recebe o número escolhido pelo jogador1
        self.numero_jogador1 = int(self.socket_cliente.recv(1024).decode())

        # --- Parte do Servidor / JOGADOR 02---

        print("\n--- Sua Vez ---")

        print(f"Você está jogando contra {self.nome_jogador1}")
        self.nome_jogador2 = input("Digite seu nome: ").strip().upper()
        
        # Envia o nome do servidor para o cliente saber contra quem joga
        self.socket_cliente.send(self.nome_jogador2.encode()) 

        # Define automaticamente se o servidor é Par ou Ímpar
        if self.opcao_jogador1 == "P":
            self.opcao_jogador2 = "I"
            print(f"Oponente escolheu PAR. Você ficou com IMPAR.")
        else:
            self.opcao_jogador2 = "P"
            print(f"Oponente escolheu IMPAR. Você ficou com PAR.")

        self.numero_jogador2 = int(input("Digite seu número (0-10): "))
        
        # --- Cálculo do Resultado ---
        total = self.numero_jogador1 + self.numero_jogador2
        print(f"Calculando: {self.numero_jogador1} + {self.numero_jogador2} = {total}")

        # Verifica quem ganhou
        if total % 2 == 0:
            resultado = "PAR"
            # Se deu Par e o Jog1 escolheu Par, ele ganha. Senão, eu ganho.
            if self.opcao_jogador1 == "P":
                vencedor = self.nome_jogador1
            else:
                vencedor = self.nome_jogador2
        else:
            resultado = "IMPAR"
            if self.opcao_jogador1 == "I":
                vencedor = self.nome_jogador1
            else:
                vencedor = self.nome_jogador2
        


        # --- Finalização ---
        msg_final = f"Deu {resultado}. Vencedor: {vencedor}"
        print(msg_final)
        
        # Envia o veredito final para o cliente
        self.socket_cliente.send(msg_final.encode())




# Bloco principal para testar
if __name__ == "__main__":
    jogo = ServidorJogo() # Aqui ele chama o __init__
    jogo.inicinar() #Chama o método que vai receber os dados do outro jogador "cliente"
    jogo.jogar()
