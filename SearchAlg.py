# This is a Python program for CS 470
# Implementing algorithms for searches

import random

class cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cost = random.randint(10,99)
        self.costtoreach = 0
        self.estimatedcosttogoal = 0
        self.parent = None
    # print
    # equals 
    # overload < > to use sort()
    def __lt__(self, other):
        if(self.costtoreach < other.costtoreach):
            return True
        return False
    
    def printPath(self):
        if(self.parent != None):
            self.parent.printPath()
        print(self.cost)

#creating map
map = []
for x in range (0,7):
    r = []
    for y in range (0,7):
        c = cell(y,x)
        r.append(c)
    map.append(r) 

def printMap(): 
    for r in map:
        for c in r:
            print(c.cost, end = " ")
        print()

def searchList(thisList, item):
    for i in thisList:
        if i == item:
            return True
    return False

def printList(L):
    for i in L:
        print(i.cost, end = " ")
    print()


#intialize 
openlist = []
closedlist = []
goal = map[5][5]

def search():
    start = map[0][3]
    start.costtoreach = start.cost
    start.parent = None
    openlist.append(start)
    while(len(openlist) > 0):
        #Least cost search
        #openlist.sort()
        current = openlist.pop(0)
        if(current == goal):
            print("Success")
            goal.printPath()
            break
        closedlist.append(current)
        # find each neighbor of current 
        # if a neighbor is not on open or closed list
        # add it to the openlist
        if(current.y > 0): #top neighbor
            neighbor = map[current.y-1][current.x]
            #check openlist to see if neighbor is the lower cost neighbor
            if(not searchList(openlist, neighbor) and not searchList(closedlist, neighbor)):
                neighbor.costtoreach = current.costtoreach + neighbor.cost
                neighbor.parent = current
                openlist.append(neighbor)
        if(current.y < len(map[0])-1): #bottom neighbor
            neighbor = map[current.y+1][current.x]
            if(not searchList(openlist, neighbor) and not searchList(closedlist, neighbor)):
                neighbor.costtoreach = current.costtoreach + neighbor.cost
                neighbor.parent = current
                openlist.append(neighbor)
        if(current.x > 0): #left neighbor
            neighbor = map[current.y][current.x-1]
            if(not searchList(openlist, neighbor) and not searchList(closedlist, neighbor)):
                neighbor.costtoreach = current.costtoreach + neighbor.cost
                neighbor.parent = current
                openlist.append(neighbor)
        if(current.x < len(map)-1): #right neighbor
            neighbor = map[current.y][current.x+1]
            if(not searchList(openlist, neighbor) and not searchList(closedlist, neighbor)):
                neighbor.costtoreach = current.costtoreach + neighbor.cost
                neighbor.parent = current
                openlist.append(neighbor)
        
#print map 
printMap()
search()
