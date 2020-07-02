import sys, re, sqlite3, os, time
import common as c
import math as m
#Problems with values that contain ;
db = None
cursor = None

def ex(l, echo=False):
	try:
		cursor.execute(l)
	except sqlite3.Error as er:
		print('Error:', er)


def D(WAY):
	ex('''
	WITH a(lat,lon,ordinal, closed)
	AS
	(SELECT n.lat, n.lon,wp.ordinal, w.closed
	FROM way w
	NATURAL JOIN waypoint wp, node n
	WHERE n.id = wp.nodeid 
	AND w.id = wp.wayid
	AND w.id = {}
	ORDER BY wp.ordinal)
	SELECT SUM(dis(x.lat,y.lat,x.lon,y.lon)),x.closed
	FROM a x, a y
	where x.ordinal+1 = y.ordinal
	'''.format(WAY))
	length = cursor.fetchall()
	
	return length
	
	
def main():
	global db, cursor
	dbName = str(sys.argv[1])
	if len(sys.argv) != 3:
		print("Invalid number of arguments entered:",len(sys.argv),"\nPlease enter at least 3, includes the program name")
		return 0


	db = sqlite3.connect(dbName)
	cursor = db.cursor()
	ex('PRAGMA foreign_keys=ON')
	#distance function used in 1
	db.create_function("dis",4,c.distance)
	try:
		a = int(sys.argv[2])
	except Exception:
		print("not a valid way ID")
		exit()
	length = D(a)
	length[0] = list(length[0])
	if length[0][0] == None:
		print("This way either doesnt exist or has only 1 point")
		db.close()
		exit()
	if length[0][1] == 1:
		print("The length of the perimeter of path",sys.argv[2],"is",length[0][0],"km")
	else:
		print("The length of the path",sys.argv[2],"is",length[0][0],"km")
	db.close()
	
main()

