import numpy as np
import copy
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QInputDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
import time
from scipy.ndimage import zoom
import matplotlib.cm as cm


def update_pattern(state, height, width):
    next_state = copy.deepcopy(state)
    for i in range(height):
        for j in range(width):
            # 自分と近傍のセルの状態を取得
            # c: center (自分自身)
            # nw: north west, ne: north east, c: center ...
            nw = state[(i-1)%height][(j-1)%width]
            n  = state[(i-1)%height][j]
            ne = state[(i-1)%height][(j+1)%width]
            w  = state[i][(j-1)%width]
            c  = state[i][j]
            e  = state[i][(j+1)%width]
            sw = state[(i+1)%height][(j-1)%width]
            s  = state[(i+1)%height][j]
            se = state[(i+1)%height][(j+1)%width]
            neighbor_cell_sum = nw + n + ne + w + e + sw + s + se
            #print(state)
            #print(i, j, neighbor_cell_sum, c)
            if c == 0 and neighbor_cell_sum == 3:
                next_state[i,j] = 1
            elif c == 1 and neighbor_cell_sum in (2,3):
                next_state[i,j] = 1
            else:
                next_state[i,j] = 0
    #print(next_state)
    #print("\n")
    return next_state

class PatternWidget(QWidget):
    def __init__(self, state_width, state_height, img_width, img_height):
        super().__init__()
        self.label = QLabel(self)
        self.state_width = state_width
        self.state_height = state_height
        self.img_width = img_width
        self.img_height = img_height
        self.label.setGeometry(0, 0, img_width, img_height)
        self.state = np.random.randint(2, size=(self.state_height, self.state_width), dtype=np.int8)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_pattern)
        self.timer.start(50)  
        self.setMouseTracking(True)
        self.click_times = []

    def update_pattern(self):
        self.state = update_pattern(self.state, self.state_height, self.state_width)
        #img = np.uint8(cm.nipy_spectral(self.img_array*0.45)[:, :, :3]*255)
        img = np.uint8(np.clip(1-self.state, 0, 1)*255)
        # calculate the total number of bytes in the frame 
        totalBytes = self.state.nbytes
        # divide by the number of rows
        bytesPerLine = int(totalBytes/self.state_height)
        qimg = QImage(img.data, img.shape[1], img.shape[0], bytesPerLine, QImage.Format_Grayscale8)
        qimg = qimg.scaled(self.img_height, self.img_width)
        pixmap = QPixmap.fromImage(qimg)
        self.label.setPixmap(pixmap)

    
    def reset_pattern(self):
        self.state = np.zeros((self.state_height, self.state_width), dtype=np.int8)
        self.state = np.random.randint(2, size=(self.state_height, self.state_width), dtype=np.int8)

    def mousePressEvent(self, event):
        current_time = time.time()
        self.click_times = [t for t in self.click_times if current_time - t <= 0.5]
        self.click_times.append(current_time)

        if len(self.click_times) >= 3:
            self.reset_pattern()
            self.click_times = []
        else:
            x, y = event.x(), event.y()
            self.state[y, x] = 1
            

if __name__ == '__main__':
    app = QApplication([])
    widget = PatternWidget(128, 128, 500, 500)
    widget.show()
    app.exec_()
