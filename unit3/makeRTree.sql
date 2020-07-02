CREATE VIRTUAL TABLE rtree_areaMBR USING rtree(
	id, 
	minX, maxX,
	minY, maxY
);
INSERT INTO rtree_areaMBR 
SELECT id, minX, maxX, minY, maxY
FROM areaMBR;
 