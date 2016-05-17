#!/usr/bin/python
from socket import *
import threading
import getpass
import time
def Send(sock, test):
	while True:
		data = input('>')
		sock.send(data.encode())
		if(data == 'quit' or data == 'exit'):
			break
			
def Recv(sock, user,tran):
	file=[]
	while True:
		
		if(tran==True):
			filename = 'new_'+file[0]
			fp = open(filename,'wb')
			while 1:
				filedata = sock.recv(1024)
				fp.write(filedata)
				if(len(filedata)-1024<0):
					fp.close()
					break
			time.sleep(2)
			print('recive OK!!')
			tran=False
			del file[0]
		else:
			data = sock.recv(BUFSIZ).decode()
			tmp=data.split()
			if(data == 'quit' or data == 'exit'):
				print('\033[36m'+username+' logout!!!'+'\033[0m')
				sock.close()
				break
			elif(tmp[0]=='Are'):
				file.append(tmp[3])
				print(data)
			elif(data=='y'):
				tran=True
			elif(data=='n'):
				if len(file) == 0:
					del file[0]
			else:
				print(data)
				

HOST = 'localhost'
PORT = 21563
BUFSIZ = 1024
ADDR = (HOST, PORT)
threads = []
tran=False

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)
username = input('Please input your username:')

passwd = getpass.getpass('Please input your password:')
data=username+' '+passwd
tcpCliSock.send(data.encode())
data=tcpCliSock.recv(BUFSIZ).decode()
print('\033[31m'+data+'\033[0m')
if(data=='password error!!' or data=='you are not member!!'):
	data='leave'
	tcpCliSock.send(data.encode())
	tcpCliSock.close()
else:
	data='run'
	tcpCliSock.send(data.encode())
	chat = threading.Thread(target = Send, args = (tcpCliSock,None))
	threads.append(chat) 
	chat = threading.Thread(target = Recv, args = (tcpCliSock,username,tran))
	threads.append(chat)
	for i in range(len(threads)):
		threads[i].start()
	threads[0].join()
