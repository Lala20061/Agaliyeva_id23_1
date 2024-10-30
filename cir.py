from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import math

def window():
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    win.setGeometry(300, 500, 600, 600)

    scene = QtWidgets.QGraphicsScene()
    view = QtWidgets.QGraphicsView(scene, win)
    view.setGeometry(0, 0, 600, 600)

    circle = QtWidgets.QGraphicsEllipseItem(100, 100, 400, 400)
    circle.setPen(QtGui.QPen(QtGui.QColor('red'), 4))
    scene.addItem(circle)

    point = QtWidgets.QGraphicsEllipseItem(-5, -5, 10, 10)
    point.setBrush(QtGui.QColor('green'))
    scene.addItem(point)

    angle = 0
    speed = 0.01
    direction = 1

    def renew():
        nonlocal angle
        angle += direction * speed
        x = 305 + 200 * math.cos(angle) - 5
        y = 305 + 200 * math.sin(angle) - 5
        point.setPos(x, y)

    timer = QtCore.QTimer()
    timer.timeout.connect(renew)
    timer.start(16)

    win.show()
    app.exec_()

window()


