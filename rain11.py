import sys
import random
import json
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QTimer

width, height = 800, 600
platform_h = 40
platform_y = height - platform_h
num_drops = 1000

drops_on_platform = 0

with open('drops_parameters.json', 'r') as file:
    drop_parameters = json.load(file)

drops = []
for _ in range(num_drops):
    params = random.choice(drop_parameters)
    drop = {
        'x': random.randint(0, width),
        'y': random.randint(0, height),
        'width': params['width'],
        'height': params['height'],
        'speed': random.randint(params['min_speed'], params['max_speed'])
    }
    drops.append(drop)

def update_drops():
    global drops_on_platform
    for drop in drops:
        drop['y'] += drop['speed']

        if drop['y'] + drop['height'] >= platform_y:
            drops_on_platform += 1
            drop['y'] = -drop['height']
            drop['x'] = random.randint(0, width)
        elif drop['y'] > height:
            drop['y'] = -drop['height']
            drop['x'] = random.randint(0, width)

    window.update()

def paint_event(event):
    painter = QPainter(window)
    painter.setBrush(QColor('blue'))

    for drop in drops:
        painter.drawRect(drop['x'], drop['y'], drop['width'], drop['height'])

    painter.setBrush(QColor('green'))
    painter.drawRect(0, platform_y, width, platform_h)

    painter.setPen(QColor('black'))
    painter.drawText(10, platform_y - 10, f'Кол-во капель: {drops_on_platform}')

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Дождик')
window.setGeometry(100, 100, width, height)
window.setStyleSheet("background-color: lightgray")
window.paintEvent = paint_event

timer = QTimer()
timer.timeout.connect(update_drops)
timer.start(30)

window.show()
sys.exit(app.exec_())











