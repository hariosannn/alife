import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
import time
from scipy.ndimage import zoom
import matplotlib.cm as cm

dt = 1
dx = 0.01
def update_pattern(U, V, Du, Dv, f, k):
    laplacian_U = (np.roll(U, 1, axis=0) + np.roll(U, -1, axis=0) + np.roll(U, 1, axis=1) + np.roll(U, -1, axis=1) - 4 * U)/(dx*dx)
    laplacian_V = (np.roll(V, 1, axis=0) + np.roll(V, -1, axis=0) + np.roll(V, 1, axis=1) + np.roll(V, -1, axis=1) - 4 * V)/(dx*dx)
    U += (Du * laplacian_U - U * V * V + f * (1.0 - U)) * dt
    V += (Dv * laplacian_V + U * V * V - (f + k) * V) * dt
    return U, V

class PatternWidget(QWidget):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, width, height)
        self.U = np.ones((height, width))
        self.V = np.zeros((height, width))
        self.V[height//2-10:height//2+10, width//2-10:width//2+10] = 1
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_pattern)
        self.timer.start(10)  # 50ミリ秒ごとに更新
        self.setMouseTracking(True)
        self.click_times = []

    def update_pattern(self):
        self.U, self.V = update_pattern(self.U, self.V, 2e-5, 1e-5, 0.04, 0.060)
        self.V = np.clip(self.V, 0, 1)
        self.U = np.clip(self.U, 0, 1)

        img = np.uint8(np.clip(self.V * 500, 0, 255))
        qimg = QImage(img.data, self.width, self.height, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qimg)
        self.label.setPixmap(pixmap)
        """
        img = np.uint8(cm.winter(img)[:, :, :3] * 255)
        print(self.V.max())
        qimg = QImage(img.data, self.width, self.height, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        self.label.setPixmap(pixmap)
        """

    
    def reset_pattern(self):
        self.U = np.ones((self.height, self.width))
        self.V = np.zeros((self.height, self.width))
        self.V[self.height//2-10:self.height//2+10, self.width//2-10:self.width//2+10] = 1

    def mousePressEvent(self, event):
        current_time = time.time()
        self.click_times = [t for t in self.click_times if current_time - t <= 0.5]
        self.click_times.append(current_time)

        if len(self.click_times) >= 3:
            self.reset_pattern()
            self.click_times = []
        else:
            x, y = event.x(), event.y()
            self.V[y-5:y+5, x-5:x+5] = 1

    def mouseMoveEvent(self, event):
        x, y = event.x(), event.y()
        self.V[y-5:y+5, x-5:x+5] = 1

if __name__ == '__main__':
    app = QApplication([])
    widget = PatternWidget(400, 400)
    widget.show()
    app.exec_()