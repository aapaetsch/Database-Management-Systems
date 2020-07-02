DROP TRIGGER IF EXISTS waypoint_duplicates;
:::
DROP TRIGGER IF EXISTS node_duplicate;
:::
DROP TRIGGER IF EXISTS waypoint_deletion_update_open;
:::
CREATE TRIGGER waypoint_duplicates
BEFORE INSERT ON waypoint
WHEN new.ordinal IN (SELECT ordinal FROM waypoint WHERE wayid =new.wayid)
OR new.ordinal >(SELECT COUNT(*) FROM waypoint WHERE wayid = new.wayid)
BEGIN
SELECT RAISE(ABORT,'Invalid waypoint entered');
END;
:::
CREATE TRIGGER waypoint_closed
BEFORE INSERT ON waypoint
WHEN new.nodeid IN (SELECT nodeid FROM waypoint WHERE wayid = new.wayid)
BEGIN
UPDATE way SET closed=1 WHERE id = new.nodeid;
END;
:::
CREATE TRIGGER waypoint_deletion_update_open
AFTER DELETE ON waypoint
WHEN 
	(old.ordinal = (SELECT MAX(ordinal) 
		FROM waypoint 
		WHERE wayid = old.wayid)
	or old.ordinal = (SELECT MIN(ordinal) 
		FROM waypoint 
		WHERE wayid = old.wayid))
	and (SELECT sum(closed) 
		FROM way 
		WHERE id = old.wayid) = 1
BEGIN
UPDATE way SET closed=0 WHERE id = old.wayid;
END;
