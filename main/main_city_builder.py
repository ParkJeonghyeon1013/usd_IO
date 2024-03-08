import importlib, typing
import pathlib

from PySide2 import QtCore, QtGui, QtWidgets

# from main.resource.ui.sample_window4_ui import Ui_MainWindow
from main.resource.ui.sample_window5_ui import Ui_MainWindow
# from main.libs import api_osm, api_grayscale, api_hou

# importlib.reload(Ui_MainWindow)

'''

'''
class LineEdit:
    grid_path = 'lineEdit__grid_path'
    osm_path = 'lineEdit__osm_path'


class CityBuilder(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parnet=None):
        super().__init__(parnet)
        # variable
        self.__grid_path = ''
        self.__osm_path = ''



        self.setupUi(self)
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
        pass

    def __connection(self):
        self.toolButton__gird_path.clicked.connect(lambda x: self.file_dialog('grid_path'))
        self.toolButton__osm.clicked.connect(lambda x: self.file_dialog('osm_path'))
        self.toolButton__save.clicked.connect(lambda x: self.dir_dialog('location'))


    def dir_dialog(self, lineedit_type, parent=None):
        dirc = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            'Get Directory',
            '/home/rapa/git_workspace/usd_IO/build_data/'
        )
        if lineedit_type is 'location':
            print(dirc)
            self.lineEdit__save.setText(dirc)


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


        if lineedit_type == 'osm_path':
            self.lineEdit__osm.setText(files[0])
            self.lineEdit__grid_path.setEnabled(0)
            self.toolButton__grid.setEnabled(0)

    def slot_drag_drop(self):
        pass

    def slot_btn_start(self):
        # self.progressBar.setValue()
        print('progress bar setting 해주기 ')



if __name__ == '__main__':
    app = QtWidgets.QApplication()
    citybuild = CityBuilder()
    citybuild.show()
    app.exec_()




