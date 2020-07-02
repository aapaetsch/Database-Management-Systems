import sys, os
from Q4 import getDB, parseAttr, EXECUTE, COMMIT, closeDB
DB_ARG = 1
TSV_ARG = 2

def getTSV(fname):
	# ask for and get db
	# returns T/F for success, tsv in list format
	if not os.path.exists(fname):
		print('TSV file [{}] does not exist!\nQuitting...'.format(fname))
		exit()
	f = open(fname, 'r', encoding='utf-8')
	return f
def getAndParseNextTSVLine(tsv):
	# tsv is a file
	a = tsv.readline().split('\t')
	return a

def Q5_inputhelper():
	# return db, curs, tsv
	# quit if problem
	# ask for files
	db, curs = getDB(sys.argv[DB_ARG])
	tsv = getTSV(sys.argv[TSV_ARG])
	return db, curs, tsv
def Q5():
	# get db and tsv
	# get nodes from tsv, insert
	if len(sys.argv) != 3:
		print("not enough arguments, format is python3 Q5.py <database.db> <data.tsv>")
		exit()
	db, curs, tsv = Q5_inputhelper()
	t = getAndParseNextTSVLine(tsv)
	while t != ['']:
		try:
			id = int(t[0])
			lat = float(t[1])
			lon = float(t[2])
		except Exception:
			print("invalid input in tsv, aborting")
			exit()
		attribs = parseAttr(t[3:])
		
		SQL = 'INSERT INTO node VALUES({},{},{})'.format(id, lat, lon)
		EXECUTE(SQL, db, curs)
		
		#print(SQL)
		for attr in attribs:
			k = attr[0]
			v = attr[1]
			SQL = 'INSERT INTO nodetag VALUES({},"{}","{}")'.format(id, k, v.strip())
			EXECUTE(SQL, db, curs)
			#print(SQL)
			
		t = getAndParseNextTSVLine(tsv)
	
	COMMIT(db, curs)
	closeDB(db, curs)
	tsv.close()
	print('done')

if __name__ == '__main__':
	Q5()