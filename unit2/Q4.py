import common, sqlite3, os, sys
DB_ARG = 1
def getDB(dbname):
	# ask for and get db
	# returns T/F for success, db, and cursor
	# also inserts the distance fcn
	if not os.path.exists(dbname):
		print('database [{}] does not exist!\nQuitting...'.format(dbname))
		exit()
	db = sqlite3.connect(dbname)
	db.create_function('dis', 4, common.distance)
	curs = db.cursor()
	EXECUTE('PRAGMA foreign_keys=ON', db, curs)
	return db, curs
def parseAttr(keyVal):
	b = [a.split('=') for a in keyVal]
	for i in b:
		if len(i) != 2 or i[0]=='' or i[1]=='':
			print('Invalid key value pair detected, program quitting')
			
			exit()
	
	return b
def attrKV(lst):
	# return OR_LIST
	r = ''
	c = 0
	for attr in lst:
		c += 1
		r += "(k = '{}' AND v = '{}') OR".format(attr[0], attr[1])
	r = r[:-2]
	if c > 1:
		r = '(%s)'%r
	return r
def EXECUTE(l,db,curs):
	# execute sql without commit
	try:
		curs.execute(l)
	except sqlite3.Error as er:
		print('Error:', l)
def SELECT(s, db, curs):
	EXECUTE(s,db,curs)
	return curs.fetchall()
def COMMIT(db, curs):
	# commit db
	db.commit()
	pass
def closeDB(db, curs):
	# ...
	db.close()
	pass

def Q4():
	# get db and attr
	# find ways with at least one of the attr
	# print 1. # of paths
	#	2. len of longest path
	if len(sys.argv) < 3:
		print("not enough arguments, quitting program")
		exit()
	db, curs = getDB(sys.argv[DB_ARG])
	SQL = open('Q4.sql','r').read()
	ATTR_CUTOFF = DB_ARG + 1
	SQL = SQL.format(OR_LIST = attrKV(parseAttr(sys.argv[ATTR_CUTOFF:])))
	r = SELECT(SQL, db, curs)
	if not r:
		a = 0
		b = 'N\A'
	else:
		a = r[0][0]
		b = r[0][1]
	print('\
Number of paths: {}\n\
Length of longest path:  {} km'.format(b,a))
	closeDB(db, curs)
	
if __name__ == '__main__':
	Q4()
