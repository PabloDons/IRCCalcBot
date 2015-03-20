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

#getting the password for IRC
passfile=open("password.txt","r")
PASSWORD=str(passfile.read())
passfile.close()

#getting connected
s=socket.socket( )
s.connect((HOST, PORT))
s.send(bytes("NICK %s\r\n" % NICK, "latin1"))
s.send(bytes("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME), "latin1"))
s.send(bytes("JOIN %s\r\n" % (CHANNEL), "latin1"))
s.send(bytes("PRIVMSG NickServ :identify %s \r\n" % (PASSWORD), "latin1"))

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
equation = ""
equation2 = ""
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
	removingfrom=0
	if c1!=2 and e:
		return "Error4! Your quotes where so bad my mom threw up..."
		e=False
	for n in arrayequation:
		if isinstance(n, str) and is_number(n):
			arrayequation[i]=calcexpression(list[int(n)],2)
		i+=1
	i=0
	for n in arrayequation:
		if n=="+" or n=="-" and len(arrayequation)-1!=i:
			at1.append(i)
		elif n=="*" or n=="/" and len(arrayequation)-1!=i:
			at2.append(i)
		elif n=="^":
			at3.append(i)
		elif is_number(n):
			pass
		else:
			e=False
		i+=1
	i=0
	removingfrom=len(arrayequation)
	if e:
		try:
			for n in at3:
				if removingfrom<n:
					n-=removing
				print ("before:",n,at3,removing,removingfrom, arrayequation,"(---3---)")
				if arrayequation[n]=="^":
					arrayequation[n+1]=arrayequation[n-1]**arrayequation[n+1]
					del arrayequation[n]
					del arrayequation[n-1]
					removing+=2
					if removingfrom>n:
						removingfrom=n
				print ("after:",n,at3,removing,removingfrom, arrayequation,"(---3---)")
				i+=1
			i=0
			for n in at2:
				if removingfrom<n:
					n-=removing
				print ("before:",n,at2,removing,removingfrom, arrayequation,"(---2---)")
				if arrayequation[n]=="*":
					arrayequation[n+1]=arrayequation[n-1]*arrayequation[n+1]
					del arrayequation[n]
					del arrayequation[n-1]
					removing+=2
					if removingfrom>n:
						removingfrom=n
				elif arrayequation[n]=="/":
					arrayequation[n+1]=arrayequation[n-1]/arrayequation[n+1]
					del arrayequation[n]
					del arrayequation[n-1]
					removing+=2
					if removingfrom>n:
						removingfrom=n
				print ("after:",n,at2,removing,removingfrom, arrayequation,"(---2---)")
				i+=1
			i=0
			for n in at1:
				if removingfrom<n:
					n-=removing
				print ("before:",n,at1,removing,removingfrom, arrayequation,"(---1---)")
				if n==0:
					if arrayequation[n]=="-":
						arrayequation[n+1]*=-1
						del arrayequation[n]
						removing+=1
						if removingfrom>n:
							removingfrom=n
				else:
					if arrayequation[n]=="-":
						arrayequation[n+1]=arrayequation[n-1]-arrayequation[n+1]
						del arrayequation[n]
						del arrayequation[n-1]
						removing+=2
						if removingfrom>n:
							removingfrom=n
					elif arrayequation[n]=="+":
						arrayequation[n+1]+=arrayequation[n-1]
						del arrayequation[n]
						del arrayequation[n-1]
						removing+=1
						if removingfrom>n:
							removingfrom=n
				i+=1
			i=0
		except (ValueError, ZeroDivisionError):
			e=False
	if e:
		for n in arrayequation:
			output+=n
		return output
	else:
		return "Error2! There occoured an error while calculating"

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
	
	elif getname()=="Hastumer":
		ircsend("Sorry, but you are blacklisted")
	
	elif text.find(cmd + "help") != -1:
		ircsend('syntax: calc "[expression]"')
		ircsend('supported characters:')
		ircsend('"*", "/", "+", "-", "()", "^"')
	
	elif text.find(cmd) != -1:
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
		equation2 = ""
		d=0
		removing=0
		appending=0
		d2=False
		reading=False
		list=[[]]
		for a in text:
			if a == '"' and c1>0:
				c1 += 1
			if c1 == 1:
				array.append(a)
			if a == '"' and c1==0:
				c1 += 1

		equation="".join(array)
		equation=equation.replace("+",",+,")
		equation=equation.replace("-",",-,")
		equation=equation.replace("*",",*,")
		equation=equation.replace("/",",/,")
		equation=equation.replace("(",",(,")
		equation=equation.replace(")",",),")
		equation=equation.replace("^",",^,")
		equation=equation.replace(" ","")
		arrayequation=equation.split(",")
		if equation.find("e")!=-1 and e:
			e=False
			ircsend("Error3! There occoured an error while calculating")
		for a in arrayequation:
			if a=="":
				pass
			elif is_number(a):
				c2=0
				a=float(a)
				list[appending].append(a)
			elif a=="*" or a=="/" or a=="+" or a=="-" or a=="^":
				c2+=1
				list[appending].append(a)
			elif a == "(":
				list.append([])
				appending+=1
				list[appending-1].append(str(appending))
			elif a == ")":
				appending-=1
			elif e:
				e=False
				ircsend("Error5! There occoured an error while calculating")
			if c2>1 and e:
				e=False
				ircsend("Error6! There occoured an error while calculating")
			i+=1
		i=0
		if appending!=0:
			e=False
			ircsend("Error7! Fix your parentheses")
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
		equation2 = ""
		d=0
		removing=0
		appending=0
		d2=False
		reading=False
		list=[[]]
