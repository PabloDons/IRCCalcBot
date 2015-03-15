import sys
import socket
import string
import random
HOST = "irc.freenode.net" #keep this the same
CHANNEL = "#OREServerChat" #keep this set to
PORT = 6667 #IRC's port, don't change
NICK = "CalcBot" #name of your bot
IDENT = "CalcBot" #more name of bot
REALNAME = "CalcBot" #bot bot bot
MASTER = "PabloPardons" #you
readbuffer = "" #can't touch this.
cmd = "calc " #what the bot looks for to execute commands

passfile=open("password.txt","r")
password=str(passfile.read())
passfile.close()

#getting connected
s=socket.socket( )
s.connect((HOST, PORT))
s.send(bytes("NICK %s\r\n" % NICK, "latin1"))
s.send(bytes("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME), "latin1"))
s.send(bytes("JOIN %s\r\n" % (CHANNEL), "latin1"))
s.send(bytes("PRIVMSG NickServ identify %s \r\n" % (password), "latin1"))

#some variables
array=[]
at1=[]
at2=[]
at3=[]
e=0
i=0
c1=0
c2=0
c3=0
output=0
d=0
d2=False
reading=False
#some functions
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
def ircsend(o):
	s.send(bytes("PRIVMSG %s :@%s %s \r\n" % (CHANNEL, getname(), o), "latin1"))
def ircquit():
	s.send(bytes("QUIT\r\n","latin1"))
def doublenn(li):
	d=0
	for n in li:
		if is_number(n):
			d=0
		else:
			d+=1
		if d==2:
			return True
def getname():
	reading=False
	array=[]
	read=False
	i=0
	for n in text:
		if n=="!" and reading:
			reading=False
		if reading:
			array.append(n)
		if i==0 and n==":":
			reading=True
		i+=1
	if "".join(array)=="ORESchool" or "".join(array)=="OREBuild":
		array=[]
		i=0
		for n in text:
			if i!=0 and n==":" and reading:
				reading=False
				break
			if reading:
				array.append(n)
			if i!=0 and n==":" and not reading and not read:
				reading=True
				read=True
			i+=1
		i=0
	return "".join(array)
	array=[]
#what your bot does after its up and running
while 1:
	text = s.recv(2040).decode("latin1") #gets data from irc and decodes it to "latin1"
	if text.find('PING') != -1:		 #confirms connection to IRC
		s.send(bytes('PONG ' + text.split() [1] + '\r\n', "latin1"))
#quit bot when you type your cmd + quit + password(without space or +)
	print (text)
	if text.find(cmd + "quit") != -1:
		if getname()==MASTER:
			ircquit()
			break
	
	if text.find(cmd + "help") != -1:
		ircsend('syntax: calc "[expression]"')
	
	if text.find(cmd + '"') != -1:
		rawtext=str(text)
		for a in rawtext:
			if a == '"' and c1 == 1:
				c1 = 2
			if c1 == 1:
				array.append(a)
			if a == '"' and c1==0:
				c1 = 1
		equation="".join(array)
		equation=equation.replace("+",",+,")
		equation=equation.replace("-",",-,")
		equation=equation.replace("*",",*,")
		equation=equation.replace("/",",/,")
		arrayequation=equation.split(",")
		i=0
		for n in arrayequation:
			if is_number(n) and n!="infinity" and n!="Infinity":
				arrayequation[i]=float(arrayequation[i])
			i+=1
		i=0
		for n in arrayequation:
			if arrayequation[i]=="":
				del arrayequation[i]
			i+=1
		i=0
		array=[]
		if equation=="help":
			pass
		elif c1 < 2:
			ircsend("Error! Did you remember quotes?")
		elif doublenn(arrayequation):
			ircsend("Error! Please doublecheck your expression")
		elif equation=="9,+,10":
			ircsend(21.0)
		else:
			for n in arrayequation:
				if is_number(n):
					arrayequation[i]=n
				if n=="*" or n=="/":
					at1.append(i)
				if n=="+" or n=="-":
					at2.append(i)
				i+=1
			i=0
			for n in at2:
				if arrayequation[n]=="-":
					arrayequation[n+1]*=-1
					arrayequation[n]=0
				if arrayequation[n]=="+":
					arrayequation[n]=0
			for n in at1:
				if arrayequation[n]=="*":
					arrayequation[n+1]*=arrayequation[n-1]
					arrayequation[n]=0
					arrayequation[n-1]=0
				if arrayequation[n]=="/":
					if arrayequation[n+1]==0:
						if e==0:
							ircsend("Error! cannot devide by 0")
						arrayequation[n]=0
						e=1
					else:
						arrayequation[n+1]=arrayequation[n-1]/arrayequation[n+1]
						arrayequation[n]=0
						arrayequation[n-1]=0
			for n in arrayequation:
				if is_number(n) and n!="infinity" and n!="Infinity":
					output+=n
				elif e==0:
					ircsend("Error! illegal characters")
					e=1
			if e==0:
				ircsend(output)
		c1 = 0
		output = 0
		c2 = 0
		e = 0
		array = []
		at1 = []
		at2 = []
		at3 = []
		arrayequation = []
		equation = ""
		fuckyou=False
		d=0
		d2=False
		reading=False
