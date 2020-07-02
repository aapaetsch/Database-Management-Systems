# q5
import sys
from q4 import opendb, closedb, SELECT
point = -1

def main():
	global point
	a =sys.argv
	if len(sys.argv) != 5:
		print("Too few")
		exit()
	dbname = a[1]
	x = a[2]
	y = a[3]
	k = a[4]
	try:
		k = int(k)
		x = float(x)
		y = float(y)
	except Exception:
		print("Wrong usage")
		exit()
	
	
	# do error checks
	
	opendb(dbname)
	
	point = Point(int(x), int(y))
	
	root = getNodebyID(1)
	nearest_k = [Branch(-1, 10000000 ,-1) for i in range(k)]
	NNSearch_k(root, point, nearest_k)
	for b in nearest_k:
		if b.id != -1:
			print("{}\t{}".format(b.id, b.dist))
	closedb()
	
BRANCH_SQL = '''
	SELECT rtreenode(2, data) 
	FROM rtree_areaMBR_node 
	WHERE nodeno=:id
'''


	
def getNodebyID(id):
	r = SELECT(BRANCH_SQL,{'id':id})
	return Node(len(r), None, id)
	
	
class Point:
	def __init__(self, x,y):
		self.x = x
		self.y = y
		
class Rect:
	def __init__(self, mn, mx):
		self.min = mn
		self.max = mx
	
class Node:
	def __init__(self, count, parent, id):
		self.id = id
		self.count = count
		self.parent = parent

	def getBranchList(self, i):
		pass
	def getNew(self, blist_i):
		pass
	def isLeaf(self):
		r = SELECT(BRANCH_SQL,{'id':self.id})
		if len(r) > 0 \
		  and len(SELECT(BRANCH_SQL,{'id':r[0][0]})) == 0:
			return True
			
		return False
		
class Branch:
	def __init__(self, id, dist, rect):
		self.id = id
		self.dist = dist
		self.rect = rect
	
	
	
def minDist(p, rect):
	r = Point(p.x, p.y)
	# need to check, could be switched
	s = rect.min
	t = rect.max
	
	if p.x < s.x:
		r.x = s.x
	elif p.x > t.x:
		r.x = t.x
		
	if p.y < s.y:
		r.y = s.y
	elif p.y > t.y:
		r.y = t.y
		
	return (p.x - r.x)**2 + (p.y - r.y)**2
	
		
def minMaxDist(p, rect):
	s = rect.min
	t = rect.max
	
	rm = Point(t.x, t.y)
	rM = Point(t.x, t.y)
	mid = Point((s.x+t.x)/2, (s.y+t.y)/2)
	
	if p.x <= mid.x:
		rm.x = s.x
	if p.y <= mid.y:
		rm.y = s.y
		
	if p.x >= mid.x:
		rM.x = s.x
	if p.y >= mid.y:
		rM.y = s.y
		
	a = (p.x - rm.x)**2 + (p.y - rM.y)**2
	b = (p.y - rm.y)**2 + (p.x - rM.x)**2
	
	return min(a,b)
	
	
def objectDist(p, rect):
	s = rect.min
	t = rect.max
	
	mid = Point((s.x+t.x)/2, (s.y+t.y)/2)
	
	return (p.x - mid.x)**2 + (p.y - mid.y)**2
def genBranchList(point, node):
	r = SELECT(BRANCH_SQL,{'id':node.id})
	leaves = []
	for i in range(len(r)):
		print(r)
		mx = Point(r[2], r[4])
		mn = Point(r[1], r[3])
		rect = Rect(mn, mx)
		dist = objectDist(point, rect)
		id = r[0]
		leaves.append(id, dist, rect)
	return leaves
def sortBranchList_key(b):
	return minDist(point, b.rect)
def pruneBranchList_down(node, point, nearest, branchList):
	prune_strategy_1(node, point, nearest, branchList)
	prune_strategy_2(node, point, nearest, branchList)
	
def pruneBranchList_up(node, point, nearest, branchList):
	rune_strategy_2(node, point, nearest, branchList)
	rune_strategy_3(node, point, nearest, branchList)
	
def prune_strategy_1(node, point, nearest, branchList):
	prune_helper(
		minDist, minMaxDist, 
		node, point, nearest, branchList)
	
def prune_strategy_2(node, point, nearest, branchList):
	prune_helper(
		objectDist, minMaxDist, 
		node, point, nearest, branchList)
		
def prune_strategy_3(node, point, nearest, branchList):
	pprune_helper(
		minDist, objectDist,
		node, point, nearest, branchList)
	
def prune_helper(f_1, f_2, node, point, nearest, branchList):
	'''
		delete the item in branchList 
		if f_1 metric is > f_2 metric of another item 
		in branchList
	'''
	last = len(branchList)
	i = 0
	while i < last:
		m_i = f_1(point, branchList[i].rect)
		toDel = False
		for j in range(len(branchList)):
			if i != j:
				m_j = f_2(point, branchList[j].rect)
				if m_i > m_j:
					toDel = True
					break
		if toDel:
			del branchList[i]
			last = len(branchList)
		else:
			i += 1
	

def NNSearch_k(node, point, nearest_k):
	if node.isLeaf():
		leaves = genBranchList(point, node)
			
		for i in range(len(leaves)):
			rect = leaves[i].rect
			dist = leaves[i].dist
			id = leaves[i].id
			for j in range(len(nearest_k)):
				n = nearest_k[j]
				if dist < n.dist:
					n.dist = dist
					n.rect = rect
					n.id = id
					break
	else:
		branchList = genBranchList(point, node)
		branchList.sort(key = sortBranchList_key)
		
		pruneBranchList_down(node, point, nearest_k, branchList)
		last = len(branchList)
		i = 0
		while i < last:
			newNode = getNodebyID(branchList[i].id)
			NNSearch_k(newNode, point, nearest_k)
			pruneBranchList_up(node, point, nearest_k, branchList)
			last = len(branchList)
			i+=1
			
			
		return branchList
			
	
	
	
main()
