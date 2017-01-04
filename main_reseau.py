#!/usr/bin/env python3
from socket import *
from grid import *

import select
import threading
import random


# def main():
# 	socket_listen = socket(AF_INET6, SOCK_STREAM, 0)

# 	socket_listen.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# 	socket_listen.bind(('', 7777))
# 	socket_listen.listen(1)

# 	list_clients = []
# 	list_clients.append(socket_listen)

# 	while(True):
# 		(ready_sockets, [], []) = select.select(list_clients, [], [])
# 		for i in range(len(ready_sockets)):
# 			if ready_sockets[i] == socket_listen :
# 				(socket_recv, addr_recv) = socket_listen.accept()
# 				list_clients.append(socket_recv)
# 			else:
# 				bytes_recv = ready_sockets[i].recv(4096)
# 				if len(bytes_recv) == 0: #deconnexion
# 					list_clients.remove(ready_sockets[i])
# 					ready_sockets[i].close()

# 				else:#envoi de message
# 					for j in range(len(list_clients)):
# #						if list_clients[j] != socket_listen and list_clients[j] != ready_sockets[i]:
# 						list_clients[j].send(bytes_recv)

# #!/usr/bin/python3

# from grid import *
# import  random

class Client:

	cId = None
	socket = None
	score = 0

	def __init__(self, socket):
		self.socket = socket

	def setId(self, cid):
		this.cId = cid

	def sendMessage(self, text):
		self.socket.send(str.encode(text))

class Player:

	pGrid = None
	pClient = None
	pId = 0


	def __init__(self, client):
		self.pGrid = grid()
		self.pClient = client

	def setId(self, pid):
		self.pId = pid

	def sendMessage(self, text):
		self.pClient.sendMessage(text)

	def displayGrid(self):
		self.sendMessage(pGrid.displayStr())

class Host:

	listClient = []
	socketListener = None
	currentPlayer = -1
	hGrid = None
	players = []
	specs = []

	def __init__(self, socketListener):
		self.socketListener = socketListener
		self.hGrid = grid()

	def isGameOver(self):
		if self.hGrid.gameOver() != -1 :
			self.currentPlayer = -1
		return self.hGrid.gameOver()

	def playMove(self, case):	#returns 1 if ok
		if self.hGrid.cells[case] == EMPTY:
			self.hGrid.play(self.currentPlayer, case)
			return 1
		else:
			p = self.getPlayer(currentPlayer)
			p.pGrid[case] = self.hGrid[case]
			return 0

	def switchPlayer(self):
		self.currentPlayer = (self.currentPlayer + 1) % 2

	def addNewClient(self, socket):
		(socket_recv, addr_recv) = self.socketListener.accept()
		c = Client(socket_recv)
		self.listClient.append(c)
		c.setId(len(listClient))

	def setNewPlayer(self, client):
		if len(self.players) <= 1:
			p = Player(client)
			self.players.append(p)
			p.setId(len(self.players))
		else:
			return

	def getPlayerId(self, socket):
		for p in self.players:
			if socket == p.pClient.socket:
				return p.pId
		return -1

	def getPlayer(self, pid):
		for p in self.players:
			if pid == p.pId:
				return p
		return -1

	def getCliendId(self, socket):
		for c in listClient:
			if socket == c.cId:
				return c.cId
		return -1

	def getClient(self, cid):
		for c in clients:
			if cid == c.cId:
				return c
		return -1

	def isGameReady(self):
		if len(players) == 2:
			return 1
		return 0

	def startGame(self):
		self.hGrid = grid()
		self.currentPlayer = 1


def printGridPlayer(socket, str_grid):
	socket.send(str.encode(str_grid))

def sendBegin(socket_j1, socket_j2, current_player):
	# print(current_player)
	if(socket_j1 == None or socket_j2 == None):
		return
	if(current_player == J1):
		socket_j1.send(str.encode("begin"))
	else:
		socket_j2.send(str.encode("begin"))

def playMove(bytes_recv, socket_player):
	global current_player 
	global grids 
	shot = int(bytes.decode(bytes_recv))
	if grids[0].cells[shot] != EMPTY: # Si la case est déjà prise alors on réactualise la grille du joueur et on la reaffiche
		grids[current_player].cells[shot] = grids[0].cells[shot]
		socket_player.send(str.encode( grids[current_player].displayStr() ))
		# socket_player.send(str.encode("Choose another case."))
		sendBegin(socket_j1, socket_j2, current_player)
	else: #Sinon le coup est joué, on actualise les grilles et on réaffiche celle du joueur
		grids[current_player].cells[shot] = current_player
		grids[0].play(current_player, shot)
		socket_player.send(str.encode( grids[current_player].displayStr() ))
		current_player = current_player%2 + 1
	print("c'est au tour du joueur" + str(current_player) )

def main_old():
	socket_listen = socket(AF_INET6, SOCK_STREAM, 0)
	socket_listen.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	socket_listen.bind(('', 7777))
	socket_listen.listen(1)
	global socket_j1, socket_j2
	socket_j1 = None
	socket_j2 = None
	list_clients = []
	list_clients.append(socket_listen)

	global current_player 
	global grids 
	current_player = J1
	grids = [grid(), grid(), grid()]

	while(grids[0].gameOver() == -1):
		(ready_sockets, [], []) = select.select(list_clients, [], [])
		for i in range(len(ready_sockets)):
			if ready_sockets[i] == socket_listen: # Connexion d'un client
				if socket_j1 == None or socket_j2 == None:
					(socket_recv, addr_recv) = socket_listen.accept()
					print("Connexion en cours avec un client...")

					if socket_j1 == None:
						print("joueur1 est connecté ..")
						socket_j1 = socket_recv
						list_clients.append(socket_recv)
						socket_j1.send(str.encode(grids[J1].displayStr() ))

					elif socket_j2 == None:
						print("joueur2 est connecté ..")
						socket_j2 = socket_recv
						list_clients.append(socket_recv)
						socket_j2.send(str.encode(grids[J2].displayStr() ))
						sendBegin(socket_j1, socket_j2, current_player)

				else:
					socket_recv.send(str.encode("Server is full."))

			elif socket_j1 != None and socket_j2 != None : #Reception d'un message d'une socket joueur

				bytes_recv = ready_sockets[i].recv(1024) 
				# print(current_player)
				if len(bytes_recv) == 0: #Deconnexion
					list_clients.remove(ready_sockets[i])
					ready_sockets[i].close()
				elif ready_sockets[i] == socket_j1 and current_player == J1 : #Si c'est au joueur1
					playMove(bytes_recv, socket_j1) #on joue le move
					sendBegin(socket_j1, socket_j2, current_player)

				elif ready_sockets[i] == socket_j2 and current_player == J2 : #si c'est au j2
					playMove(bytes_recv, socket_j2) # on joue le move
					sendBegin(socket_j1, socket_j2, current_player)

				else:
					print("something's wrong ...")
	#FIN DE PARTIE / ANNONCE DES SCORES
	socket_j1.send(str.encode("GAME OVER !"))
	socket_j2.send(str.encode("GAME OVER !"))

	socket_j1.send(str.encode( grids[0].displayStr() ))
	socket_j2.send(str.encode( grids[0].displayStr() ))

	if grids[0].gameOver() == J1:
		socket_j1.send(str.encode( "YOU WIN !" ))
		socket_j2.send(str.encode( "YOU LOOSE !" ))

	elif grids[0].gameOver() == J2:
		socket_j2.send(str.encode( "YOU WIN !" ))
		socket_j1.send(str.encode( "YOU LOOSE !" ))
	else:
		socket_j1.send(str.encode("EGALITY"))
		socket_j2.send(str.encode("EGALITY"))

	socket_j1.close()
	socket_j2.close()


def main():
	socket_listen = socket(AF_INET6, SOCK_STREAM, 0)
	socket_listen.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	socket_listen.bind(('', 7777))
	socket_listen.listen(1)

	host = Host(socket_listen)

	while(1):
		if (host.isGameOver() == 1):
			host.getPlayer(host.isGameOver()).sendMessage("You win")
			host.getPlayer((host.isGameOver() + 1 )% 2).sendMessage("You loose")
		(ready_sockets, [], []) = select.select(host.listClient, [], [])
		for current_socket in ready_sockets:
			if current_socket == host.socketListener:
				host.addNewClient(socket)
				print("Nouveau client connecté")
			else:
				cId = host.getClientId(socket)
				pId = host.getPlayerId(socket)
				bytes_recv = current_socket.recv(1024)
				if pId != -1:
					if pId == host.currentPlayer:
						if host.playMove(bytes_recv) == 1:
							host.switchPlayer()
						host.getPlayerId(pId).displayGrid()
				else:
					if bytes_recv == "play":
						host.setNewPlayer(host.getClient(cId))
						if host.isGameReady() == 1:
							host.startGame()
						else:
							host.getClient(cId).sendMessage("Waiting opposent...")








main()