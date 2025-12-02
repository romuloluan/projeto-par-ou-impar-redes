import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET: Define que usaremos IP versão 4.  SOCK_STREAM: Define que usaremos TCP.

HOST ="127.0.0.1"  #APONTA PARA O PRÓPRIO COMPUTADOR (IDEAL PARA TESTES)

PORT =50000  #MESMA PORTA DO SERVIDOR

cliente.connect ((HOST, PORT))

opcao = input("Escolha (P) para PAR ou (I) para IMPAR: ")

cliente.send (opcao.encode()) #O .encode() transforma a string em bytes para ela poder viajar.

numero = input ("Digite um número de 0 a 10: ")

cliente.send(numero.encode())

resultado = cliente.recv(1024)

print(resultado.decode())