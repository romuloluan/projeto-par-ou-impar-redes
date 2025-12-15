import socket
import json

class ClienteJogo:
    def __init__(self):
        """
        Construtor da classe: Prepara o Socket do Cliente.
        """
        # CONFIGURAÇÃO DO SOCKET
        # socket.AF_INET  -> Família de endereços IPv4.
        # socket.SOCK_STREAM -> Protocolo TCP (Confiável, Orientado a Conexão).
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Porta onde vamos tentar bater na porta do servidor.
        # Deve ser EXATAMENTE a mesma porta configurada no servidor (50000).
        self.port = 50000

    def conectar(self, ip_alvo=None):
        """
        ESTABELECIMENTO DA CONEXÃO (Active Open).
        Tenta criar um túnel TCP com o Servidor no IP especificado.
        """
        
        # Definição do Host (Endereço IP)
        if ip_alvo:
            self.host = ip_alvo # IP vindo da interface gráfica
        else:
            self.host = 'localhost' # Fallback para testes locais

        try:
            print(f"Iniciando Handshake TCP com {self.host}:{self.port}...")
            
            # CONNECT:
            # Tenta realizar o 'Three-Way Handshake' do TCP (SYN -> SYN/ACK -> ACK).
            # Se o servidor não estiver rodando ou o IP estiver errado, isso lança um erro.
            self.client_socket.connect((self.host, self.port))
            
            print("Conexão TCP estabelecida com sucesso!")
            
        except Exception as e:
            print(f"Falha na conexão: {e}")
            # Lançamos o erro novamente para que a Interface Gráfica saiba que falhou
            # e mostre um aviso para o usuário.
            raise Exception("Não foi possível conectar ao servidor.")

    def enviar_jogada(self, dados):
        """
        ENVIO DE DADOS (Solicitação).
        Serializa o dicionário de dados e envia para o servidor.
        """
        try:
            # 1. SERIALIZAÇÃO (Marshalling):
            # Convertemos o Dicionário Python para uma String JSON.
            # Isso é necessário porque sockets só transportam bytes, não objetos complexos.
            mensagem_json = json.dumps(dados)
            
            # 2. SEND (Transmission):
            # Codificamos a string em bytes (UTF-8) e colocamos no buffer de saída da rede.
            self.client_socket.send(mensagem_json.encode())

            # 3. CONFIRMAÇÃO DE APLICAÇÃO (ACK):
            # O TCP garante a entrega dos pacotes, mas aqui implementamos um 'ACK de Aplicação'.
            # Ficamos esperando o servidor dizer "Recebi e entendi" (b'ack') antes de continuarmos.
            # Isso evita que o cliente tente ler a resposta final antes do servidor ter processado a jogada.
            try:
                confirmacao = self.client_socket.recv(1024)
                print(f"Confirmação do Servidor (ACK): {confirmacao.decode()}")
            except Exception as e:
                print(f"Alerta: Servidor não enviou confirmação: {e}")

        except Exception as e:
            print(f"Erro ao enviar pacote de jogada: {e}")

    def receber_resultado(self):
        """
        RECEBIMENTO DE DADOS (Resposta).
        Fica aguardando o Servidor processar o jogo e retornar o vencedor.
        """
        try:
            print("Aguardando pacote de resposta do servidor...")
            
            # RECV (Bloqueante):
            # O programa para aqui e fica escutando a porta até chegarem dados.
            # Buffer de 2048 bytes é suficiente para o JSON do resultado.
            resposta_bytes = self.client_socket.recv(2048) 
            
            # Se receber vazio, a conexão foi encerrada (FIN enviado pelo servidor).
            if not resposta_bytes:
                print("Conexão encerrada pelo host remoto.")
                return None
            
            # DESERIALIZAÇÃO:
            # Transforma os bytes recebidos de volta em um Dicionário Python útil.
            resposta_json = resposta_bytes.decode()
            dados_resultado = json.loads(resposta_json)
            
            return dados_resultado

        except json.JSONDecodeError:
            print("Erro de Protocolo: O servidor enviou dados corrompidos ou não-JSON.")
            return None
        except Exception as e:
            print(f"Erro de Rede ao receber resultado: {e}")
            return None