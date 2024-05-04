from game_of_life import GameOfLife
import pyxel

class APP:
    def __init__(self):
        self.game_of_life = GameOfLife(128, 128)
        self.cell_img_topleft = (0, 0)
        self.cell_img_heigt = 2
        self.cell_img_width = 2
        pyxel.init(256, 256, title="game of life")
        pyxel.load('my_resource.pyxres')
        pyxel.run(self.update, self.draw)

    def update(self):
        self.game_of_life.update_state()

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, 0, 0, 256, 256)
        for r, row in enumerate(self.game_of_life.state):
            for c, val in enumerate(row):
                if val == 1:
                    pyxel.blt(c*2, r*2, 0,\
                        self.cell_img_topleft[0], self.cell_img_topleft[1], \
                        self.cell_img_width, self.cell_img_heigt, 0)
      
      
APP()