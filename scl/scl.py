import sys, os
from scl_interaction_functions import *
import random

# 初期化設定に関するパラメタ
INITIAL_SUBSTRATE_DENSITY = 0.8

# モデルのパラメタ
# 各分子の移動しやすさ
MOBILITY_FACTOR = {
    'HOLE':           0.1,
    'SUBSTRATE':      0.1, 
    'CATALYST':       0.0001,
    'LINK':           0.05,
    'LINK_SUBSTRATE': 0.05,}
PRODUCTION_PROBABILITY             = 0.95
DISINTEGRATION_PROBABILITY         = 0.0005
BONDING_CHAIN_INITIATE_PROBABILITY = 0.1
BONDING_CHAIN_EXTEND_PROBABILITY   = 0.6
BONDING_CHAIN_SPLICE_PROBABILITY   = 0.9
BOND_DECAY_PROBABILITY             = 0.0005
ABSORPTION_PROBABILITY             = 0.5
EMISSION_PROBABILITY               = 0.5

class SCL:
    def __init__(self, space_size):
        self.space_size = space_size
        INITIAL_CATALYST_POSITIONS = [(random.randint(0, self.space_size), random.randint(0, self.space_size)) for _ in range(random.randint(1, 3))]
        self.particles = [[None for _ in range(self.space_size)] for _ in range(self.space_size)]
        # INITIAL_SUBSTRATE_DENSITYに従って、SUBSTRATEとHOLEを配置する。
        for x in range(self.space_size):
            for y in range(self.space_size):
                if evaluate_probability(INITIAL_SUBSTRATE_DENSITY):
                    p = {'type': 'SUBSTRATE', 'disintegrating_flag': False, 'bonds': []}
                else:
                    p = {'type': 'HOLE', 'disintegrating_flag': False, 'bonds': []}
                self.particles[x][y] = p
        # INITIAL_CATALYST_POSITIONSにCATALYSTを配置する。
        for x, y in INITIAL_CATALYST_POSITIONS:
            self.particles[x][y]['type'] = 'CATALYST'
    
        # 膜がある状態からスタートするには、コメントアウトしてください
        # for x0, y0, x1, y1 in INITIAL_BONDED_LINK_POSITIONS:
        #     particles[x0][y0]['type'] = 'LINK'
        #     particles[x0][y0]['bonds'].append((x1, y1))
        #     particles[x1][y1]['bonds'].append((x0, y0))

    def update(self):
        # 移動
        moved = [[False for _ in range(self.space_size)] for _ in range(self.space_size)]
        for x in range(self.space_size):
            for y in range(self.space_size):
                p = self.particles[x][y]
                n_x, n_y = get_random_neumann_neighborhood(x, y, self.space_size)
                n_p = self.particles[n_x][n_y]
                mobility_factor = (MOBILITY_FACTOR[p['type']] * MOBILITY_FACTOR[n_p['type']])**0.5
                if not moved[x][y] and not moved[n_x][n_y] and \
                len(p['bonds']) == 0 and len(n_p['bonds']) == 0 and \
                evaluate_probability(mobility_factor):
                        self.particles[x][y], self.particles[n_x][n_y] = n_p, p
                        moved[x][y] = moved[n_x][n_y] = True
        # 反応 
        for x in range(self.space_size):
            for y in range(self.space_size):
                production(self.particles, x, y, PRODUCTION_PROBABILITY)
                disintegration(self.particles, x, y, DISINTEGRATION_PROBABILITY)
                bonding(self.particles, x, y, BONDING_CHAIN_INITIATE_PROBABILITY,
                                        BONDING_CHAIN_SPLICE_PROBABILITY,
                                        BONDING_CHAIN_EXTEND_PROBABILITY) 
                bond_decay(self.particles, x, y, BOND_DECAY_PROBABILITY)
                absorption(self.particles, x, y, ABSORPTION_PROBABILITY)
                emission(self.particles, x, y, EMISSION_PROBABILITY)
                
    def reset(self):
        INITIAL_CATALYST_POSITIONS = [(random.randint(0, self.space_size-1), random.randint(0, self.space_size-1)) for _ in range(random.randint(1, 3))]
        self.particles = [[None for _ in range(self.space_size)] for _ in range(self.space_size)]
        # INITIAL_SUBSTRATE_DENSITYに従って、SUBSTRATEとHOLEを配置する。
        for x in range(self.space_size):
            for y in range(self.space_size):
                if evaluate_probability(INITIAL_SUBSTRATE_DENSITY):
                    p = {'type': 'SUBSTRATE', 'disintegrating_flag': False, 'bonds': []}
                else:
                    p = {'type': 'HOLE', 'disintegrating_flag': False, 'bonds': []}
                self.particles[x][y] = p
        # INITIAL_CATALYST_POSITIONSにCATALYSTを配置する。
        for x, y in INITIAL_CATALYST_POSITIONS:
            self.particles[x][y]['type'] = 'CATALYST'