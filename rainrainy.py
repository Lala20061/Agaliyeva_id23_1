import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QInputDialog
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QTimer

width, height = 800, 600
platform_h = 40
platform_y = height - platform_h
drops_on_platform = 0
moving_cloud = None
is_paused = False

clouds = [{'x': 200, 'y': 100, 'w': 100, 'h': 50, 'shape': 'ellipse', 'color': 'gray', 'drops': 30, 'speed': 5}]
drops = []

def create_drops_for_cloud(cloud):
    return [{'x': random.randint(cloud['x'], cloud['x'] + cloud['w']),
             'y': cloud['y'] + cloud['h'],
             'w': random.randint(2, 4),
             'h': random.randint(8, 15),
             'dx': random.uniform(-2, 2),
             'speed': cloud['speed'] + random.uniform(-1, 1),
             'acceleration': random.uniform(0.1, 0.3),
             'cloud': cloud} for _ in range(cloud['drops'])]

def update_drops():
    global drops_on_platform
    for drop in drops:
        drop['speed'] += drop['acceleration']
        drop['y'] += drop['speed']
        drop['x'] += drop['dx']

        if platform_y <= drop['y'] <= platform_y + platform_h and 0 <= drop['x'] <= width:
            drops_on_platform += 1
            reset_drop(drop)

        if drop['y'] > height or drop['x'] < 0 or drop['x'] > width:
            reset_drop(drop)

    window.update()

def reset_drop(drop):
    c = drop['cloud']
    drop['x'] = random.randint(c['x'], c['x'] + c['w'])
    drop['y'] = c['y'] + c['h']
    drop['speed'] = c['speed'] + random.uniform(-1, 1)
    drop['dx'] = random.uniform(-1, 1)
    drop['acceleration'] = random.uniform(0.1, 0.3)

def paint_event(event):
    painter = QPainter(window)
    painter.setBrush(QColor('blue'))

    for drop in drops:
        painter.drawRect(int(drop['x']), int(drop['y']), drop['w'], drop['h'])

    painter.setBrush(QColor('green'))
    painter.drawRect(0, platform_y, width, platform_h)

    for c in clouds:
        painter.setBrush(QColor(c['color']))
        if c['shape'] == 'ellipse':
            painter.drawEllipse(c['x'], c['y'], c['w'], c['h'])
        elif c['shape'] == 'rectangle':
            painter.drawRect(c['x'], c['y'], c['w'], c['h'])
        elif c['shape'] == 'pooh':
            draw_pooh(painter, c)

    painter.setPen(QColor('black'))
    painter.drawText(10, platform_y - 10, f'Капли на платформе: {drops_on_platform}')

def draw_pooh(painter, c):
    cx, cy, r = c['x'] + c['w'] // 2, c['y'] + c['h'] // 2, min(c['w'], c['h']) // 2
    painter.drawEllipse(cx - r, cy - r, 2 * r, 2 * r)
    ear_r = r // 2
    painter.drawEllipse(cx - r - ear_r, cy - r, ear_r, ear_r)
    painter.drawEllipse(cx + r, cy - r, ear_r, ear_r)

def add_cloud():
    new_cloud = {'x': 100, 'y': 100, 'w': 100, 'h': 50, 'shape': 'ellipse', 'color': 'gray', 'drops': 10, 'speed': 5}
    clouds.append(new_cloud)
    drops.extend(create_drops_for_cloud(new_cloud))

def remove_cloud():
    if clouds:
        removed_cloud = clouds.pop()
        global drops
        drops = [drop for drop in drops if drop['cloud'] != removed_cloud]

def edit_cloud(c):
    colors = ['gray', 'blue', 'white', 'pink', 'yellow', 'green', 'orange']
    shapes = ['ellipse', 'rectangle', 'pooh']
    c['color'], _ = QInputDialog.getItem(window, "Цвет", "Выберите цвет:", colors, editable=False)
    c['shape'], _ = QInputDialog.getItem(window, "Форма", "Выберите форму:", shapes, editable=False)
    c['speed'], _ = QInputDialog.getInt(window, "Скорость", "Укажите скорость капель:", value=c['speed'], min=1, max=20)
    c['drops'], _ = QInputDialog.getInt(window, "Капли", "Укажите кол-во капель:", value=c['drops'], min=1, max=50)
    recreate_drops_for_cloud(c)

def recreate_drops_for_cloud(cloud):
    global drops
    drops = [drop for drop in drops if drop['cloud'] != cloud]
    drops.extend(create_drops_for_cloud(cloud))

def mouse_press(event):
    global moving_cloud
    for c in clouds:
        if c['x'] <= event.x() <= c['x'] + c['w'] and c['y'] <= event.y() <= c['y'] + c['h']:
            if event.button() == 1:
                moving_cloud = c
            elif event.button() == 2:
                edit_cloud(c)


def makestop():
    global is_paused
    if is_paused:
        timer.start(20)
        pause_button.setText("Пауза")
    else:
        timer.stop()
        pause_button.setText("Продолжить")
    is_paused = not is_paused

def mouse_move(event):
    if moving_cloud:
        moving_cloud['x'] = event.x() - moving_cloud['w'] // 2
        moving_cloud['y'] = event.y() - moving_cloud['h'] // 2
        recreate_drops_for_cloud(moving_cloud)

def mouse_release(event):
    global moving_cloud
    moving_cloud = None

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Дождик')
window.setGeometry(100, 100, width, height)
window.setStyleSheet("background-color: lightgray")
window.paintEvent = paint_event
window.mousePressEvent = mouse_press
window.mouseMoveEvent = mouse_move
window.mouseReleaseEvent = mouse_release

layout = QVBoxLayout()
btn_layout = QHBoxLayout()
btn_layout.addWidget(QPushButton("Добавить тучку", clicked=add_cloud))
btn_layout.addWidget(QPushButton("Удалить тучку", clicked=remove_cloud))
layout.addStretch()
layout.addLayout(btn_layout)
window.setLayout(layout)
pause_button = QPushButton("Пауза", clicked=makestop)
btn_layout.addWidget(pause_button)

timer = QTimer()
timer.timeout.connect(update_drops)
timer.start(20)

for cloud in clouds:
    drops.extend(create_drops_for_cloud(cloud))

window.show()
sys.exit(app.exec_())