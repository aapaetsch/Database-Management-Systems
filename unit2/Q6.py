import sys, os
from Q4 import getDB, parseAttr, EXECUTE, COMMIT, closeDB
from Q5 import Q5_inputhelper, getAndParseNextTSVLine
DB_ARG = 1
TSV_ARG = 2

def Q6():
	# get db and tsv
	# get way from tsv, insert
	if len(sys.argv) != 3:
			print("not enough arguments, format is python3 Q6.py <database.db> <data.tsv>")
			exit()
	db, curs, tsv = Q5_inputhelper()
	t = getAndParseNextTSVLine(tsv)
	while t != ['']:
		try:
			id = int(t[0])
		except Exception:
			print("invalid input in tsv, aborting")
			exit()
		attribs = parseAttr(t[1:])
		SQL = 'INSERT INTO way VALUES({},{})'.format(id, 0)
		EXECUTE(SQL, db, curs)
		
		#print(SQL)
		for attr in attribs:
			k = attr[0]
			v = attr[1]
			SQL = 'INSERT INTO waytag VALUES({},"{}","{}")'.format(id, k, v.strip())
			EXECUTE(SQL, db, curs)
			#print(SQL)
			
		t = getAndParseNextTSVLine(tsv)
		i=0
		closed = False
		try:
			first = int(t[0].strip())
		except Exception:
			print("invalid input in tsv, aborting")
			exit()
		SQL = 'INSERT INTO waypoint VALUES({},{},{})'.format(id, i, first)
		EXECUTE(SQL, db, curs)
		i +=1
		for nid in t:
			try:
				last = int(nid.strip())
			except Exception:
				print("invalid input in tsv, aborting")
				exit()
			SQL = 'INSERT INTO waypoint VALUES({},{},{})'.format(id, i, last)
			EXECUTE(SQL, db, curs)
			#print(SQL)
			i += 1
		closed = first == last
		if closed:
			SQL = 'UPDATE way SET closed = 1 WHERE id = {}'.format(id)
			EXECUTE(SQL, db, curs)
			#print(SQL)
		getAndParseNextTSVLine(tsv)
		t = getAndParseNextTSVLine(tsv)
	
	COMMIT(db, curs)
	tsv.close()
	print('done')
	
if __name__ == '__main__':
	Q6()