Drop table IF EXISTS node;
Drop table IF EXISTS way;
Drop table IF EXISTS waypoint;
Drop table IF EXISTS nodetag;
Drop table IF EXISTS waytag;

CREATE TABLE node (
	id INTEGER PRIMARY KEY,
	lat REAL,
	lon REAL
);
CREATE TABLE way (
	id INTEGER PRIMARY KEY,
	closed BOOLEAN
);
CREATE TABLE waypoint (
	wayid INTEGER,
	nodeid INTEGER,
	ordinal INTEGER,
	FOREIGN KEY (wayid) REFERENCES way (id) ON DELETE CASCADE, 
	FOREIGN KEY (nodeid) REFERENCES node (id) ON DELETE CASCADE
);
CREATE TABLE nodetag (
	id INTEGER,
	k TEXT,
	v TEXT,
	FOREIGN KEY (id) REFERENCES node (id) ON DELETE CASCADE
);
CREATE TABLE waytag (
	id INTEGER,
	k TEXT,
	v TEXT,
	FOREIGN KEY (id) REFERENCES way (id) ON DELETE CASCADE
);
