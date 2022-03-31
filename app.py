import numpy as np
import matplotlib.pyplot as plt

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QDialog


class Ui_MainWindow(QDialog):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 550)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.input = QtWidgets.QLabel(self.centralwidget)
        self.input.setGeometry(QtCore.QRect(0, 0, 400, 400))
        self.input.setText("")
        self.input.setScaledContents(True)
        self.input.setObjectName("input")
        self.output = QtWidgets.QLabel(self.centralwidget)
        self.output.setGeometry(QtCore.QRect(400, 0, 400, 400))
        self.output.setText("")
        self.output.setScaledContents(True)
        self.output.setObjectName("output")
        self.browse = QtWidgets.QPushButton(self.centralwidget)
        self.browse.setGeometry(QtCore.QRect(100, 457, 200, 50))
        self.browse.setObjectName("browse")
        self.segment = QtWidgets.QPushButton(self.centralwidget)
        self.segment.setGeometry(QtCore.QRect(500, 450, 200, 50))
        self.segment.setObjectName("segment")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.image = None
        self.browse.clicked.connect(self.browse_files)
        self.segment.clicked.connect(self.seg_image)

    def browse_files(self):
        self.output.setPixmap(QtGui.QPixmap(None))

        self.image = QFileDialog.getOpenFileName(self, 'Open Image', 'c:/')[0]
        self.input.setPixmap(QtGui.QPixmap(self.image))

    def seg_image(self):
        if self.image:
            lung_image, chest_image = segment(plt.imread(self.image))

            save_path = self.image.rsplit('.', 1)
            lung_save_path = save_path[0]+'_lung.'+save_path[1]
            chest_save_path = save_path[0]+'_chest.'+save_path[1]

            plt.imsave(lung_save_path, lung_image,
                       cmap='gray', vmin=0, vmax=255)
            plt.imsave(chest_save_path, chest_image,
                       cmap='gray', vmin=0, vmax=255)
            self.output.setPixmap(QtGui.QPixmap(lung_save_path))
        else:
            from PyQt5.QtWidgets import QMessageBox
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Enter an image, please!")
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(
            "MainWindow", "Lung segmentation"))
        self.browse.setText(_translate("MainWindow", "Add Image"))
        self.segment.setText(_translate("MainWindow", "Segment"))


if __name__ == "__main__":
    import sys

    lung_mean, lung_var, p_lung = 48.05384337837438, 617.538061718146, 0.2950886382501044
    chest_mean, chest_var, p_chest = 164.1760943484364, 886.4373431684157, 0.7049113617498955

    def pl(q): return p_lung*np.exp(-((q-lung_mean)**2) /
                                    (2*lung_var)) / np.sqrt(2*np.pi*lung_var)
    def pc(q): return p_chest*np.exp(-((q-chest_mean)**2) /
                                     (2*chest_var)) / np.sqrt(2*np.pi*chest_var)

    def compare(q): return pl(q) >= pc(q)

    def segment(img):
        # binary image of the lung
        lung_mask = compare(img)
        # element wise multiplication to get the greyscale image of the lung
        lung_image = lung_mask*img
        # invert the binary image to get the chest
        chest_image = ~lung_mask*img

        return lung_image, chest_image

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
