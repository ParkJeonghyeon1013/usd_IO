import importlib, typing
import pathlib, sys, functools
import os
from PySide2 import QtCore, QtGui, QtWidgets

sys.path.append("D:/git_workspace/usd_IO/main")


# from main.resource.ui.sample_window4_ui import Ui_MainWindow
from main.resource.ui.sample_window5_ui import Ui_MainWindow
from main.libs.api_osm import OSMCity
from main.libs.api_grayscale import GrayScaleCity

# importlib.reload(Ui_MainWindow)

'''

'''

class Signals(QtWidgets.QApplication):
    update_progress = QtCore.Signal(int)

class LineEdit:
    grid_path = 'lineEdit__grid_path'
    osm_path = 'lineEdit__osm_path'


class CityBuilder(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parnet=None):
        super(CityBuilder, self).__init__(parnet)

        # variable
        self.__grid_path = ''
        self.__osm_path = ''
        self.__save_path = 'D:/git_workspace/usd_IO/outout'
        self.__form = {'hip':'', 'jpg':'', 'mov':'', 'usd':''}
        self.__save_path_lst = list()
        self.__task_type = ''
        self.build_grayscale = GrayScaleCity()
        self.build_osm = OSMCity()



        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.__init()
        self.resize(1000, 1000)
        self.setupUi(self)
        # self.show()
        self.__connection()

    @property
    def grid_path(self):
        return self.__grid_path
    @grid_path.setter
    def grid_path(self, val):
        # assert isinstance(val, pathlib.path)
        self.__grid_path = val

    @property
    def osm_path(self):
        return self.__osm_path
    @osm_path.setter
    def osm_path(self, val):
        # assert isinstance(val, pathlib.path)
        self.__osm_path = val


    # 초기상태 저장
    def __init(self):
        # self.pushButton__save.setEnabled(0)
        pass

    def __connection(self):
        self.toolButton__gird_path.clicked.connect(lambda x: self.file_dialog('grid_path'))
        self.toolButton__osm.clicked.connect(lambda x: self.file_dialog('osm_path'))
        self.pushButton__start.clicked.connect(self.__slot_btn_save)
        self.pushButton__open.clicked.connect(self.__slot_btn_open)


    def __slot_btn_open(self):
        saved_path = self.lineEdit__open.text()
        self.dir_dialog(saved_path)


    def __slot_btn_save(self):
        self.mk_dir()
        # self.progressBar__build.setValue()
        print('progress bar setting 해주기 ')
        self.build_grayscale.save_hip(self.__form['hip'])

    def __slot_image_Rclick(self):
        pass

    # WHEN Right click on the label
    # then MOV player come up
    def contextMenuEvent(self, event):
        # todo : 범위 지정해주기 현재는 어디든 다 적용됨.
        context_menu = QtWidgets.QMenu(self)

        a1 = context_menu.addAction('OverView City MOV')
        a2 = context_menu.addAction('action 2')

        a1.triggered.connect(self.overview_player)
        a2.triggered.connect(self.action2_trigger)

        context_menu.exec_(event.globalPos())

    def overview_player(self):
        print('mov play hereeeee')
    def action2_trigger(self):
        pass


    def send_email(self):
        pass

    # output 받기 위한 directory 트리구조 제작
    # [base path] / [city name] / [jpg, mov, hip, usd]
    def mk_dir(self):
        city_dpath = f'{self.__save_path}/{self.__task_type}_{self.lineEdit__city_name.text()}'
        self.lineEdit__open.setText(city_dpath)
        try:
            os.makedirs(city_dpath)
            for form in self.__form.keys():
                fpath = f'{city_dpath}/{form}'
                self.__form[form] = fpath
                if not os.path.exists(fpath):
                    os.makedirs(fpath)
        except OSError:
            print('Cant make dir >> ', )

    # dir dialog 띄우기
    def dir_dialog(self, dir_path, parent=None):
        dirc = QtWidgets.QFileDialog.getOpenFileName(
            self,
            'Open File',
            # dir='/home/rapa/git_workspace/usd_IO/build_data/'
            dir=dir_path
        )
        print(dirc)

    # grid / osm file import 위한 file dialog
    def file_dialog(self, lineedit_type, parent=None):
        files = QtWidgets.QFileDialog.getOpenFileName(
            self,
            caption='Get File',
            # filter='.jpg',
            dir='~/'
        )
        if lineedit_type == 'grid_path':
            self.lineEdit__grid_path.setText(files[0])
            self.lineEdit__osm.setEnabled(0)
            self.toolButton__osm.setEnabled(0)
            self.__task_type = 'grayscale'

        if lineedit_type == 'osm_path':
            self.lineEdit__osm.setText(files[0])
            self.lineEdit__grid_path.setEnabled(0)
            self.toolButton__grid.setEnabled(0)
            self.__task_type = 'osm'

        self.pushButton__start.setEnabled(1)

    # drag and drop 구현
    def slot_drag_drop(self):
        pass




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    citybuild = CityBuilder()
    citybuild.show()
    app.exec_()

