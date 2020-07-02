SELECT count(*) as num_nodes
FROM node;
SELECT count(*) as num_ways
FROM way;
SELECT count(*) as closed_ways
FROM way
WHERE closed = 1;
SELECT *
FROM nodetag t, node n
WHERE t.id = n.id
LIMIT 5;