#!/usr/bin/python
from socket import *
from time import ctime
import threading
import re
import time
HOST = ''
PORT = 21563
BUFSIZ = 1024
ADDR = (HOST, PORT)

def Deal(sock, user):
	friend = []
	friend = friend_table[user]
	while True:
		data = sock.recv(BUFSIZ).decode()
		tmp=data.split()
		friend_tmp=data.split()
		file=data.split()
		msg=' '
		for i in range(2,len(tmp),1):
			msg=msg+tmp[i]+' '
		
		if(data == 'quit' or data=='exit'):
			del clients[user]
			friend_table[user]=[]
			friend_table[user] = friend
			sock.send(data.encode())
			sock.close()
			break
		elif(tmp[0]=='send'): 
			if(tmp[1] in users):
				if(tmp[1] in clients):
					data=ctime()+' '+'\033[32m'+user+'\033[0m'+msg
					clients[tmp[1]].send(data.encode())
				else:
					if(tmp[1] in unsend_name):
						index=unsend_name.index(tmp[1])
						unsend_msg[index]+='\n'+msg
					else:
						unsend_name.append(tmp[1])
						unsend_msg.append(msg)
						unsend_from.append(user)
			else:
				data='the user is not exit'
				sock.send(data.encode())
		elif(friend_tmp[0]=='friend'):
			if(friend_tmp[1]=='list'):
				if len(friend) == 0:
					msg='no friend'
				else:
					for i in range(0,len(friend),1):
						if(friend[i] in clients):
							state='online'
						else:
							state='offline'
						msg=msg+friend[i]+' '+state+'\n'
				sock.send(msg.encode())
			if(friend_tmp[1]=='add'):
				if(friend_tmp[2] in users):
					if(not(friend_tmp[2] in friend)):
						index=users.index(friend_tmp[2])
						friend.append(friend_tmp[2])
						data=friend_tmp[2]+' added into the friend list'
						sock.send(data.encode())
					else:
						data='the user '+friend_tmp[2]+' is exist in frined list'
						sock.send(data.encode())
					
				else:
					data='the user '+friend_tmp[2]+' is not exist'
					sock.send(data.encode())
			if(friend_tmp[1]=='rm'):
				index=friend.index(friend_tmp[2])
				del friend[index]
				data=friend_tmp[2]+' removed from the friend list'
				sock.send(data.encode())
		elif(file[0]=='sendfile'):  
			if(tmp[1] in users):
				if(tmp[1] in clients):
					if(file[2]=='y'):
						data='y'
						sock.send(data.encode())
						time.sleep(1) 
						if((file[1] in fileowner) and (user in fileto)):
							index=fileowner.index(file[1])
							fp = open(filename[index],'rb')
							while 1:
								filedata = fp.read(1024)
								if not filedata: break
								sock.send(filedata)
							fp.close()
							del fileowner[index]
							del fileto[index]
							del filename[index]
							data='end of filename transmitted'
							clients[file[1]].send(data.encode())
						else:
							data=file[1]+' no file to send'
							sock.send(data.encode())
					elif(file[2]=='n'):
						data='n'
						sock.send(data.encode())
						time.sleep(1) 
						if((file[1] in fileowner) and (user in fileto)):
							index=fileowner.index(file[1])
							data='denied from '+user
							del fileto[index]
							del fileowner[index]
							del filename[index]
							clients[file[1]].send(data.encode())
						else:
							data=file[1]+' no file to send'
							sock.send(data.encode())
					else:
						data='Are you accept '+file[2]+' from '+user+' ?(sendfile file_owner y/n)'
						if(not(user in fileowner) or not(file[1] in fileto)):
							fileowner.append(user)
							filename.append(file[2])
							fileto.append(file[1])
						else: 
							
							index=fileto.index(file[1])
							filename[index]=file[2]
							
						clients[file[1]].send(data.encode())
					
				else:
					data=tmp[1]+' is offline'
					sock.send(data.encode())
			else:
				data='the user is not exit'
				sock.send(data.encode())
		else:
			data='Please input "send anyother message"'
			sock.send(data.encode())
		

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

users = ['aa','bb','cc']
pwd = ['11','22','33']

friend_table = {}
friend_table['aa']=[]
friend_table['bb']=[]
friend_table['cc']=[]
clients = {}
unsend_name=[]
unsend_msg=[]
unsend_from=[]
fileowner = []
fileto = []
filename = []

while True:
	print ('waiting for connection...')
	tcpCliSock, addr = tcpSerSock.accept()
	print ('...connected from:',addr)
	data = tcpCliSock.recv(BUFSIZ).decode()
	name,passwd=data.split()
	
	if(name in users):
		index=users.index(name)
		if(passwd==pwd[index]):
			data='Welcom,'+name+'\n'
			if(name in unsend_name):
				index=unsend_name.index(name)
				data+='Message from '+unsend_from[index]+' :\n'+unsend_msg[index]
				del unsend_from[index]
				del unsend_name[index]
				del unsend_msg[index]
		else:
			data='password error!!'
	else:
		data='you are not member!!'
	tcpCliSock.send(data.encode())
	data = tcpCliSock.recv(BUFSIZ).decode()
	if(data=='run'):
		clients[name] = tcpCliSock
		chat = threading.Thread(target = Deal, args = (tcpCliSock,name))
		chat.start()
	
	#break
	
tcpSerSock.close()
