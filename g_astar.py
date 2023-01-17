import re
from dataclasses import dataclass, field
from typing import Any
import heapq
import gym


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)
    patent: Any = field(compare=False)


class A_star:
    def __init__(self, p=(0, 0), f=(10, 10), g=None):
        self.Ground = []
        self.P = p
        self.F = f
        if g == None:
            self.g = ["SFFHHHHHHHH",
                      "FFFFFFFFFFF",
                      "HFFHFHFFFHF",
                      "HFFFFFFFFHF",
                      "HFFHHHHFHFF",
                      "HFFFFFHFFHF",
                      "HHHFHHHFFHF",
                      "HFHFFFFHFFH",
                      "HFFFHHHFFFF",
                      "HFHFFFFFHFF",
                      "HHHHHHHHHFG"]
        else:
            self.g = g

        # Create the custom self.environment
        self.env = gym.make("FrozenLake-v1", desc=self.g,
                            render_mode="human", is_slippery=False)
        self.env.action_space.seed(42)
        observation, info = self.env.reset(seed=42)
        self.Size = (len(self.g), len(self.g[0]))
        for r in self.g:
            self.Ground.append(list(r))

        # Reset the self.environment and start the game
        obs = self.env.reset()
    # computes the manhaten distance between Goal and current node

    def manhaten(self, x0, x1):
        return abs(x0[0]-x1[0]) + abs(x0[1]-x1[1])

    def push_itm(self, Open, itm):
        # print(Open)
        for a in Open:
            # print(a)
            if a.item == itm.item:
                if a.priority > itm.priority:
                    a.priority = itm.priority
                    a.patent = itm.patent
                return
        heapq.heappush(Open, itm)
        return

    def run(self):
        path = 'F'
        goal = 'G'
        self.Closed = {}
        Open = []

        itm = PrioritizedItem(0, (int(self.P[0]), int(self.P[1])), None)
        Open.append(itm)
        # end the loop if all possible node's are explored
        while len(Open) != 0:
            vertex = heapq.heappop(Open)
            self.Closed[str(vertex.item)] = vertex.patent
            dist = vertex.priority
            node = vertex.item
            # if the Pacman fineds food break the loop
            if node == self.F:
                print("goal!!")
                self.Closed[self.F] = vertex.patent
                break

            # create neighbouring indexes
            UP, DOWN, LEFT, RIGHT = node[0]-1, node[0]+1, node[1]-1, node[1]+1

            # search for boundary and update nodes to Open
            if UP > 0:
                if self.Ground[UP][node[1]] == path or self.Ground[UP][node[1]] == goal:
                    dist = dist + 1 + self.manhaten(((UP, node[1])), self.F)
                    itm = PrioritizedItem(dist, (UP, node[1]), node)
                    self.push_itm(Open, itm)

                    self.Ground[UP][node[1]] = '#'

            if LEFT > 0:
                if self.Ground[node[0]][LEFT] == path or self.Ground[node[0]][LEFT] == goal:
                    dist = dist + 1 + self.manhaten((node[0], LEFT), self.F)
                    itm = PrioritizedItem(dist, (node[0], LEFT), node)
                    self.push_itm(Open, itm)

                    self.Ground[node[0]][LEFT] = '#'

            if RIGHT < self.Size[1]:
                if self.Ground[node[0]][RIGHT] == path or self.Ground[node[0]][RIGHT] == goal:
                    dist = dist + 1 + self.manhaten((node[0], RIGHT), self.F)
                    itm = PrioritizedItem(dist, (node[0], RIGHT), node)
                    self.push_itm(Open, itm)

                    self.Ground[node[0]][RIGHT] = '#'

            if DOWN < self.Size[0]:
                if self.Ground[DOWN][node[1]] == path or self.Ground[DOWN][node[1]] == goal:
                    dist = dist + 1 + self.manhaten((DOWN, node[1]), self.F)
                    itm = PrioritizedItem(dist, (DOWN, node[1]), node)
                    self.push_itm(Open, itm)

                    self.Ground[DOWN][node[1]] = '#'

    def play(self):

        s = self.F
        path = [self.F]

        while s != self.P:
            path.append(self.Closed[str(s)])
            s = self.Closed[str(s)]

        print(path)
        for i in reversed(range(1, len(path))):
            p0 = path[i]
            p1 = path[i-1]
            # print(p0,p1)
            # print(p0[0]-p1[0],p0[1]-p1[1])
            # move down
            if p0[0] - p1[0] < 0:
                p = abs(p0[0] - p1[0])
                # print(p)
                for i in range(p):
                    self.env.step(1)
            # move up
            elif p0[0] - p1[0] > 0:
                p = abs(p0[0] - p1[0])
                for i in range(p):
                    self.env.step(3)
            # move left
            if p0[1] - p1[1] > 0:
                p = abs(p0[1] - p1[1])
                for i in range(p):
                    self.env.step(0)
            # move right
            elif p0[1] - p1[1] < 0:
                p = abs(p0[1] - p1[1])
                for i in range(p):
                    self.env.step(2)

        self.env.close()


if __name__ == "__main__":
    d = A_star()
    d.run()
    d.play()
