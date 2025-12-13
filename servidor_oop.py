import socket
from comuns import Jogador

class ServidorJogo:
    def __init__(self):

        #Configurações da Rede

        #"Seja um anfitrião (Host) em TODAS as interfaces de rede que este computador tiver."
        self.host=''

        #Define a porta no qual usaremos para o programa
        self.port=50000

        #AF_INET: Define que usaremos IP versão 4.  SOCK_STREAM: Define que usaremos TCP.
        self.server_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        
        # Permite reusar a porta imediatamente (evita erro ao reiniciar pelo menu)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Já faz o bind e o listen assim que cria o objeto

        #INFORMA AO COMPUTADOR QUE O QUE CHEGAR NESSA PORTA PERTENCE AO PROGRAMA
        self.server_socket.bind((self.host, self.port)) 

        #Diz ao servidor quantos clientes (usuários) podem ficar aguardando uma conexão.
        self.server_socket.listen(1)

        #AQUI CRIAMOS OS OBJETOS DO TIPO JOGADOR
        self.jogador1 = Jogador()
        self.jogador2 = Jogador()

        print(f"Servidor iniciado na porta {self.port}. Aguardando...")


    def iniciar(self):
        print("Aguardando Conexão...")
        #O método self.server_socket.accept() vai receber duas informações
        #1° o novo socket (onde a comunicação vai acontecer)
        #2° o endereço do cliente, quem se conectou (IP, PORTA) EX: ("10.13.134.1", 49523)
        self.socket_cliente, self.endereco_cliente = self.server_socket.accept()
        print(f"Conectado em {self.endereco_cliente}")

    def receber_jogada_jogador1 (self):
        print("Aguardando o Jogador 1 jogar!")

        # O .recv(1024) recebe os dados brutos enviados pelo jogador 1 --  O 1024 é o tamanho máximo do pacote (em bytes) que vamos ler de uma vez.
        # O decode() decodifica esses dados recebidos
        self.jogador1.nome = self.socket_cliente.recv(1024).decode() #armazena o nome do jogador1 (que se conectou)
        
        # Envia o ACK para confirmar recebimento e evitar colagem de pacotes
        self.socket_cliente.send("ACK".encode()) 

        #Recebe e armazena a opção escolhida (par ou impar)
        self.jogador1.escolha= self.socket_cliente.recv(1024).decode()

        # Envia o ACK para confirmar recebimento
        self.socket_cliente.send("ACK".encode()) 

        #Recebe o número escolhido pelo jogador1
        self.jogador1.numero = int(self.socket_cliente.recv(1024).decode())

    def realizar_jogada_jogador2(self):
        print("\n--- Sua Vez ---\n")
        print(f"Você está jogando contra {self.jogador1.nome}\n")
        self.jogador2.nome = input("Digite seu nome: ").strip().upper()
        
        # Envia o nome do servidor para o cliente saber contra quem joga
        self.socket_cliente.send(self.jogador2.nome.encode()) 

        # Define automaticamente se o JOGADOR2/servidor é Par ou Ímpar
        if self.jogador1.escolha == "P":
            self.jogador2.escolha = "I"
            print(f"Oponente escolheu PAR. Você ficou com IMPAR.")
        else:
            self.jogador2.escolha = "P"
            print(f"Oponente escolheu IMPAR. Você ficou com PAR.")

        self.jogador2.numero = int(input("Digite seu número (0-10): "))


        # --- Cálculo do Resultado ---
    def calcular_vencedor(self):
        total = self.jogador1.numero + self.jogador2.numero
        print(f"\nCalculando: {self.jogador1.numero} + {self.jogador2.numero} = {total}")

        if total % 2 == 0:
            resultado = "PAR"
            vencedor = self.jogador1.nome if self.jogador1.escolha == "P" else self.jogador2.nome
        else:
            resultado = "IMPAR"
            vencedor = self.jogador1.nome if self.jogador1.escolha == "I" else self.jogador2.nome
        
        # --- ATUALIZAÇÃO AQUI ---
        # Mensagem detalhada com o número do J2, a soma e o vencedor
        msg_final = (f"\n--- PLACAR ---\n"
                     f"Oponente jogou: {self.jogador2.numero}\n"
                     f"Soma: {total} ({resultado})\n"
                     f"VENCEDOR: {vencedor}")
        
        print(msg_final)
        self.socket_cliente.send(msg_final.encode())


    # Organiza a ordem das coisas
    def jogar(self):
        self.receber_jogada_jogador1()
        self.realizar_jogada_jogador2()
        self.calcular_vencedor()
        
        # Fecha o socket do cliente específico ao terminar a rodada
        self.socket_cliente.close()