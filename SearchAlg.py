# This is a Python program for CS 470
# Implementing search algorithms for pathfinding

import math

# Read in map from file and save values
file = "map.txt"
with open(file) as f:
    lines = f.readlines()

# Intialize values
Width = lines[0][:2]
Height = lines[0][3:5]
StartX = lines[1][:1]
StartY = lines[1][2:3]
GoalX = lines[2][:1]
GoalY = lines[2][2:4]

basemap = lines[3:]
#create copies of basemap
pathmap = [] # will contain found path from start to goal
for n in basemap:
    pathmap.append(n)
exploredmap = [] # will contain all explored cells
for n in basemap:
    exploredmap.append(n)

# A cell represents an individual part of the map
class cell:
    def __init__(self, x, y, cost):
        self.x = x
        self.y = y
        self.cost = cost
        self.costtoreach = 0
        self.estimatedcosttogoal = 0 #heuristic
        self.length = 1
        self.parent = None

    # Sort different based on search used
    def __lt__(self, other):
        #least cost
        #if(self.costtoreach < other.costtoreach):
        #    return True
        #A*
        if((self.costtoreach+self.estimatedcosttogoal) < (other.costtoreach+other.estimatedcosttogoal)):
            return True
        #Greedy
        #if(self.estimatedcosttogoal < other.estimatedcosttogoal):
        #   return True
        
        return False
    
    def printPath(self):
        if(self.parent != None):
            self.parent.printPath()
        print(self.cost)
    
    def fillMapPath(self):
        if(self.parent != None):
            self.parent.fillMapPath()
        pathmap[self.y] = pathmap[self.y][:self.x] + '*' + pathmap[self.y][(self.x)+1:]
    
    def distance1(self):
        # |x-x'| + |y-y'|
        return abs(int(GoalX)-self.x) + abs(int(GoalY)-self.y)
    def distance2(self):
        # sqrt(a^2+b^2)
        return math.sqrt( pow(int(GoalX)-self.x, 2) + pow(int(GoalY)-self.y, 2) )


# Function definitions
def printCostMap(): 
    for r in map:
        for c in r:
            print(c.cost, end = " ")
        print()

def printMap(obj):
    for n in obj:
        print(n, end = "")
    print()

def searchList(thisList, item):
    for i in thisList:
        if i == item:
            return True
    return False

def printList(L):
    for i in L:
        #print(i.costtoreach, end = " ") # least cost 
        print(i.costtoreach+round(i.estimatedcosttogoal, 2), end = " ") # A*
        #print(round(i.estimatedcosttogoal, 2), end = " ") # greedy
    print()

def findCost(terrain):
    switcher={
        'R':1,  #road 
        'f':2,  #field
        'F':4,  #forest
        'h':5,  #hills
        'r':7,  #river
        'M':10, #mountains
        'W':333   #water
    }
    return switcher.get(terrain)

def avg():
    return (1+2+4+5+7+10)/6

def maxval(a, b):
    if(a>=b):
        return a
    return b


#creating map
map = []
for y in range (0,int(Height)):
    r = []
    for x in range (0,int(Width)):
        cost = findCost(basemap[y][x])
        c = cell(x,y, cost)
        r.append(c)
    map.append(r) 

#intialize 
openlist = []
closedlist = []
goal = map[int(GoalY)][int(GoalX)]

def search():
    start = map[int(StartY)][int(StartX)]
    start.costtoreach = start.cost
    start.parent = None
    start.estimatedcosttogoal = maxval(start.distance1(), start.distance2()) * avg() # heuristic
    openlist.append(start)
    while(len(openlist) > 0):
        # Breadth-first no sorting
        # Least cost sort by total cost
        # A* sort by total cost + estimated cost
        # Greedy sort by estimated cost (heuristic)
        openlist.sort()
        current = openlist.pop(0)

        #check if the goal has been reached
        if(current == goal):
            #goal.printPath()
            goal.fillMapPath()
            print("Total Cost: ", goal.costtoreach)
            print("Total Length: ", goal.length)
            print()
            print("Open List:")
            printList(openlist)
            print()
            break
        #mark on explored map
        exploredmap[current.y] = exploredmap[current.y][:current.x] + '-' + exploredmap[current.y][(current.x)+1:]
        closedlist.append(current) #add to closed list
        # Find each neigbor of current and add to openlist if hasn't been searched yet
        if(current.y > 0): #top neighbor
            neighbor = map[current.y-1][current.x]
            #check if neighbor is water and place on closed list
            if(neighbor.cost == 333):
                closedlist.append(neighbor)
            #check openlist to see if neighbor is the lower cost neighbor
            if(not searchList(openlist, neighbor) and not searchList(closedlist, neighbor)):
                neighbor.costtoreach = current.costtoreach + neighbor.cost
                neighbor.estimatedcosttogoal = maxval(neighbor.distance1(), neighbor.distance2()) * avg() 
                neighbor.length = current.length + neighbor.length
                neighbor.parent = current
                openlist.append(neighbor)
        if(current.y < len(map)-1): #bottom neighbor
            neighbor = map[current.y+1][current.x]
            #check if neighbor is water and place on closed list
            if(neighbor.cost == 333):
                closedlist.append(neighbor)
            if(not searchList(openlist, neighbor) and not searchList(closedlist, neighbor)):
                neighbor.costtoreach = current.costtoreach + neighbor.cost
                neighbor.estimatedcosttogoal = maxval(neighbor.distance1(), neighbor.distance2()) * avg() 
                neighbor.length = current.length + neighbor.length
                neighbor.parent = current
                openlist.append(neighbor)
        if(current.x > 0): #left neighbor
            neighbor = map[current.y][current.x-1]
            #check if neighbor is water and place on closed list
            if(neighbor.cost == 333):
                closedlist.append(neighbor)
            if(not searchList(openlist, neighbor) and not searchList(closedlist, neighbor)):
                neighbor.costtoreach = current.costtoreach + neighbor.cost
                neighbor.estimatedcosttogoal = maxval(neighbor.distance1(), neighbor.distance2()) * avg() 
                neighbor.length = current.length + neighbor.length
                neighbor.parent = current
                openlist.append(neighbor)
        if(current.x < len(map[0])-1): #right neighbor
            neighbor = map[current.y][current.x+1]
            #check if neighbor is water and place on closed list
            if(neighbor.cost == 333):
                closedlist.append(neighbor)
            if(not searchList(openlist, neighbor) and not searchList(closedlist, neighbor)):
                neighbor.costtoreach = current.costtoreach + neighbor.cost
                neighbor.estimatedcosttogoal = maxval(neighbor.distance1(), neighbor.distance2()) * avg() 
                neighbor.length = current.length + neighbor.length
                neighbor.parent = current
                openlist.append(neighbor)

#Driver Code
#printcostMap()
print("Starting Map:")
printMap(basemap)
search()
print("Path Found:")
printMap(pathmap)
print("Explored Map:")
printMap(exploredmap)
