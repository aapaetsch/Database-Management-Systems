WITH a(id,lat,lon,ordinal) AS (
	SELECT w.id, n.lat, n.lon, wp.ordinal 
	FROM way w 
		NATURAL JOIN waypoint wp, node n, waytag wt 
	WHERE n.id = wp.nodeid 
		AND w.id = wp.wayid 
		AND w.id = wt.id 
		AND {OR_LIST} ) 
, distances(dist) AS(
SELECT  sum(dis(x.lat,y.lat,x.lon,y.lon)) as dist
from a x, a y 
where x.ordinal+1 = y.ordinal 
	and x.id = y.id 
group by x.id)
SELECT max(dist), count(*)
FROM distances;