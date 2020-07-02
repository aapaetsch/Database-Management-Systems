import sys, re, sqlite3, os, time
import math as m

def main():
	print('''CREATE TABLE IF NOT EXISTS nodeCartesian(
	id INTEGER,
	x REAL,
	y REAL,
	PRIMARY KEY(id));''')
	print('''with origin(oLat,oLon) as
		(SELECT min(lat),min(lon)from node)
	INSERT INTO nodeCartesian
		SELECT id, (lon - oLon)*67137,(lat-oLat)*11286
		FROM node,origin;''')


main()
