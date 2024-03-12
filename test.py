# !/usr/bin/env python
# encoding=utf-8

# author            : jeonghyeon park
# created data      : 2024.03.08
# modified data     : 2024.03.08
# description       :

"""
drag drop test!!!!!!!!!!

"""

from PySide2 import QtCore, QtGui, QtWidgets


import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QLabel, QMenu, QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Context Menu Example')

        # 레이블들을 생성하고 각각의 컨텍스트 메뉴 연결
        self.labels = []
        for i in range(3):
            label = QLabel(f'Label {i+1}', self)
            label.move(20, 30*i + 10)
            label.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            label.customContextMenuRequested.connect(self.showContextMenu)
            self.labels.append(label)

    def showContextMenu(self, pos):
        # 현재 우클릭한 레이블을 확인
        label = self.sender()
        index = self.labels.index(label)

        # 서브 메뉴 생성
        contextMenu = QMenu(self)
        action1 = contextMenu.addAction(f"Action 1 for Label {index+1}")
        action2 = contextMenu.addAction(f"Action 2 for Label {index+1}")

        # 서브 메뉴 표시
        action = contextMenu.exec_(self.mapToGlobal(pos))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())