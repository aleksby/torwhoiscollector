import os,sys,random,time
from stem import Signal
from stem.control import Controller
import whois,socket
import parser 
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Process, Lock
from math import *

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)

lk_cnt=0
lk_cnttor=Lock()
lk=Lock()
lk_print=Lock()
outfile=""
bad=""
gcnt=0

def safeprint(str):
	global lk_print
        lk_print.acquire()
        print str.encode('utf-8').decode(sys.stdout.encoding)
        lk_print.release()

def newtorident():
	global lk_cnttor
	global lk_cnt
	lk_cnttor.acquire()
	lk_cnt+=1
	if lk_cnt % 150 == 0:
		with Controller.from_port(port = 9051) as controller:
			controller.authenticate()
			controller.signal(Signal.NEWNYM)
			time.sleep(2)
			lk_cnt=0
			#safeprint("New ident")
	lk_cnttor.release()

def wrout(outFileName,outstr):
	global lk
	lk.acquire()
	outFile = open(outFileName, "a")
	try:
		outFile.writelines(outstr.encode('utf-8'))
	except Exception,e:
		safeprint("write file error:"+str(e))
		print str(e)
	outFile.close()	
	lk.release()

def getdata(domain):
	global gcnt
	gcnt+=1
	#time.sleep(random.randint(1,3))
	newtorident()
	domain=domain.replace("\n","")
	run=None
	try:
		ip=socket.gethostbyname(domain)
		#safeprint(ip)
		run=True
	except Exception,e:
		run=False
	#safeprint(domain)
	if run:
		whoisData = whois.whois(domain).query()
	        email=''
	        name=''
	        phone=''
		flag=False
		for i in  whoisData[1].split("\n"):
			#print i
			if "mail:" in i:
				email=i.split(":")[1].strip()
				flag=True
			if ('ame:' in i) and not ('omain' in i):
				name=i.split(":")[1].strip()
				flag=True
			if 'hone:' in i:
				phone=i.split(":")[1].strip()
				flag=True
		out=(domain+","+ip+","+name+","+email+","+phone).replace("\t","")
		if flag:
			#safeprint(out.replace("\n",""))
			wrout(outfile,out.replace("\n","")+"\n")
			safeprint(str(gcnt))
		else:
			wrout(bad,domain.replace("\n","")+"\n")

def main():
	infile=sys.argv[1]
	global outfile
	global bad
	outfile=sys.argv[2]
	bad=sys.argv[3]
	domains=[]
	domains=open(infile).readlines()


	pool = ThreadPool(150)
	results = pool.map(getdata, domains)
	pool.close()
	pool.join()


if __name__ == "__main__":
	main()
