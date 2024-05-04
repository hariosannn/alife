from scl import SCL
import pyxel

class APP:
    def __init__(self):
        self.scl = SCL(32)
        self.catalyst_img_topleft = (0, 0)
        self.settings = {'CATALYST':{'img_topleft':(0, 0), 'height':8, 'width':8},\
                         'SUBSTRATE':{'img_topleft':(8, 0), 'height':8, 'width':8},
                         'LINK':{'img_topleft':(0, 8), 'height':8, 'width':8},
                         'LINK_SUBSTRATE':{'img_topleft':(8, 8), 'height':8, 'width':8}}
        pyxel.init(256, 256, fps=30, title="substrate catalyst link")
        pyxel.load('my_resource.pyxres')
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            #self.scl.reset_state()
            pass
        else:
            self.scl.update()

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, 0, 0, 256, 256)
        for r, row in enumerate(self.scl.particles):
            for c, val in enumerate(row):
                if val['type'] != 'HOLE':
                    pyxel.blt(c*8, r*8, 0,\
                        self.settings[val['type']]['img_topleft'][0], self.settings[val['type']]['img_topleft'][1], \
                        self.settings[val['type']]['width'], self.settings[val['type']]['height'], 0)
                    if len(val['bonds']) > 0:
                        for bond in val['bonds']:
                            diff_y = bond[0] - r
                            diff_x = bond[1] - c
                            bond_ind = diff_x+1 + 3*(diff_y+1)
                            pyxel.blt(c*8, r*8, 0,\
                                      0, 16+bond_ind*8, \
                                      8, 8, 0)
                            
      
APP()