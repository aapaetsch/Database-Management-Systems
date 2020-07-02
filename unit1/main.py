import re, sqlite3, os, time, sys, time

db = None
cursor = None
pline = 0
def printPercent(n):
	global pline
	
	a = "{0:.2f} % done".format(100*n)
	print(a,end='\r')
escapeDict = {
	'&amp;'	:'&',
	'&lt;':	'<',
	'&gt;'	:'>',
	'&quot;':	'"',
	'&apos;'	:"''",
}
def multiple_replace(dict, text):
	# Create a regular expression  from the dictionary keys
	regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))

	# For each match, look-up corresponding value in dictionary
	return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text) 		
def execute(l, echo=False):
	try:
		cursor.execute(l)
	except Exception:
		print('Error:', l)
		#time.sleep(2)
	#if echo: print(l.strip())
	#db.commit()	
def main():
	global db, cursor
	dbname = input("Enter the name of the database that you wish to create (do not add .db at the end) > ")
	dbname = dbname+".db"
	
	db = sqlite3.connect(dbname)
	cursor = db.cursor()
	
	df = open('edmonton.sql','r')
	for cmd in df.read().split(';'):
		#print(cmd)
		db.execute(cmd)
	df.close()
	
	
	db.commit()
	enc = 'utf-8'
	file = input("Enter the name of the osm file that you wish to open(Do not add .osm at the end) > ")
	file = file+".osm"
		
	f = open(file, 'r', encoding = enc)
	
	startTime = time.time()
	statinfo = os.stat(file)
	print("The input file is {} bytes.\n*Percentage is not fully accurate!".format(int(statinfo.st_size)))
	tsize = int(statinfo.st_size)
	sizenow = 0
	avgbytes = 1.0
	i = 0
	igap = 10000
	execute("PRAGMA foreign_keys")
	#execute("foreign_keys=on;")
	while 1: # node loop
		if(i%igap==0):
			printPercent(sizenow/tsize)
		line = f.readline()
		#print(line)
		if line == '':
			break
		a = re.findall("<node (.*?)>", line)
		if len(a) > 0:
			i += 1
			sizenow += len(line)*avgbytes
			a = a[0]
			if a[-1] == '/':
				#print("...NO TAGS...")
				d = nodeSeparator(a[:-1], echo=False)
				execute('''
INSERT INTO node values (
	{}, 
	{}, 
	{})'''.format(int(d['id']), float(d['lat']),float(d['lon'])))
				continue
			else:
				# its has tags
				d = nodeSeparator(a, echo=False)
				execute('''
INSERT INTO node values (
	{}, 
	{}, 
	{})'''.format(int(d['id']), float(d['lat']),float(d['lon'])))
				#print("...TAGS...")
				while 1:
					line = f.readline()
					b = re.findall("<tag (.*?)/>", line)
					if(len(b) > 0):
						sizenow += len(line)*avgbytes
						b = b[0]
						e = nodeTagSeparator(b, echo=False)
						execute('''
INSERT INTO nodetag values (
	{}, 
	'{}', 
	'{}')'''.format(int(d['id']), e['k'],e['v']))
					else:
						break
				continue
				
				
	print("Got all nodes!")		
				
	f.close()
	f = open(file, 'r', encoding = enc)
	while 1: # way loop
		if(i%igap==0):
			printPercent(sizenow/tsize)
		line = f.readline()
		if line == '':
			break
		a = re.findall("<way (.*?)>", line)
		if len(a) > 0:
			i += 1
			sizenow += len(line)*avgbytes
			a = a[0]
			# its has tags
			d = waySeparator(a, echo=False)
			d['closed'] = 0
			execute('''
INSERT INTO way values (
	{}, 
	{})'''.format(int(d['id']), d['closed']))
			line = f.readline()
			c = re.findall("<nd (.*?)/>", line)
			first = wayPointSeparator(c[0], echo=False)
			count = 0
			execute('''
INSERT INTO waypoint values (
	{}, 
	{}, 
	{})'''.format(int(d['id']), int(first['ref']),count))
			second = None
			while 1:
				line = f.readline()
				c = re.findall("<nd (.*?)/>", line)
				
				if(len(c) > 0):
					sizenow += len(line)*avgbytes
					c = c[0]
					second = wayPointSeparator(c, echo=False)
					count += 1
					#print(c)
					execute('''
INSERT INTO waypoint values (
	{}, 
	{}, 
	{})'''.format(int(d['id']), int(second['ref']),count))
					
					
					continue
				
				b = re.findall("<tag (.*?)/>", line)
				if(len(b) > 0):
					sizenow += len(line)*avgbytes
					b = b[0]
					e = wayTagSeparator(b, echo=False)
					execute('''
INSERT INTO waytag values (
	{}, 
	'{}', 
	'{}')'''.format(int(d['id']), e['k'],e['v']))
				else:
					break
			if second['ref'] == first['ref']:
				# print('WAY {} is closed!\nAnd had {} points',d['id'], count+1)
				d['closed'] = 1
				execute('''
UPDATE way SET closed = {} WHERE id = {}'''.format(d['closed'], int(d['id'])))
				
		
	print("Got all ways!")		
	

	f.close()
	df = open('triggers.sql','r')
	for cmd in df.read().split(':::'):
		#print(cmd)
		execute(cmd)
	df.close()
	db.commit()
	db.close()	
	printPercent(1)
	print('The process took {} seconds'.format(time.time()-startTime))
def waySeparator(line, echo = False):
	c = attribSeparator(line)
	return c
def wayPointSeparator(line, echo = False):
	c = attribSeparator(line)
	return c
def wayTagSeparator(line, echo = False):
	return tagSeparator(line, echo)
	
def nodeTagSeparator(line, echo = False):
	return tagSeparator(line, echo)
def tagSeparator(line, echo = False):
	c = attribSeparator(line)
	if 'v' in c:
		c['v'] = multiple_replace(escapeDict, c['v'])
	return c
	
def attribSeparator(line):
	c = re.findall(r'([^\s]+)="(.*?)"',line)
	return dict(c)
	
def nodeSeparator(line, echo = False):
	c = attribSeparator(line)
	return c
	
main()
