import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QInputDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
import time
from scipy.ndimage import zoom
import matplotlib.cm as cm

SPACE_SIZE = 600

def update_pattern(state, rule):
    next_state = np.zeros(state.shape, dtype=np.int8)
    for i in range(SPACE_SIZE):
        # left, center, right cellの状態を取得
        l = state[i-1]
        c = state[i]
        r = state[(i+1)%SPACE_SIZE]
        # neighbor_cell_codeは現在の状態のバイナリコーディング
        # ex) 現在が[1 1 0]の場合
        #     neighbor_cell_codeは 1*2^2 + 1*2^1 + 0*2^0 = 6となるので、
        #     RULEの６番目のビットが１ならば、次の状態は１となるので、
        #     RULEをneighbor_cell_code分だけビットシフトして１と論理積をとる。
        neighbor_cell_code = 2**2 * l + 2**1 * c + 2**0 * r
        if (rule >> neighbor_cell_code) & 1:
            next_state[i] = 1
        else:
            next_state[i] = 0
    # 表示をアップデート
    return next_state

class PatternWidget(QWidget):
    def __init__(self, width, height):
        super().__init__()
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, width, height)
        self.rule = 62
        self.state = np.zeros(SPACE_SIZE, dtype=np.int8)
        self.state[:] = np.random.randint(2, size=len(self.state))
        self.img_array = np.zeros((SPACE_SIZE, SPACE_SIZE))
        self.img_array[0] = self.state
        self.update_row = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_pattern)
        self.timer.start(10)  # 50ミリ秒ごとに更新
        self.setMouseTracking(True)
        self.click_times = []

    def update_pattern(self):
        self.state = update_pattern(self.state, self.rule)
        self.update_row += 1
        self.update_row %= self.img_array.shape[1]
        self.img_array[self.update_row] = 1-self.state
        #img = np.uint8(cm.nipy_spectral(self.img_array*0.45)[:, :, :3]*255)
        img = np.uint8(np.clip(self.img_array, 0, 1)*255)
        qimg = QImage(img.data, img.shape[0], img.shape[1], QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qimg)
        self.label.setPixmap(pixmap)

    
    def reset_pattern(self):
        self.state = np.zeros(SPACE_SIZE, dtype=np.int8)
        self.state[:] = np.random.randint(2, size=len(self.state))
        self.img_array = np.zeros((SPACE_SIZE, self.height))
        self.img_array[0] = self.state
        self.update_row = 0

    def mousePressEvent(self, event):
        current_time = time.time()
        self.click_times = [t for t in self.click_times if current_time - t <= 0.5]
        self.click_times.append(current_time)

        if len(self.click_times) >= 3:
            self.reset_pattern()
            self.click_times = []
        else:
            # ポップアップウィンドウを表示してself.ruleの値を選択する
            rules, ok = QInputDialog.getItem(self, "Select Rule", "Rule:", [str(i) for i in range(256)], current=self.rule)
            if ok:
                self.rule = int(rules)

if __name__ == '__main__':
    app = QApplication([])
    widget = PatternWidget(SPACE_SIZE, SPACE_SIZE)
    widget.show()
    app.exec_()
