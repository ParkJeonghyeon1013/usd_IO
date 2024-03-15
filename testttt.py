from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent
from PySide2 import QtCore

class VideoWidget(QWidget):
    def __init__(self):
        super().__init__()

        # QMediaPlayer 및 QVideoWidget 생성
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget()

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)
        self.setLayout(layout)

        # 동영상 파일 경로 설정
        video_path = r"D:\git_workspace\usd_IO\resource\seq_sample\output.mov"

        # url = QtCore.QUrl.fromLocalFile(finfo.absoluteFilePath(fpath))

        media_content = QtCore.QUrl.fromLocalFile(video_path)
        self.media_player.setMedia(media_content)

        # 비디오 위젯에 레이아웃 설정
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.play()

if __name__ == '__main__':
    app = QApplication([])
    window = VideoWidget()
    window.show()
    app.exec_()
