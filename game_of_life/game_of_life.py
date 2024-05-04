import copy
import random

class GameOfLife(object):
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.state = [[0]*self.width for i in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                self.state[i][j] = random.randint(0, 1)


    def update_state(self):
        next_state = copy.deepcopy(self.state)
        for i in range(self.height):
            for j in range(self.width):
                # 自分と近傍のセルの状態を取得
                # c: center (自分自身)
                # nw: north west, ne: north east, c: center ...
                nw = self.state[(i-1)%self.height][(j-1)%self.width]
                n  = self.state[(i-1)%self.height][j]
                ne = self.state[(i-1)%self.height][(j+1)%self.width]
                w  = self.state[i][(j-1)%self.width]
                c  = self.state[i][j]
                e  = self.state[i][(j+1)%self.width]
                sw = self.state[(i+1)%self.height][(j-1)%self.width]
                s  = self.state[(i+1)%self.height][j]
                se = self.state[(i+1)%self.height][(j+1)%self.width]
                neighbor_cell_sum = nw + n + ne + w + e + sw + s + se
                #print(state)
                #print(i, j, neighbor_cell_sum, c)
                if c == 0 and neighbor_cell_sum == 3:
                    next_state[i][j] = 1
                elif c == 1 and neighbor_cell_sum in (2,3):
                    next_state[i][j] = 1
                else:
                    next_state[i][j] = 0
        self.state = next_state