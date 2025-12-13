import tkinter as tk

class JogoGUI:
    def __init__(self, master):
        # 'master' é a janela principal que criamos lá embaixo
        self.master = master
        self.master.title("Par ou Ímpar - Redes")
        self.master.geometry("400x350")
        
        # --- MONTAGEM DA TELA INICIAL (MENU) ---
        
        # 1. Título (Label)
        # bg="black" (fundo), fg="white" (letra), font=("Arial", 16)
        self.titulo = tk.Label(self.master, text="JOGO - PAR OU ÍMPAR", font=("Arial", 14, "bold"))
        self.titulo.pack(pady=20) # pady=20 dá um espaço de 20px em cima e embaixo

        # 2. Subtítulo (Label)
        self.subtitulo = tk.Label(self.master, text="Escolha seu modo de jogo:", font=("Arial", 12))
        self.subtitulo.pack(pady=10)

        # 3. Botão Servidor
        self.btn_servidor = tk.Button(self.master, text="CRIAR SALA (Servidor)", width=25, height=2, command=self.clique_servidor)
        self.btn_servidor.pack(pady=5)

        # 4. Botão Cliente
        self.btn_cliente = tk.Button(self.master, text="ENTRAR (Cliente)", width=25, height=2, command=self.clique_cliente)
        self.btn_cliente.pack(pady=5)

    # --- MÉTODOS DE AÇÃO (O que acontece quando clica) ---
    
    def clique_servidor(self):
        print("Botão Servidor Clicado!")
        # Aqui depois vamos colocar a lógica de iniciar o servidor

    def clique_cliente(self):
        print("Botão Cliente Clicado!")
        # Aqui depois vamos colocar a lógica de iniciar o cliente


# --- BLOCO PRINCIPAL ---
if __name__ == "__main__":
    root = tk.Tk() # Criamos a janela raiz
    app = JogoGUI(root) # Entregamos a janela para nossa classe cuidar
    root.mainloop() # Mantém vivo