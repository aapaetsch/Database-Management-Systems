import sys, random, time, sqlite3

RECTLIST = []
db, curs = -1, -1
def main():
	if len(sys.argv) != 4:
		print("Too few")
		exit()
	dbname = sys.argv[1]
	K = sys.argv[2]
	l = sys.argv[3]
	try:
		K = int(K)
		l = int(l)
	except Exception:
		print("Wrong usage")
		exit()
		
	opendb(dbname)
	type = 'areaMBR' if 'btree' in dbname else 'rtree_areaMBR'
	rangeSQL = '''
		SELECT min(minX), max(maxX), min(minY), max(maxY)
		FROM {}
	'''.format(type)
	rnge = SELECT(rangeSQL, {})[0]
	
	SQL = '''
		SELECT count(*)
		FROM {}
		WHERE minX >=:minX
			AND minY >=:minY
			AND maxX <=:maxX
			AND maxY <=:maxY
	'''.format(type)
	# according to q3.md
	sum = 0
	s = time.time()
	for runs in range(K):
		x, y, w, h = getRandomRect(l, rnge)
		SELECT(SQL, {
			'minX' : x,
			'minY' : y,
			'maxX' : x + w,
			'maxY' : y + h
		})
		
		f = time.time()
		sum += f-s
		s = f
		
	print("{}\t{}\t{}s".format(K, l, sum/K))
	closedb()
	
def getRandomRect(l, rnge):
	r = random.random
	while 1:
		w = l * ((r()*10)+1)
		h = l * ((r()*10)+1)
		
		minX, maxX, minY, maxY = rnge
		
		x = minX + r()*(maxX - minX)
		y = minY + r()*(maxY - minY)
		
		s = "{}_{}_{}_{}".format(x,y,w,h)
		if s in RECTLIST:
			continue
		
		RECTLIST.append(s)
		return x, y, w, h
	
def EXECUTE(l, d):
	# execute sql without commit
	try:
		curs.execute(l,d)
	except sqlite3.Error as er:
		print('Error:', l)
def SELECT(s,d):
	EXECUTE(s,d)
	return curs.fetchall()
def COMMIT():
	# commit db
	db.commit()
def closedb():
	# ...
	db.close()
def opendb(dbname):
	global db, curs
	db = sqlite3.connect(dbname)
	curs = db.cursor()
	

	
	
	
if __name__ == '__main__':
	main()
