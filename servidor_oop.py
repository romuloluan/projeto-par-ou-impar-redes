import socket
import json 

class ServidorJogo:
    def __init__(self):
        """
        Construtor da classe: Configura e inicia o Socket do Servidor.
        Aqui definimos que usaremos a arquitetura TCP/IP para a comunicação.
        """

        # --- CONFIGURAÇÕES DE REDE ---

        # '' (Vazio) significa que o servidor vai escutar em TODAS as placas de rede disponíveis 
        # (Wi-Fi, Cabo, Localhost). Isso torna o servidor acessível na rede local.
        self.host = ''

        # Porta lógica onde o serviço vai rodar. Portas altas (>1024) evitam conflitos com o sistema.
        # O Cliente deve se conectar EXATAMENTE nesta porta.
        self.port = 50000

        # CRIAÇÃO DO SOCKET (PONTO FINAL DE COMUNICAÇÃO)
        # socket.AF_INET  -> Define a família de endereços IPv4 (ex: 192.168.1.5).
        # socket.SOCK_STREAM -> Define o protocolo de transporte TCP (Transmission Control Protocol).
        # O TCP garante que os dados cheguem na ordem certa, sem erros e sem perdas (confiável).
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        
        # Configuração avançada para liberar a porta imediatamente caso o servidor seja fechado e reaberto.
        # Evita o erro "Address already in use" (Endereço já em uso), muito comum em desenvolvimento.
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            # BIND (VINCULAÇÃO):
            # Associa este programa (processo Python) ao IP e Porta definidos acima.
            # A partir de agora, o Sistema Operacional sabe que pacotes chegando na porta 50000 são para nós.
            self.server_socket.bind((self.host, self.port)) 

            # LISTEN (ESCUTA):
            # Coloca o socket em modo passivo, aguardando conexões de entrada.
            # O parâmetro (1) é o 'backlog': define que aceitamos apenas 1 pessoa na fila de espera.
            self.server_socket.listen(1)
            
            print(f"Servidor TCP iniciado na porta {self.port}. Aguardando pedidos de conexão...")
            
        except Exception as e:
            print(f"Erro fatal ao iniciar o socket do servidor: {e}")

    def iniciar(self):
        """
        ESTABELECIMENTO DA CONEXÃO (Handshake TCP).
        Este método é bloqueante: o código para aqui até que um cliente tente se conectar.
        """
        print("Aguardando Handshake (SYN) do Cliente...")
        
        # ACCEPT (ACEITE):
        # Quando um cliente conecta, o 'accept' retorna dois valores fundamentais:
        # 1. self.socket_cliente: Um NOVO objeto socket exclusivo para conversar APENAS com este cliente.
        #    (O server_socket original continua livre para escutar novas pessoas, se quiséssemos).
        # 2. self.endereco_cliente: Uma tupla com (IP, Porta) de quem se conectou.
        self.socket_cliente, self.endereco_cliente = self.server_socket.accept()
        
        print(f"Conexão TCP estabelecida com sucesso: {self.endereco_cliente}")

    def obter_ip_local(self):
        """
        Utilitário: Descobre o endereço IP da máquina na rede local (ex: 192.168.0.X).
        Isso ajuda o usuário a saber qual IP informar para o amigo conectar.
        """
        try:
            # Cria um socket UDP temporário apenas para consultar a tabela de roteamento do SO.
            # O protocolo UDP é "connectionless", ou seja, não precisa conectar de verdade para funcionar.
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80)) # Simula conexão com Google DNS
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1" # Retorno padrão (localhost) se não houver rede ou der erro

    def aguardar_jogada_cliente(self):  
        """
        RECEBIMENTO DE DADOS (Camada de Aplicação).
        Fica aguardando o cliente enviar o pacote JSON com a jogada completa.
        """
        try:
            print("SERVER: Aguardando fluxo de dados do cliente...")
            
            # RECV (RECEIVE):
            # Lê até 2048 bytes do buffer de entrada da placa de rede.
            # Esta chamada é 'bloqueante': o thread trava aqui até chegarem dados.
            dados_bytes = self.socket_cliente.recv(2048)
            
            # Se recv retornar vazio (b''), significa que o cliente enviou um FIN (fechou conexão)
            # ou a conexão caiu abruptamente.
            if not dados_bytes:
                return None
            
            # ACK DE APLICAÇÃO (Confirmação):
            # Enviamos uma pequena mensagem 'ack' para avisar ao software do cliente
            # que recebemos os dados com sucesso. Isso garante sincronia entre as telas.
            self.socket_cliente.send(b"ack")
            
            # PROCESSAMENTO (SERIALIZAÇÃO):
            # 1. decode(): Converte bytes binários para string (UTF-8).
            # 2. json.loads(): Converte string JSON para Dicionário Python.
            dados_str = dados_bytes.decode()
            dados_dict = json.loads(dados_str)
            
            print(f"SERVER: Pacote recebido e processado: {dados_dict}")
            
            return dados_dict
            
        except Exception as e:
            print(f"Erro na camada de transporte ao receber jogada: {e}")
            return None

    def processar_vencedor(self, nome_serv, num_serv, dados_cliente):
        """
        LÓGICA DE NEGÓCIO (Regra do Jogo).
        Este método encapsula a inteligência do jogo. Ele não sabe nada sobre interface gráfica,
        apenas recebe dados brutos, faz a matemática e retorna o resultado.
        
        Parâmetros:
            nome_serv (str): Nome do Servidor.
            num_serv (int): Número escolhido pelo Servidor.
            dados_cliente (dict): Dicionário com {nome, numero, escolha} do Cliente.
            
        Retorna:
            dict: Pacote final com soma, vencedor e mensagem explicativa.
        """
        # 1. Extração de Dados
        num_cliente = dados_cliente['numero']
        escolha_cliente = dados_cliente['escolha'] # "P" ou "I"
        nome_cliente = dados_cliente['nome']
        
        # 2. Cálculo Matemático (Core do Jogo)
        soma = num_serv + num_cliente
        deu_par = (soma % 2 == 0)
        
        vencedor = ""
        resultado_txt = ""

        # 3. Definição do Vencedor
        if deu_par:
            resultado_txt = "PAR"
            # Se deu PAR e cliente escolheu PAR (P), cliente ganha.
            if escolha_cliente == "P":
                vencedor = nome_cliente
            else:
                vencedor = nome_serv
        else:
            resultado_txt = "ÍMPAR"
            # Se deu IMPAR e cliente escolheu IMPAR (I), cliente ganha.
            if escolha_cliente == "I":
                vencedor = nome_cliente
            else:
                vencedor = nome_serv
            
        # 4. Montagem do Pacote de Resposta
        pacote_resultado = {
            "soma": soma,
            "resultado_texto": resultado_txt,
            "vencedor": vencedor,
            "msg": f"{num_cliente} + {num_serv} = {soma} ({resultado_txt})"
        }
        
        return pacote_resultado

    def enviar_resultado(self, pacote_resultado):
        """
        ENVIO DE DADOS (Resposta).
        Serializa o resultado calculado e envia de volta pelo túnel TCP estabelecido.
        """
        try:
            # SERIALIZAÇÃO:
            # Transforma o objeto Python (Dicionário) em formato de texto JSON para transporte,
            # pois o Socket só trafega bytes lineares.
            msg_json = json.dumps(pacote_resultado)
            
            # Verifica se o túnel (socket_cliente) ainda existe
            if hasattr(self, 'socket_cliente'):
                # SEND (ENVIAR):
                # Transforma a string em bytes (.encode) e empurra para a rede.
                self.socket_cliente.send(msg_json.encode())
                print("Resultado enviado para o cliente. Ciclo de jogada concluído.")
            else:
                print("Erro: Tentativa de envio sem conexão ativa.")
                
        except Exception as e:
            print(f"Erro ao enviar dados no servidor: {e}")

    # Observação: O encerramento definitivo da conexão (socket.close) é gerenciado 
    # pela Interface Gráfica quando o usuário clica em "Voltar" ou fecha a janela.