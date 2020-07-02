import sys, re, sqlite3, os, time
import math as m
import common as c
#Problems with values that contain ;
db = None
cursor = None

def ex(l, echo=False):
	try:
		cursor.execute(l)
	except sqlite3.Error as er:
		print('Error:', er)

def formatList(keyVal):

	b = [a.split('=') for a in keyVal]
	for i in b:
		if len(i) != 2 or i[0]=='' or i[1]=='':
			print('Invalid key value pair detected, program quitting')
			
			exit()
	
	return b
	
		

def find(keyVal):
	
	statement = ''
	length = len(keyVal)
	
	if length != 1:
		for i in range(length):
			statement +='(k = "{}" AND v = "{}")'.format(str(keyVal[i][0]),str(keyVal[i][1]))
			if i != length-1:
				statement += ' OR '
	else:
		statement = 'k = "{}" and v = "{}"'.format(str(keyVal[0][0]),str(keyVal[0][1]))

	ex('''
		with nodes1(n)
		as 
		(SELECT DISTINCT id 
		FROM nodetag
		WHERE {}),
		nodes(n1,n2) as 
		(select DISTINCT node1.n,node2.n
		from nodes1 node1
		cross join nodes1 node2
		where node1.n < node2.n)
		
		select max(dis(a.lat,b.lat,a.lon,b.lon)), count(distinct nodes.n2)+1
		from nodes,node a, node b
		where nodes.n1 = a.id
		and nodes.n2 = b.id'''.format(statement))
	#+1 to the count as there is 1 node n1 that is not in n2 
	#and 1 node n2 that is not in n1

	nods = cursor.fetchall()

	return nods
	
	
def main():
	global db, cursor
	dbName = str(sys.argv[1])
	if len(sys.argv) <= 2:
		print("Invalid number of arguments entered:",len(sys.argv),"\nPlease enter at least 3, includes the program name")
		return 0
	
	key_Val = formatList(sys.argv[2:])	
	
	db = sqlite3.connect(dbName)
	cursor = db.cursor()
	ex('PRAGMA foreign_keys=ON')
	#distance function used in 1
	db.create_function("dis",4,c.distance)

	nodes = find(key_Val)
	
	db.close()

	print("Maximum Pairwise Distance:",nodes[0][0],'km')
	print("Total nodes observed:",nodes[0][1])
	
main()