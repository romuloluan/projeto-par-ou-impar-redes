#SERVIDOR

import socket

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #AF_INET: Define que usaremos IP versão 4.  SOCK_STREAM: Define que usaremos TCP.

HOST =""

PORT =50000 #Define a porta no qual usaremos para o programa

servidor.bind((HOST, PORT))  #INFORMA AO COMPUTADOR QUE O QUE CHEGAR NESSA PORTA PERTENCE AO PROGRAMA

servidor.listen(1) #Diz ao servidor quantos clientes (usuários) podem ficar aguardando uma conexão.

print("Servidor ligado!\n\nAguardando conexão...")

conn, ender = servidor.accept() #O código para nessa linha e fica esperando até um cliente conectar.
# quando conecta o conn recebe um novo socket só para falar com esse cliente
# ender recebe o endereço de ip de quem conectou.

print ("Conectado em", ender)

print('\n●●●●●●●●●● JOGO INICIADO ●●●●●●●●●●')
print("\n\n----------Bem vindo ao jogo de PAR OU IMPAR----------\n\n")

print("\n\nAguardando o Jogador 1 jogar...\n\n")


nome_jog1= (conn.recv (1024)).decode() #recebe o nome do Jogador 1.

dados_opcao_jog1 = conn.recv (1024) #recv significa "receive" (receber). O 1024 é o tamanho máximo do pacote (em bytes) que vamos ler de uma vez.

opcao_jog1= dados_opcao_jog1.decode() #Transformamos os bytes que chegaram via rede de volta em texto legível.

numero_jog1 =int((conn.recv(1024)).decode()) #recebe o numero escolhido

print("\n\nAGORA É SUA VEZ!\n\n")

nome_jog2= input("\n\nDigite seu nome: ").strip().upper()

conn.send(nome_jog2.encode()) #ENVIA O NOME DO JOGADOR 2 PARA O CLIENTE.

print(f"\n Olá {nome_jog2}, você irá jogar contra {nome_jog1}.")

if opcao_jog1=="P":
    opcao_jog2="I"
    print (f"\nO jogador(a) {nome_jog1} escolheu PAR... \nLogo você é IMPAR\n")

else:
    opcao_jog2="P"
    print (f"\nO jogador(a) {nome_jog1} escolheu IMPAR...\nLogo você é PAR\n")

  
numero_jog2 = int(input("Sua vez, Digite um número de 0 a 10: "))

total = numero_jog1 + numero_jog2

print(f"Resultado: {numero_jog1} + {numero_jog2} = {total}")


if total % 2 == 0:
    resultado = "PAR"
    if opcao_jog1.upper() == 'P':
        vencedor = nome_jog1
    else:
        vencedor = nome_jog2
else:
    resultado = "IMPAR"
    if opcao_jog1.upper() == 'I':
        vencedor = nome_jog1
    else:
        vencedor = nome_jog2

msg_final = f"Deu {resultado}. Vencedor: {vencedor}"
print(msg_final)

conn.send(msg_final.encode())