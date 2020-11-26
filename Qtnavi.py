from functions_for_navigator import min_way_func, StartPointError, EndPointError, WeyError
from PyQt5.QtGui import QPixmap
from interfeis import Ui_MainWindow
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QColorDialog, QInputDialog, \
    QTableWidgetItem
import sys
import csv
from random import randint
from PyQt5.QtCore import Qt
from PIL import ImageQt
import json
from PIL import Image, ImageDraw
from PyQt5 import uic


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.InitUi()

    def InitUi(self):
        self.setWindowTitle('Навигатор')
        self.setFixedSize(817, 622)
        self.color_of_foot_road = '#00ff00'
        self.color_of_velo_road = '#bebe00'
        self.color_of_wey = '#ff0000'
        self.foot_speed = 2.5
        self.speed_foot_lbl.setText(str(self.foot_speed))
        self.cycle_speed = 6
        self.speed_cycle_lbl.setText(str(self.cycle_speed))
        self.start_point = -1
        self.end_point = -1
        self.tran = 'by_foot'
        self.flags_false()
        self.draw_flag = False
        # create
        self.change_map_func()
        self.map.setScaledContents(True)
        self.choose_start.clicked.connect(self.choose_start_point)
        self.choose_end.clicked.connect(self.choose_end_point)
        self.bild_wey.clicked.connect(self.build_wey_func)
        self.transport.buttonClicked.connect(self.transport_func)
        self.change_speed_cycle.clicked.connect(self.change_speed_cycle_func)
        self.change_speed_foot.clicked.connect(self.change_speed_foot_func)
        self.clear_btn.clicked.connect(self.clear_func)
        self.chenge_map.clicked.connect(self.change_map_func)
        self.chenge_color_of_foot_wey.clicked.connect(self.change_color_of_foot_road_func)
        self.chenge_color_of_cicle_wey.clicked.connect(self.change_color_of_cycle_road_func)
        self.chenge_color_of_wey.clicked.connect(self.change_color_of_wey_func)
        self.see_the_history.clicked.connect(self.call_history)
        self.clear_history_btn.clicked.connect(self.clear_history)

    def clear_history(self):
        self.new_line_history(["transport", "from", "to", "len of wey", "time", "wey to map"],
                              char='w')

    def flags_false(self):
        self.flag_a = False
        self.flag_o = False
        self.flag_v = False
        self.flag_d = False

    def keyPressEvent(self, event):
        if int(event.modifiers()) == Qt.ControlModifier:
            # from
            if event.key() == Qt.Key_F:
                self.choose_start_point()
            # to
            elif event.key() == Qt.Key_T:
                self.choose_end_point()
            # pasha
            elif event.key() == Qt.Key_O:
                if not (self.flag_v and self.flag_a and self.flag_d):
                    self.flag_o = True
                else:
                    self.flags_false()
            elif event.key() == Qt.Key_V and self.flag_o:
                if not (self.flag_a and self.flag_d):
                    self.flag_v = True
                else:
                    self.flags_false()
            elif event.key() == Qt.Key_A and self.flag_v:
                if not self.flag_d:
                    self.flag_a = True
                else:
                    self.flags_false()
            elif event.key() == Qt.Key_D and self.flag_a:
                self.flag_d = True
        if self.flag_d and self.flag_a and self.flag_v and self.flag_o:
            self.draw_flag = True
            self.repaint()

    def paintEvent(self, event):
        if self.draw_flag:
            qp = QPainter()
            qp.begin(self)
            self.pasha_paint_func(qp)
            qp.end()

    def pasha_paint_func(self, qp):
        # self.setStyleSheet("background-color: {}".format(255, 255, 255))
        color = QColor(randint(0, 255), randint(0, 255), randint(0, 255))
        qp.setPen(color)
        qp.drawEllipse(5, 250, 62, 350)
        qp.drawLine(72, 250, 103, 600)
        qp.drawLine(103, 600, 134, 250)
        qp.drawLine(130, 600, 161, 250)
        qp.drawLine(161, 250, 192, 600)
        qp.drawArc(180, 250, 62, 350, -1650, 3300)
        qp.drawLine(205, 250, 205, 600)
        qp.drawLine(255, 250, 255, 585)
        qp.setBrush(color)
        qp.drawEllipse(253, 592, 5, 5)

    def call_history(self):
        ex_h.loadTable('history.csv')
        ex_h.middle_items()
        ex_h.show()

    def paint(self, map_wey='all', restoration='w'):
        # if map_wey != all: map_wey == [wey_points]
        if map_wey == 'all':
            drawer = ImageDraw.Draw(self.image)
            for i in self.foot_graph:
                for j in self.foot_graph[i]:
                    drawer.line(((self.coordinates[i]), (self.coordinates[j[0]])),
                                self.color_of_foot_road, 5)
            for i in self.velo_graph:
                for j in self.velo_graph[i]:
                    drawer.line(((self.coordinates[i]), (self.coordinates[j[0]])),
                                self.color_of_velo_road, 5)
        else:
            if restoration == 'v':
                color = self.color_of_velo_road
            elif restoration == 'f':
                color = self.color_of_foot_road
            else:
                color = self.color_of_wey
            try:
                drawer = ImageDraw.Draw(self.image)
                first = self.start_point
                for i in map_wey:
                    drawer.line((self.coordinates[first], self.coordinates[i]), color, 3)
                    first = i
            except KeyError:
                pass
        self.image.putalpha(255)
        self.map.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(self.image)))

    def change_color_of_wey_func(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_of_wey = color.name()
            if self.last_wey != -1:
                self.paint(map_wey=self.last_wey[1:-1], restoration='w')

    def change_speed_cycle_func(self):
        speed, flag = QInputDialog.getDouble(self, 'введите скорость лт',
                                             'какая скорость лт в м/с?', 6.0, 3.0, 12.0, 2)
        if flag:
            self.cycle_speed = speed
            self.speed_cycle_lbl.setText(str(self.cycle_speed))

    def change_speed_foot_func(self):
        speed, flag = QInputDialog.getDouble(self, 'введите скорость пешехода',
                                             'какая скорость пешехода в м/с?', 2.5, 0.5, 5.0, 2)
        if flag:
            self.foot_speed = speed
            self.speed_foot_lbl.setText(str(self.foot_speed))

    def change_color_of_foot_road_func(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_of_foot_road = color.name()
            self.paint()
            if self.last_wey != -1:
                self.paint(map_wey=self.last_wey[1:-1], restoration='w')

    def change_color_of_cycle_road_func(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_of_velo_road = color.name()
            self.paint()
            if self.last_wey != -1:
                self.paint(map_wey=self.last_wey[1:-1], restoration='w')

    def change_map_func(self):
        new_name, flag = QFileDialog.getOpenFileName(self, 'Выбрать карту',
                                                     '', 'Картинка (*.jpg);;Картинка (*.PNG)')
        if flag:
            self.name_of_map = new_name
            # give
            file_name, flag1 = QFileDialog.getOpenFileName(self, 'Выбрать файл с данными', '',
                                                           'JSON file (*.json)')
            if flag1:
                read_list = open(file_name, 'r', encoding='utf-8').readline()
                read_list = json.loads(read_list)
                self.rect_gr = read_list[0]
                self.foot_graph = {int(k): v for k, v in read_list[1].items()}
                self.foot_max_of_len = read_list[2]
                self.velo_graph = {int(k): v for k, v in read_list[3].items()}
                self.velo_max_of_len = read_list[4]
                self.coordinates = {int(k): tuple(v) for k, v in read_list[5].items()}
                self.dict_of_names = {int(k): v for k, v in read_list[6].items()}
                self.dict_of_names_rev = {v: k for k, v in self.dict_of_names.items()}
                # end give
                self.image = Image.open(self.name_of_map)
                self.last_wey = -1
                self.clear_func()

    def mouseDoubleClickEvent(self, event):
        x = event.x()
        y = event.y()
        for obj in self.coordinates:
            x_o = self.coordinates[obj][0] + 300
            y_o = self.coordinates[obj][1] + 10
            if (x_o - self.rect_gr // 2 < x < x_o + self.rect_gr and
                    y_o - self.rect_gr // 2 < y < y_o + self.rect_gr):
                value, flag = QInputDialog.getItem(self, 'сюда или отсюда', 'отсюда или сюда?',
                                                   ('сюда', 'отсюда'), 1, False)
                if flag:
                    if value == 'отсюда':
                        self.start_point = obj
                        self.start_lbl.setText(self.dict_of_names[self.start_point])
                    else:
                        self.end_point = obj
                        self.end_lbl.setText(self.dict_of_names[self.end_point])
                break

    def clear_func(self):
        self.paint()
        self.error_lbl.setText('')
        self.start_lbl.setText('')
        self.end_lbl.setText('')
        self.wey.setText('')
        self.start_point = -1
        self.end_point = -1
        self.best_transport.setText('')
        self.len_of_wey.display(0)
        self.time_of_wey.display(0)

    def transport_func(self, btn):
        self.tran = btn.objectName()

    def choose_start_point(self):
        start_point, flag = QInputDialog.getItem(self, "Выберите стартовую точку", "откуда начать?",
                                                 (self.dict_of_names[i] for i in self.dict_of_names),
                                                 1, False)
        if flag:
            self.start_point = start_point
            self.start_lbl.setText(self.start_point)
            self.start_point = self.dict_of_names_rev[self.start_point]

    def choose_end_point(self):
        end_point, flag = QInputDialog.getItem(self, "Выберите стартовую точку", "откуда начать?",
                                               (self.dict_of_names[i] for i in self.dict_of_names),
                                               1, False)
        if flag:
            self.end_point = end_point
            self.end_lbl.setText(self.end_point)
            self.end_point = self.dict_of_names_rev[self.end_point]

    def new_line_history(self, letter, char='a'):
        # letter = [points, len, time]
        with open('history.csv', char, encoding='utf-8', newline='') as hist_file:
            writer = csv.writer(hist_file, delimiter=';', quotechar='"',
                                quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(letter)

    def build_wey_func(self):
        self.error_lbl.setText('')
        self.best_transport.setText('')
        # arg from data base
        if self.last_wey != -1:
            self.paint(map_wey=self.last_wey[1:-1], restoration=self.last_wey[0])
        try:
            if self.start_point == -1:
                raise StartPointError('Выберите начальную точку!')
            if self.end_point == -1:
                raise EndPointError('Выберите конечную точку!')
            fast = '------'
            if self.start_point == self.end_point:
                self.wey.setText('Вы уже на месте')
            else:
                if self.tran == 'by_foot':
                    min_wey = min_way_func(self.foot_graph, self.foot_max_of_len, self.start_point,
                                           self.end_point)
                    speed = self.foot_speed
                    char_wey = 'f'
                elif self.tran == 'by_cycle':
                    min_wey = min_way_func(self.velo_graph, self.velo_max_of_len, self.start_point,
                                           self.end_point)
                    speed = self.cycle_speed
                    char_wey = 'v'
                else:
                    min_wey_foot = min_way_func(self.foot_graph, self.foot_max_of_len,
                                                self.start_point,
                                                self.end_point)
                    min_wey_cycle = min_way_func(self.velo_graph, self.velo_max_of_len,
                                                 self.start_point,
                                                 self.end_point)
                    if min_wey_cycle == -1:
                        min_wey = min_wey_foot
                        fast = 'пешком'
                        speed = self.foot_speed
                        char_wey = 'f'
                    elif min_wey_foot == -1:
                        min_wey = min_wey_cycle
                        fast = 'личный транспорт'
                        speed = self.cycle_speed
                        char_wey = 'v'
                    else:
                        if min_wey_cycle[-1] * 100 / self.cycle_speed < \
                                min_wey_foot[-1] * 100 / self.foot_speed:
                            fast = 'на личном транспорте'
                            speed = self.cycle_speed
                            min_wey = min_wey_cycle
                            char_wey = 'v'
                        elif min_wey_cycle[-1] * 100 / self.cycle_speed > \
                                min_wey_foot[-1] * 100 / self.foot_speed:
                            speed = self.foot_speed
                            fast = 'пешком'
                            min_wey = min_wey_foot
                            char_wey = 'f'
                        else:
                            fast = 'все равно, гуляйте'
                            speed = self.foot_speed
                            min_wey = min_wey_foot
                            char_wey = 'f'
                if min_wey == -1:
                    raise WeyError('Выберите другой транспорт!')
                self.best_transport.setText(fast)
                normal_view = [self.dict_of_names[i] for i in min_wey[:-1]]
                self.wey.setText(', '.join(normal_view))
                len_of_wey = min_wey[-1] * 100
                self.len_of_wey.display(len_of_wey)
                time = round(min_wey[-1] * 100 / speed / 60, 2)
                self.time_of_wey.display(time)
                self.paint(min_wey[:-1])
                # запись маршрута в историю поездок
                self.new_line_history([char_wey, self.dict_of_names[self.start_point],
                                       self.dict_of_names[self.end_point], len_of_wey, time,
                                       self.name_of_map])
                self.last_wey = [char_wey, self.start_point] + min_wey
                self.error_lbl.setText("Маршрут построен")
        except StartPointError as er:
            self.error_lbl.setText(str(er))
        except EndPointError as er:
            self.error_lbl.setText(str(er))
        except WeyError as er:
            self.error_lbl.setText(str(er))
            self.wey.setText('Маршрут невозможен')
            self.len_of_wey.display('error')
            self.time_of_wey.display('error')


class HistoryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('history window.ui', self)
        self.loadTable('history.csv')
        self.middle_items()

    def middle_items(self):
        with open('history.csv', 'r', encoding='utf-8') as file1:
            n = 0
            time_m = 0
            len_m = 0
            start = dict()
            end = dict()
            reader = csv.DictReader(file1, delimiter=';', quotechar='"')
            for note in reader:
                n += 1
                time_m += float(note["time"])
                len_m += float(note["len of wey"])
                if note["from"] in start:
                    start[note["from"]] += 1
                else:
                    start[note["from"]] = 1
                if note["to"] in end:
                    end[note["to"]] += 1
                else:
                    end[note["to"]] = 1
            if n != 0:
                self.mi_time_lbl.setText(f'{round(time_m / n, 2)} минут')
                self.mi_len_lbl.setText(f'{round(len_m / n, 3)} метров')
                self.mostly_start_lbl.setText(sorted(start, key=lambda x: start[x], reverse=True)[0])
                self.mostly_end_lbl.setText(sorted(end, key=lambda x: end[x], reverse=True)[0])
            else:
                self.mi_time_lbl.setText('0')
                self.mi_len_lbl.setText('0')
                self.mostly_start_lbl.setText('нет поездок')
                self.mostly_end_lbl.setText('нет поездок')

    def loadTable(self, table_name):
        with open(table_name, encoding="utf8") as csv_file:
            reader = csv.reader(csv_file,
                                delimiter=';', quotechar='"')
            title = next(reader)
            self.history_table.setColumnCount(len(title))
            self.history_table.setHorizontalHeaderLabels(title)
            self.history_table.setRowCount(0)
            for i, row in enumerate(reader):
                self.history_table.setRowCount(
                    self.history_table.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.history_table.setItem(
                        i, j, QTableWidgetItem(elem))
        self.history_table.resizeColumnsToContents()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex_h = HistoryWindow()
    sys.excepthook = except_hook
    ex.show()
    sys.exit(app.exec_())
