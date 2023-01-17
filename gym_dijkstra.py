import re
from dataclasses import dataclass, field
from typing import Any
import heapq
import gym


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)
    patent: Any=field(compare=False)

# ### get the inputs ###
# P = tuple(map(int, re.findall('\d+',input())))
# F = tuple(map(int, re.findall('\d+',input())))
# Size = tuple(map(int, re.findall('\d+',input())))
Ground = []
P = (0,0)
F = (10,10)
g = ["SFFHHHHHHHH",
     "FFFFFFFFFFF",
     "HFFHFHHFFHF",
     "HFFFFFHFFHF",
     "HFFHHHHHHFF",
     "HFFFFFHFFHF",
     "HHHFHHHFFHF",
     "HFFFFFFFFFF",
     "HFFFHHHFFFF",
     "HFFFFFFFHFF",
     "HHHHHHHHHFG"]

# Create the custom environment
env = gym.make("FrozenLake-v1",desc=g,
 render_mode="human", is_slippery=False)
env.action_space.seed(42)
observation, info = env.reset(seed=42)
Size = (len(g), len(g[0]))
for r in g:
    Ground.append(list(r))




# Reset the environment and start the game
obs = env.reset()
def push_itm(Open,itm):
    #print(Open)
    for a in Open:
        # print(a)
        if a.item == itm.item:
            if a.priority > itm.priority:
                a.priority = itm.priority
                a.patent = itm.patent
            return
    heapq.heappush(Open, itm)
    return
path = 'F'
goal = 'G'
Closed = {}
Open = []

parent = {}
parent[P] = [P]
itm = PrioritizedItem(0,(int(P[0]), int(P[1])),None)
Open.append(itm)
# end the loop if all possible node's are explored
while len(Open) != 0:
    vertex = heapq.heappop(Open)
    Closed[str(vertex.item)] = vertex.patent
    dist = vertex.priority
    node = vertex.item
    #if the Pacman fineds food break the loop
    if node == F:
        print("hi")
        Closed[F] = vertex.patent
        break

    # create neighbouring indexes
    UP, DOWN, LEFT, RIGHT = node[0]-1, node[0]+1, node[1]-1, node[1]+1

    # search for boundary and update nodes to Open
    if UP>0:
        if   Ground[UP][node[1]] == path or Ground[UP][node[1]] == goal :
            itm = PrioritizedItem(dist+1,(UP, node[1]),node)
            push_itm(Open, itm)
            
            Ground[UP][node[1]] = '#'

    if LEFT > 0 :
        if Ground[node[0]][LEFT] == path or  Ground[node[0]][LEFT] == goal :
            
            itm = PrioritizedItem(dist+1,(node[0], LEFT),node)
            push_itm(Open, itm)
            
            Ground[node[0]][LEFT] = '#'

    if RIGHT < Size[1]:
        if  Ground[node[0]][RIGHT] == path or Ground[node[0]][RIGHT] == goal:
    
            itm = PrioritizedItem(dist+1,(node[0], RIGHT),node)
            push_itm(Open, itm)
        
            Ground[node[0]][RIGHT] = '#'
    
    if DOWN < Size[0]:
        if  Ground[DOWN][node[1]] == path or Ground[DOWN][node[1]] == goal:

            itm = PrioritizedItem(dist,(DOWN, node[1]),node)
            push_itm(Open, itm)
        
            Ground[DOWN][node[1]] = '#'
              

print(len(Open))
# for n in Open:
#     print(f'{n[0]} {n[1]}')
s = F
print(Closed)
path = [F]

while s != P:
    path.append(Closed[str(s)])

    s = Closed[str(s)]
# print(path[0])
# print(path[1])
print(path)
for  i in reversed(range(1,len(path))):
    p0 = path[i]
    p1 = path[i-1]
    print(p0,p1)
    print(p0[0]-p1[0],p0[1]-p1[1])
    # move down
    if p0[0] - p1[0] <0:
        p = abs(p0[0] - p1[0])
        # print(p)
        for i in range(p):
            env.step(1)
    # move up
    elif p0[0] - p1[0] >0:
        p = abs(p0[0] - p1[0])
        for i in range(p):
            env.step(3)
    # move left
    if p0[1] - p1[1] >0:
        p = abs(p0[1] - p1[1])
        for i in range(p):
            env.step(0)
    # move right
    elif  p0[1] - p1[1] <0:
        p = abs(p0[1] - p1[1])
        for i in range(p):
            env.step(2)

env.close()