import sys, re, sqlite3, os, time
import common as c
import math as m
db = None
cursor = None

def checkInDb(node,node2):
	ex('''
	SELECT dis(n1.lat,n2.lat,n1.lon,n2.lon)
	FROM node n1, node n2
	WHERE n1.id = {} 
       AND n2.id = {}'''.format(int(node),int(node2)))
	results = cursor.fetchall()

	return results

def ex(l, echo=False):
	try:
		cursor.execute(l)
	except sqlite3.Error as er:
		print('Error:', l)


def main():
	global db, cursor
	if len(sys.argv) != 4:
		print("Invalid number of arguments entered:",len(sys.argv),"\nPlease enter 4, includes the program name")
		return 0
	else:
		fileName, dbName, node1, node2 = sys.argv
		try:
			int(node1)
			int(node2)
		except Exception:
			print("At least one of the nodes contains a non integer value")
			return 0
	db = sqlite3.connect(dbName)
	cursor = db.cursor()
	ex('PRAGMA foreign_keys=ON')
	db.create_function("dis",4,c.distance)
	a = checkInDb(node1,node2)
	if len(a) != 1:
		print("At least 1 of the nodes is not in the database")
	else:
		print("Distance between nodes",node1,node2,"is",a[0][0],"km")
	
	
	
	db.close()

main()
