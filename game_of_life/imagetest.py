import numpy as np
import copy
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QInputDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
import time
from scipy.ndimage import zoom
import matplotlib.cm as cm


class PatternWidget(QWidget):
    def __init__(self, state_width, state_height, img_width, img_height):
        super().__init__()
        self.label = QLabel(self)
        self.state_width = state_width
        self.state_height = state_height
        self.img_width = img_width
        self.img_height = img_height
        self.label.setGeometry(0, 0, img_width, img_height)
        #self.state = np.random.randint(2, size=(self.state_height, self.state_width), dtype=np.int8)
        self.state = np.zeros((self.state_height, self.state_width))
        img = np.uint8(np.clip(self.state, 0, 1)*255)
        qimg = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_Grayscale8)
        qimg = qimg.scaled(self.img_height, self.img_width, Qt.SmoothTransformation)
        pixmap = QPixmap.fromImage(qimg)
        self.label.setPixmap(pixmap)
            

if __name__ == '__main__':
    app = QApplication([])
    widget = PatternWidget(30, 30, 30, 30)
    widget.show()
    app.exec_()
