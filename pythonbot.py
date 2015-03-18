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
s.send(bytes("PRIVMSG NickServ :identify %s \r\n" % (password), "latin1"))

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
appending=0
removing=0
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
def calcexpression(arrayequation,c1):
	i=0
	output=0
	e=True
	array=[]
	at1 = []
	at2 = []
	at3 = []
	removing=0
	if c1!=2:
		return "Error! Your quotes where so bad my mom threw up..."
		e=False
	for n in arrayequation:
		if isinstance(n, str) and is_number(n):
			arrayequation[i]=calcexpression(list[int(n)],2)
		i+=1
	i=0
	for n in arrayequation:
		if n=="+" or n=="-":
			at1.append(i)
		elif n=="*" or n=="/":
			at2.append(i)
		elif is_number(n):
			pass
		else:
			e=False
		i+=1
	i=0
	for n in at2:
		n-=removing
		if arrayequation[n]=="*" and is_number(arrayequation[n+1]):
			arrayequation[n+1]=arrayequation[n-1]*arrayequation[n+1]
			del arrayequation[n]
			del arrayequation[n-1]
			removing+=2
		elif arrayequation[n]=="/" and is_number(arrayequation[n+1]):
			if e and arrayequation[n+1]==0:
				e=False
			else:
				arrayequation[n+1]=arrayequation[n-1]/arrayequation[n+1]
				del arrayequation[n]
				del arrayequation[n-1]
				removing+=2
		i+=1
	i=0
	removing=0
	for n in at1:
		n-=removing
		if arrayequation[n]=="-" and is_number(arrayequation[n+1]):
			if i==0:
				arrayequation[n+1]*=-1
				del arrayequation[n]
				removing+=1
			else:
				arrayequation[n+1]=arrayequation[n-1]-arrayequation[n+1]
				del arrayequation[n]
				del arrayequation[n-1]
				removing+=2
		elif arrayequation[n]=="+" and is_number(arrayequation[n+1]):
			arrayequation[n+1]+=arrayequation[n-1]
			del arrayequation[n]
			del arrayequation[n-1]
			removing+=2
		i+=1
	i=0
	print (arrayequation)
	if e:
		for n in arrayequation:
			output+=n
		return output
	else:
		return "Error! There occoured an error while calculating"

#what your bot does after its up and running
while 1:
	text = s.recv(2040).decode("latin1") #gets data from irc and decodes it to "latin1"
	if text.find('PING') != -1:		 #confirms connection to IRC
		s.send(bytes('PONG ' + text.split() [1] + '\r\n', "latin1"))
#quit bot when you type your cmd + quit + password(without space or +)
	if text.find(cmd + "quit") != -1:
		if getname()==MASTER:
			ircquit()
			break
	
	if text.find(cmd + "help") != -1:
		ircsend('syntax: calc "[expression]"')
		ircsend('supported characters:')
		ircsend('"*", "/", "+", "-"')
	
	if text.find(cmd) != -1:
		if text=="quit":
			e=False
		if text=="help":
			e=False
		c1=0
		list=[[]]
		appending=0
		i=0
		i2=0
		for a in text:
			if a == '"' and c1==1:
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
		equation=equation.replace("(",",(,")
		equation=equation.replace(")",",),")
		equation=equation.replace(" ","")
		arrayequation=equation.split(",")
		for a in arrayequation:
			if is_number(a):
				a=float(a)
			if a=="":
				pass
			elif a == "(":
				list.append([])
				appending+=1
				list[appending-1].append(str(appending))
			elif a == ")":
				appending-=1
			else:
				list[appending].append(a)
			i+=1
		i=0
		if appending!=0:
			e=False
			ircsend("Error! Fix your parentheses")
		if e:
			ircsend(calcexpression(list[0],c1))

		i=0
		array=[]
		c1 = 0
		output = 0
		c2 = 0
		e=True
		array = []
		at1 = []
		at2 = []
		at3 = []
		arrayequation = []
		equation = ""
		d=0
		removing=0
		appending=0
		d2=False
		reading=False
		list=[[]]
