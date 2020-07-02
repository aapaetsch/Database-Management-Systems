
def main():
	print('''CREATE TABLE IF NOT EXISTS areaMBR(
	id INTEGER,
	minX REAL,
	maxX REAL,
	minY REAL,
	maxY REAL,
	PRIMARY KEY(id));

with wpCoords(id, x, y) as (select w.id, x,y
from way w,waypoint wp, nodeCartesian nc 
where w.closed = 1
and w.id = wp.wayid
and nc.id = wp.nodeid)  
insert into areaMBR
select id, min(x), max(x), min(y), max(y)
from wpCoords
group by id;

	''')
main()
