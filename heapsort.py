#!/bin/env python
# Python version 2.7
# http://sourceforge.net/projects/matplotlib/files/matplotlib/matplotlib-1.1.0/
# http://sourceforge.net/projects/numpy/files/NumPy/1.6.1/
import matplotlib.pyplot as plt
# easy_install networkx
# NetworkX 1.6
import networkx as nx
import math
import time

counter = 0
G = nx.Graph()
treePosCache = None

class Node(object):
	__x = None
	__y = None
	__stepx = 20
	__stepy = 10
	__level = 0
	__key = None
	__right = None
	__left = None
	__picture = {}
	
	def __init__(self, key, x, y, level):
		self.__x = x
		self.__y = y
		self.__level = level
		self.__key = key
		self.__right = None
		self.__left = None
		self.__picture[key] = self.getCoords()
	
	def addRightChild(self, key, level):
		if self.__right != None:
			raise Exception
		self.__right = Node(key,
							self.__x + self.__stepx*(5-self.__level), 
							self.__y - self.__stepy,
							level)
		self.__picture[key] = self.__right.getCoords()
		return self.__right
	
	def addLeftChild(self, key, level):
		if self.__left != None:
			raise Exception
		self.__left = Node(	key,
							self.__x - self.__stepx*(5-self.__level), 
							self.__y - self.__stepy,
							level)
		self.__picture[key] = self.__left.getCoords()
		return self.__left
		
	def getRightChild(self):
		return self.__right
	
	def getLeftChild(self):
		return self.__left
		
	def getCoords(self):
		return (self.__x, self.__y)
		
	def getPicture(self):
		return self.__picture		
	
def swap(A, i, j):	
	A[i], A[j] = A[j], A[i]
	G.node[i]['color'] = G.node[j]['color'] = 'y'
	drawHeap()
	G.node[i]['label'], G.node[j]['label'] = G.node[j]['label'], G.node[i]['label']
	drawHeap()
	G.node[i]['color'] = G.node[j]['color'] = 'r'
	
def heapify(A, i, size):
	maxindex = i
	l = 2*i + int(i == 0)
	r = 2*i + int(i == 0) + 1
	
	if l < size and A[l] > A[maxindex]:
		maxindex = l
		
	if r < size and A[r] > A[maxindex]:
		maxindex = r 
		
	if i != maxindex:
		swap(A, i, maxindex)
		heapify(A, maxindex, size)

def buildHeap(A):
	for i in xrange(int(len(A)/2), -1, -1):
		heapify(A, i, len(A))

def heapSort(A):
	fillWithVertices(A)
	drawLine(A)
	fillWithEdges(A)
	buildHeap(A)
	size = len(A)
	print A
	for i in range(0, len(A)-1):
		swap(A, 0, size-1)
		print A
		size -= 1
		G.node[size]['color'] = 'w'
		heapify(A, 0, size)
		print A
	G.remove_edges_from(G.edges())
	drawLine(A)

def getLinePos(count):
	Line = {}
	for i in range(0, count):
		Line[i] = (i*10, 0)
	return Line
	
def getTreePos(count):
	collection = {}
	root = Node(0, 50, 0, 0)
	collection[0] = root
	
	for i in range(1, count+1):
		if i != 1:			
			p = int(math.floor(i/2))
			parent = collection[p-1]
			level = int(math.floor(math.log(i, 2)))
			if i % 2 != 0:
				collection[i-1] = parent.addRightChild(i-1, level)
			else:
				collection[i-1] = parent.addLeftChild(i-1, level)	
				
	return root.getPicture()

def getColors():
	Colors = []
	for i in range(0, len(G)):
		Colors.append(G.node[i]['color'])
	return Colors
	
def fillWithVertices(Arr):
	global G
	if(len(G) == 0):
		for i in range(0, len(Arr)):
			G.add_node(i, label=Arr[i], color='r')
	
def fillWithEdges(Arr):
	global G
	for i in range(1, len(Arr)+1):
		if i != 1:			
			p = int(math.floor(i/2))
			G.add_edge(i-1, p-1)
				
def getLabelMapping():
	global G
	Dict = {}
	for i in range(0, len(G)):
		Dict[i] = str(G.node[i]['label'])
	return Dict
	
def drawHeap():
	global counter, treePosCache
	if not treePosCache:
		treePosCache = getTreePos(len(Arr))

	nx.draw(G, 
			pos=treePosCache, 
			labels=getLabelMapping(), 
			node_color=getColors(),
			node_size=600
			)
	plt.savefig("heap%02d.png" % counter)
	counter += 1
	plt.clf()
	
def drawLine(A):
	global counter	
	nx.draw(G, 
			pos=getLinePos(len(Arr)), 
			labels=getLabelMapping(),
			node_size=600
			)
	plt.savefig("heap%02d.png" % counter)
	counter += 1
	plt.clf()
	
file = open("input.txt")
Arr = [int(x) for x in file.read().strip().split(" ")]

#Arr = [3, 5, 8, 10, 2, 3, 3, 4, 5]
#Arr = [3, 5, 8, 0]
heapSort(Arr)
