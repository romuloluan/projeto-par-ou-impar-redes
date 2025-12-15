import threading 
import sys
import os
from servidor_oop import ServidorJogo
from cliente_oop import ClienteJogo
import tkinter as tk
from PIL import Image, ImageTk 

def caminho_recurso(caminho_relativo):
    """ Retorna o caminho absoluto, funcione em dev ou como exe """
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, caminho_relativo)

class JogoGUI:
    def __init__(self, master):
        """
        Construtor da Interface Gráfica.
        Configura a janela principal, cores e carrega os recursos visuais.
        """
        self.master = master
        self.master.title("Par ou Ímpar - Projeto de Redes TCP/IP")
        self.master.geometry("500x500") 
        self.master.resizable(False, False)

        # Paleta de Cores (Design Flat)
        self.cor_fundo = "#2c3e50" # Azul Petróleo Escuro
        self.cor_texto = "#ecf0f1" # Branco Gelo
        self.cor_btn_1 = "#e74c3c" # Vermelho Alizarin
        self.cor_btn_2 = "#3498db" # Azul Peter River
        self.cor_btn_txt = "#ffffff"

        self.master.configure(bg=self.cor_fundo)

# --- CARREGAMENTO DE ASSETS (IMAGEM) ---
        try:
            # Tenta carregar e redimensionar a logo do jogo
            # !!! AQUI ESTÁ A MUDANÇA: USAMOS A FUNÇÃO NOVA !!!
            caminho_imagem = caminho_recurso("logo_jogo.png") 
            imagem_bruta = Image.open(caminho_imagem)
            
            imagem_redimensionada = imagem_bruta.resize((250, 150), Image.LANCZOS)
            self.imagem_logo = ImageTk.PhotoImage(imagem_redimensionada)
        except Exception as e:
            print(f"Aviso: Não foi possível carregar 'logo_jogo.png'. Erro: {e}")
            self.imagem_logo = None

        # Carrega a primeira tela (Menu Principal)
        self.montar_menu_principal()

    # --- MÉTODOS UTILITÁRIOS DE TELA ---

    def limpar_janela(self):
        """
        Remove todos os widgets (botões, textos) da tela atual 
        para permitir desenhar a próxima tela limpa.
        """
        for itens_tela in self.master.winfo_children():
            itens_tela.destroy()

    def montar_menu_principal(self):
        """
        Tela Inicial: Permite ao usuário escolher o papel na rede:
        - Servidor (Host/Criador da Sala)
        - Cliente (Guest/Quem entra na Sala)
        """
        self.limpar_janela()

        # 1. Título e Logo
        self.titulo = tk.Label(self.master, text="JOGO - PAR OU ÍMPAR", 
                               font=("Arial", 20, "bold"),
                               bg=self.cor_fundo, fg=self.cor_texto)
        self.titulo.pack(pady=(30, 10))

        if self.imagem_logo:
            self.lbl_imagem = tk.Label(self.master, image=self.imagem_logo, bg=self.cor_fundo)
            self.lbl_imagem.pack(pady=10) 

        # 2. Botões de Escolha
        self.frame_menu = tk.Frame(self.master, bg=self.cor_fundo)
        self.frame_menu.pack(expand=True)

        tk.Label(self.frame_menu, text="ESCOLHA SEU MODO DE JOGO: ", 
                 font=("Arial", 12, "bold"),
                 bg=self.cor_fundo, fg=self.cor_texto).grid(row=0, column=0, columnspan=2, pady=10)

        # Botão Host
        btn_servidor = tk.Button(self.frame_menu, text="CRIAR SALA", width=20, height=2,
                                 bg=self.cor_btn_1, fg=self.cor_btn_txt, font=("Arial", 10, "bold"),
                                 command=self.clique_servidor)
        btn_servidor.grid(row=1, column=0, pady=10, padx=10)

        # Botão Guest
        btn_cliente = tk.Button(self.frame_menu, text="ENTRAR EM SALA", width=20, height=2,
                                bg=self.cor_btn_2, fg=self.cor_btn_txt, font=("Arial", 10, "bold"),
                                command=self.clique_cliente)
        btn_cliente.grid(row=1, column=1, pady=10, padx=10)

    # --- LÓGICA DE NAVEGAÇÃO ---

    def clique_servidor(self):
        self.montar_tela_servidor()

    def clique_cliente(self):
        self.montar_tela_cliente()

    #___________________________________________________________________
    # PARTE 1: FLUXO DO CLIENTE (QUEM ENTRA NA SALA)
 

    def montar_tela_cliente(self):
        self.limpar_janela()
        
        tk.Label(self.master, text="CONECTAR AO SERVIDOR", font=("Arial", 16, "bold"),
                 bg=self.cor_fundo, fg=self.cor_texto).pack(pady=30)
        
        frame_input = tk.Frame(self.master, bg=self.cor_fundo)
        frame_input.pack()
        
        tk.Label(frame_input, text="Digite o IP:", font=("Arial", 12),
                 bg=self.cor_fundo, fg=self.cor_texto).grid(row=0, column=0, padx=10)
        
        self.entrada_ip = tk.Entry(frame_input, font=("Arial", 12), width=20)
        self.entrada_ip.grid(row=0, column=1, padx=10)
        self.entrada_ip.insert(0, "localhost") # Facilitador para testes locais
        
        btn_conectar = tk.Button(self.master, text="CONECTAR", width=20, height=2,
                                 bg=self.cor_btn_2, fg=self.cor_btn_txt, font=("Arial", 10, "bold"),
                                 command=self.acao_conectar) 
        btn_conectar.pack(pady=30)
        
        tk.Button(self.master, text="Voltar", command=self.montar_menu_principal).pack()

    def acao_conectar(self):
        """
        Inicia o processo de conexão TCP.
        
        CONCEITO DE THREADS (CONCORRÊNCIA):
        A interface gráfica roda em um loop infinito (mainloop). Se tentarmos conectar
        diretamente aqui, e a rede demorar 5 segundos, a janela vai 'congelar' por 5 segundos.
        Para evitar isso, criamos uma 'Thread' (processo paralelo) apenas para cuidar da rede.
        """
        ip_digitado = self.entrada_ip.get()
        print(f"GUI: Iniciando thread de conexão com {ip_digitado}...")

        # 1. Instancia a classe de Rede do Cliente (Lógica OOP)
        self.backend_cliente = ClienteJogo()

        # 2. Dispara a Thread
        t = threading.Thread(target=self.esperar_conexao_cliente, args=(ip_digitado,), daemon=True)
        t.start()

    def esperar_conexao_cliente(self, ip_alvo):
        """
        Método executado em BACKGROUND (Segundo plano).
        Tenta o Handshake TCP.
        """
        try:
            # Chama o método .connect() do socket (pode ser bloqueante)
            self.backend_cliente.conectar(ip_alvo)
            
            # Se a linha acima não der erro, atualizamos a tela para o formulário de jogo
            self.ir_para_jogo_cliente()
            
        except Exception as e:
            print(f"GUI: Erro na thread de conexão: {e}")

    def ir_para_jogo_cliente(self):
        """
        Formulário onde o Cliente preenche seus dados de jogo.
        """
        self.limpar_janela()

        tk.Label(self.master, text="SUA VEZ DE JOGAR", font=("Arial", 18, "bold"), 
                 bg=self.cor_fundo, fg=self.cor_texto).pack(pady=20)

        # Input Nome
        frame_nome = tk.Frame(self.master, bg=self.cor_fundo)
        frame_nome.pack(pady=5)
        tk.Label(frame_nome, text="Seu Nome:", font=("Arial", 12), bg=self.cor_fundo, fg=self.cor_texto).pack(side=tk.LEFT)
        self.entry_nome = tk.Entry(frame_nome, width=20, font=("Arial", 11))
        self.entry_nome.pack(side=tk.LEFT, padx=10)

        # Escolha (Radio Buttons para Par/Ímpar)
        tk.Label(self.master, text="Escolha sua opção:", font=("Arial", 12), bg=self.cor_fundo, fg=self.cor_texto).pack(pady=(20, 5))
        self.var_escolha = tk.StringVar(value="P") 
        frame_radio = tk.Frame(self.master, bg=self.cor_fundo)
        frame_radio.pack()
        
        tk.Radiobutton(frame_radio, text="PAR", variable=self.var_escolha, value="P",
                       font=("Arial", 10, "bold"), bg=self.cor_fundo, fg="white", 
                       selectcolor=self.cor_btn_1, activebackground=self.cor_fundo).pack(side=tk.LEFT, padx=20)
        
        tk.Radiobutton(frame_radio, text="ÍMPAR", variable=self.var_escolha, value="I",
                       font=("Arial", 10, "bold"), bg=self.cor_fundo, fg="white",
                       selectcolor=self.cor_btn_2, activebackground=self.cor_fundo).pack(side=tk.LEFT, padx=20)

        # Input Número (Spinbox)
        tk.Label(self.master, text="Seu Número (0 a 10):", font=("Arial", 12), bg=self.cor_fundo, fg=self.cor_texto).pack(pady=(20, 5))
        self.spin_numero = tk.Spinbox(self.master, from_=0, to=10, width=5, font=("Arial", 16, "bold"), state="readonly", justify="center")
        self.spin_numero.pack()

        # Botão Enviar
        tk.Button(self.master, text="ENVIAR JOGADA", width=25, height=2, bg="#27ae60", fg="white", font=("Arial", 12, "bold"),
                  command=self.acao_enviar_jogada_cliente).pack(pady=30)

    def acao_enviar_jogada_cliente(self):
        # 1. Coleta dados da UI (View)
        nome = self.entry_nome.get().strip()
        escolha = self.var_escolha.get()
        numero = self.spin_numero.get()

        if not nome:
            print("Validação: O nome é obrigatório.")
            return

        # 2. Prepara o Dicionário de Dados
        dados_jogada = {
            "nome": nome,
            "escolha": escolha,
            "numero": int(numero)
        }

        try:
            # 3. Envia para a rede via Backend (Controller/Model)
            self.backend_cliente.enviar_jogada(dados_jogada)
            print("GUI: Dados enviados com sucesso. Aguardando cálculo do servidor...")
            self.ir_para_espera_resultado_cliente()
        except Exception as e:
            print(f"GUI: Erro ao enviar jogada: {e}")

    def ir_para_espera_resultado_cliente(self):
        """
        Tela de espera. Fica aguardando o servidor processar e retornar quem ganhou.
        """
        self.limpar_janela()
        tk.Label(self.master, text="JOGADA ENVIADA!", font=("Arial", 18, "bold"), fg="#27ae60", bg=self.cor_fundo).pack(pady=40)
        tk.Label(self.master, text="Aguardando o Servidor jogar e calcular...", font=("Arial", 12), fg=self.cor_texto, bg=self.cor_fundo).pack()
        
        # Inicia Thread para esperar a resposta (recv é bloqueante)
        t = threading.Thread(target=self.thread_esperar_resultado_final_cliente, daemon=True)
        t.start()

    def thread_esperar_resultado_final_cliente(self):
        # Esta linha bloqueia a thread até chegar o pacote TCP do servidor
        resultado = self.backend_cliente.receber_resultado()
        
        if resultado:
            self.mostrar_vencedor(resultado)

    # ___________________________________________________________________
    # PARTE 2: FLUXO DO SERVIDOR (QUEM CRIA A SALA)
  

    def montar_tela_servidor(self):
        """
        Prepara a visualização do Servidor.
        """
        self.limpar_janela()

        # Truque: Instanciamos o servidor rapidamente apenas para descobrir o IP da máquina
        # e exibir na tela para o usuário. Logo fechamos para não travar a porta.
        try:
            temp_server = ServidorJogo()
            meu_ip = temp_server.obter_ip_local()
            temp_server.server_socket.close() 
        except:
            meu_ip = "Desconhecido"

        lbl_titulo = tk.Label(self.master, text="AGUARDANDO JOGADOR...", font=("Arial", 16, "bold"), bg=self.cor_fundo, fg=self.cor_texto)
        lbl_titulo.pack(pady=30)

        texto_ip = f"SALA CRIADA!\n\nSEU IP É: {meu_ip}\n\nAGUARDANDO O OPONENTE SE CONECTAR..."
        tk.Label(self.master, text=texto_ip, font=("Arial", 14, "bold"), bg=self.cor_fundo, fg="#f1c40f").pack(pady=20)
        tk.Label(self.master, text="Porta: 50000", font=("Arial", 10), bg=self.cor_fundo, fg=self.cor_texto).pack(pady=5)

        # Inicia o servidor automaticamente (em Thread)
        self.acao_iniciar_servidor()

        tk.Button(self.master, text="VOLTAR", bg=self.cor_btn_1, fg=self.cor_btn_txt,
                  command=self.voltar_e_fechar_servidor).pack(pady=30)

    def acao_iniciar_servidor(self):
        print("GUI: Iniciando servidor (bind/listen) em Thread paralela...")
        self.backend_servidor = ServidorJogo()
        
        # Thread para esperar a conexão (accept) sem congelar a janela
        t = threading.Thread(target=self.esperar_conexao_servidor, daemon=True)
        t.start()

    def esperar_conexao_servidor(self):
        """
        Thread que fica parada no .accept() aguardando alguém entrar.
        """
        try:
            self.backend_servidor.iniciar() 
            print("GUI: Cliente conectado! Mudando para tela de jogo...")
            self.ir_para_jogo_servidor()
        except OSError:
            print("GUI: Socket fechado manualmente (usuário voltou ao menu).")
            return 
        except Exception as e:
            print(f"GUI: Erro inesperado na thread do servidor: {e}")

    def ir_para_jogo_servidor(self):
        """
        Tela onde o Servidor espera o Cliente mandar sua jogada.
        """
        self.limpar_janela()
        tk.Label(self.master, text="ADVERSÁRIO ENCONTRADO!", font=("Arial", 18, "bold"), fg="#27ae60", bg=self.cor_fundo).pack(pady=40)
        tk.Label(self.master, text="Aguardando o ADVERSÁRIO fazer a jogada...", font=("Arial", 12), fg=self.cor_texto, bg=self.cor_fundo).pack()
        
        # Thread para esperar os dados (Nome, Escolha, Número) do cliente
        t = threading.Thread(target=self.thread_esperar_dados_cliente, daemon=True)
        t.start()

    def thread_esperar_dados_cliente(self):
        # Fica bloqueado esperando o JSON do cliente
        dados = self.backend_servidor.aguardar_jogada_cliente()
        
        if dados:
            print(f"GUI: Dados recebidos do cliente: {dados}")
            self.ir_para_formulario_servidor(dados)
        else:
            print("GUI: Erro na recepção de dados.")

    def ir_para_formulario_servidor(self, dados_cliente):
        """
        Tela onde o Servidor insere seus dados e finaliza o jogo.
        """
        self.dados_cliente_cache = dados_cliente # Salva os dados do oponente para usar no cálculo
        self.limpar_janela()

        # Lógica visual: Mostra o que o cliente escolheu e o que sobrou para o servidor
        escolha_cliente = dados_cliente['escolha']
        nome_cliente = dados_cliente['nome']
        
        if escolha_cliente == "P":
            txt_cliente = "PAR"
            minha_escolha = "ÍMPAR"
            cor_minha = self.cor_btn_2 # Azul
        else:
            txt_cliente = "ÍMPAR"
            minha_escolha = "PAR"
            cor_minha = self.cor_btn_1 # Vermelho

        tk.Label(self.master, text="SUA VEZ!", font=("Arial", 20, "bold"), bg=self.cor_fundo, fg=self.cor_texto).pack(pady=10)
        info = f"Oponente ({nome_cliente}) escolheu {txt_cliente}.\nVocê ficou com: {minha_escolha}"
        tk.Label(self.master, text=info, font=("Arial", 14), bg=self.cor_fundo, fg="#f1c40f").pack(pady=10)

        # Inputs do Servidor
        frame_nome = tk.Frame(self.master, bg=self.cor_fundo)
        frame_nome.pack(pady=10)
        tk.Label(frame_nome, text="Seu Nome:", font=("Arial", 12), bg=self.cor_fundo, fg=self.cor_texto).pack(side=tk.LEFT)
        self.entry_nome_servidor = tk.Entry(frame_nome, width=20, font=("Arial", 11))
        self.entry_nome_servidor.pack(side=tk.LEFT, padx=10)

        tk.Label(self.master, text="Seu Número (0 a 10):", font=("Arial", 12), bg=self.cor_fundo, fg=self.cor_texto).pack(pady=(10, 5))
        self.spin_numero_servidor = tk.Spinbox(self.master, from_=0, to=10, width=5, font=("Arial", 16, "bold"), state="readonly", justify="center")
        self.spin_numero_servidor.pack()

        # Botão Calcular
        tk.Button(self.master, text="CALCULAR RESULTADO", width=25, height=2, bg=cor_minha, fg="white", font=("Arial", 12, "bold"),
                  command=self.acao_calcular_resultado_final).pack(pady=30)

    def acao_calcular_resultado_final(self):
        """
        [ATUALIZADO] Separação de Responsabilidades (MVC/OOP):
        A Interface Gráfica NÃO calcula mais quem ganhou. Ela apenas coleta os dados
        e delega o processamento para a classe ServidorJogo (Backend).
        """
        # 1. Coleta dados da View
        nome_serv = self.entry_nome_servidor.get().strip()
        num_serv = int(self.spin_numero_servidor.get())
        
        if not nome_serv:
            print("Validação: O servidor precisa de um nome!")
            return

        # 2. Chama a Lógica de Negócio (Backend)
        # O método .processar_vencedor() contém toda a matemática e regras do jogo
        pacote_resultado = self.backend_servidor.processar_vencedor(
            nome_serv, 
            num_serv, 
            self.dados_cliente_cache
        )
        
        # 3. Envia o resultado processado pela Rede
        self.backend_servidor.enviar_resultado(pacote_resultado)
        
        # 4. Atualiza a View com o resultado
        self.mostrar_vencedor(pacote_resultado)

    # ___________________________________________________________
    # TELA DE RESULTADO (COMUM PARA OS DOIS)
    

    def mostrar_vencedor(self, resultado):
        self.limpar_janela()

        vencedor_nome = resultado['vencedor']
        detalhes_conta = resultado['msg']

        tk.Label(self.master, text="RESULTADO FINAL", font=("Arial", 22, "bold"), bg=self.cor_fundo, fg="#ecf0f1").pack(pady=30)
        tk.Label(self.master, text="🏆 VENCEDOR 🏆", font=("Arial", 12, "bold"), bg=self.cor_fundo, fg="#95a5a6").pack()
        tk.Label(self.master, text=vencedor_nome.upper(), font=("Arial", 28, "bold"), bg=self.cor_fundo, fg="#f1c40f").pack(pady=(5, 20))

        frame_detalhe = tk.Frame(self.master, bg="#34495e", bd=2, relief="sunken")
        frame_detalhe.pack(pady=10, padx=20, ipadx=20, ipady=15)

        tk.Label(frame_detalhe, text="Detalhes da partida:", font=("Arial", 10), bg="#34495e", fg="#bdc3c7").pack()
        tk.Label(frame_detalhe, text=detalhes_conta, font=("Arial", 18, "bold"), bg="#34495e", fg="#ffffff").pack(pady=5)

        tk.Button(self.master, text="VOLTAR AO MENU", width=20, height=2, bg=self.cor_btn_1, fg="white", font=("Arial", 11, "bold"),
                  command=self.voltar_ao_menu_reset).pack(pady=30)

    def voltar_ao_menu_reset(self):
        """
        Encerramento seguro: Fecha conexões TCP antes de voltar ao menu.
        Isso é crucial para evitar 'Socket Leaks' e erros de porta em uso.
        """
        print("GUI: Resetando jogo e fechando sockets...")
        
        # Fecha socket do servidor, se existir
        if hasattr(self, 'backend_servidor'):
            try:
                self.backend_servidor.server_socket.close()
            except:
                pass
        
        # Fecha socket do cliente, se existir
        if hasattr(self, 'backend_cliente'):
            try:
                self.backend_cliente.client_socket.close() 
            except:
                pass

        self.montar_menu_principal()

    def voltar_e_fechar_servidor(self):
        """
        Usado quando o host desiste de esperar na sala de espera.
        """
        self.voltar_ao_menu_reset()

if __name__ == "__main__":
    root_janela = tk.Tk()
    app = JogoGUI(root_janela)
    root_janela.mainloop()