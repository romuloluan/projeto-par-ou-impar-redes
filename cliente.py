#CLIENTE

import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET: Define que usaremos IP versão 4.  SOCK_STREAM: Define que usaremos TCP.

HOST = input("Digite o IP do Servidor nesse formato (10.13.134.2): " ).strip() #APONTA PARA O SERVIDOR

PORT =50000  #MESMA PORTA DO SERVIDOR
print('\nIniciando a conexão com o servidor...')
cliente.connect ((HOST, PORT))

print('\n●●●●●●●●●● JOGO INICIADO ●●●●●●●●●●')

print("\n\n----------Bem vindo ao jogo de PAR OU IMPAR----------\n\n")

nome = input("Digite seu nome: ").strip().upper()
cliente.send(nome.encode()) #Envia o nome para o servidor.

opcao = input("Escolha (P) para PAR ou (I) para IMPAR: ").upper().strip()

cliente.send (opcao.encode()) #O .encode() transforma a string em bytes para ela poder viajar.

numero = input ("Digite um número de 0 a 10: ")

cliente.send(numero.encode())
nome_jog2= (cliente.recv(1024)).decode()  #RECEBE O NOME DO JOGADOR 2 E DECODIFICA ELE

print(f"\n Você irá jogar contra {nome_jog2}.\n")

resultado = cliente.recv(1024)

print(resultado.decode())