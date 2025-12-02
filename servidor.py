import socket

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #AF_INET: Define que usaremos IP versão 4.  SOCK_STREAM: Define que usaremos TCP.
HOST =""
PORT =50000 #Define a porta no qual usaremos para o programa

servidor.bind((HOST, PORT))  #INFORMA AO COMPUTADOR QUE O QUE CHEGAR NESSA PORTA PERTENCE AO PROGRAMA

servidor.listen(1) #Diz ao servidor quantos clientes (usuários) podem ficar aguardando uma conexão.

print("Aguardando conexão")

conn, ender = servidor.accept() #O código para nessa linha e fica esperando até um cliente conectar.
# quando conecta o conn recebe um novo socket só para falar com esse cliente
# ender recebe o endereço de ip de quem conectou.

print ("Conectado em", ender)

dados_recebidos = conn.recv (1024) #recv significa "receive" (receber). O 1024 é o tamanho máximo do pacote (em bytes) que vamos ler de uma vez.

opcao_cliente = dados_recebidos.decode() #Transformamos os bytes que chegaram via rede de volta em texto legível.

print("O cliente escolheu:", opcao_cliente)

dados_numero = conn.recv(1024) #recebe o numero escolhido

numero_cliente = int(dados_numero.decode())

print ("O cliente jogou o número: ", numero_cliente)

numero_servidor = int(input("Sua vez (Servidor)! Digite seu número: "))

total = numero_cliente + numero_servidor

print(f"Resultado: {numero_cliente} + {numero_servidor} = {total}")


if total % 2 == 0:
    resultado = "PAR"
    if opcao_cliente.upper() == 'P':
        vencedor = "CLIENTE"
    else:
        vencedor = "SERVIDOR"
else:
    resultado = "IMPAR"
    if opcao_cliente.upper() == 'I':
        vencedor = "CLIENTE"
    else:
        vencedor = "SERVIDOR"

msg_final = f"Deu {resultado}. Vencedor: {vencedor}"
print(msg_final)

conn.send(msg_final.encode())