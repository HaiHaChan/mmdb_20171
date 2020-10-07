import sys
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot, QRect, Qt

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
on = True


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        destopSize = QDesktopWidget().screenGeometry()
        w, h = destopSize.width(), destopSize.height()
        self.setGeometry(w / 2 - 300, h / 2 - 250, 700, 500)
        self.setWindowTitle("Face Detection")

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabImage = QWidget()
        self.tabVideo = QWidget()
        self.tabWebcam = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tabImage, "Image")
        self.tabs.addTab(self.tabVideo, "Video")
        self.tabs.addTab(self.tabWebcam, "Webcam")

        # Create TAB IMAGE
        # Create textbox to get path of image
        self.imagePathI = QLineEdit(self.tabImage)
        self.imagePathI.setGeometry(QRect(20, 30, 450, 30))

        # Create load Button to load image
        self.loadButtonI = QPushButton("Load", self.tabImage)
        self.loadButtonI.setGeometry(QRect(500, 30, 100, 30))
        self.loadButtonI.clicked.connect(self.loadImage)

        # Create box to show image
        self.imageView = QGraphicsView(self.tabImage)
        self.imageView.setGeometry(QRect(20, 80, 450, 360))

        # Create form to get parametes
        self.scaleLabelI = QLabel("Scale Factor:", self.tabImage)
        self.scaleLabelI.setGeometry(QRect(500, 200, 100, 30))
        self.scaleSpinBoxI = QDoubleSpinBox(self.tabImage)
        self.scaleSpinBoxI.setGeometry(QRect(600, 200, 50, 30))
        self.scaleSpinBoxI.setDecimals(1)
        self.scaleSpinBoxI.setMinimum(1.1)
        self.scaleSpinBoxI.setMaximum(2.0)
        self.scaleSpinBoxI.setSingleStep(0.1)

        self.MinNeighborLabelI = QLabel("Min Neighbor:", self.tabImage)
        self.MinNeighborLabelI.setGeometry(QRect(500, 300, 100, 30))
        self.minNeighborSpinBoxI = QSpinBox(self.tabImage)
        self.minNeighborSpinBoxI.setGeometry(QRect(600, 300, 50, 30))
        self.minNeighborSpinBoxI.setMinimum(1)
        self.minNeighborSpinBoxI.setMaximum(50)

        # Create button to Detect
        self.detectButtonI = QPushButton("Detect", self.tabImage)
        self.detectButtonI.setGeometry(QRect(550, 400, 100, 30))
        self.detectButtonI.clicked.connect(self.detectOfImage)
        # END IMAGE TAB

        # Create VIDEO TAB
        # Create textbox to get path of video
        self.videoPath = QLineEdit(self.tabVideo)
        self.videoPath.setGeometry(QRect(20, 30, 450, 30))

        # Create load Button to load video
        self.loadButtonV = QPushButton("Load", self.tabVideo)
        self.loadButtonV.setGeometry(QRect(500, 30, 100, 30))
        self.loadButtonV.clicked.connect(self.loadVideo)

        # Create box to show video
        self.videoView = QGraphicsView(self.tabVideo)
        self.videoView.setGeometry(QRect(20, 80, 450, 360))

        # Create form to get parametes
        self.scaleLabelV = QLabel("Scale Factor:", self.tabVideo)
        self.scaleLabelV.setGeometry(QRect(500, 100, 100, 30))
        self.scaleSpinBoxV = QDoubleSpinBox(self.tabVideo)
        self.scaleSpinBoxV.setGeometry(QRect(600, 100, 50, 30))
        self.scaleSpinBoxV.setDecimals(1)
        self.scaleSpinBoxV.setMinimum(1.1)
        self.scaleSpinBoxV.setMaximum(2.0)
        self.scaleSpinBoxV.setSingleStep(0.1)

        self.MinNeighborLabelV = QLabel("Min Neighbor:", self.tabVideo)
        self.MinNeighborLabelV.setGeometry(QRect(500, 200, 100, 30))
        self.minNeighborSpinBoxV = QSpinBox(self.tabVideo)
        self.minNeighborSpinBoxV.setGeometry(QRect(600, 200, 50, 30))
        self.minNeighborSpinBoxV.setMinimum(1)
        self.minNeighborSpinBoxV.setMaximum(50)

        # Create button to start or stop video
        self.startButton = QPushButton("Start", self.tabVideo)
        self.startButton.setGeometry(QRect(500, 300, 100, 30))
        self.startButton.clicked.connect(self.startVideo)
        self.stopButton = QPushButton("Stop", self.tabVideo)
        self.stopButton.setGeometry(QRect(500, 400, 100, 30))
        self.stopButton.clicked.connect(self.stopVideo)
        # END VIDEO TAB

        # Create WEBCAM TAB
        # Create box to show video
        self.camView = QGraphicsView(self.tabWebcam)
        self.camView.setGeometry(QRect(20, 30, 600, 350))

        # Create form to get parametes
        self.scaleLabel = QLabel("Scale Factor:", self.tabWebcam)
        self.scaleLabel.setGeometry(QRect(30, 400, 100, 30))
        self.scaleSpinBox = QDoubleSpinBox(self.tabWebcam)
        self.scaleSpinBox.setGeometry(QRect(100, 400, 50, 30))
        self.scaleSpinBox.setDecimals(1)
        self.scaleSpinBox.setMinimum(1.1)
        self.scaleSpinBox.setMaximum(2.0)
        self.scaleSpinBox.setSingleStep(0.1)

        self.MinNeighborLabel = QLabel("Min Neighbor:", self.tabWebcam)
        self.MinNeighborLabel.setGeometry(QRect(200, 400, 100, 30))
        self.minNeighborSpinBox = QSpinBox(self.tabWebcam)
        self.minNeighborSpinBox.setGeometry(QRect(280, 400, 50, 30))
        self.minNeighborSpinBox.setMinimum(1)
        self.minNeighborSpinBox.setMaximum(50)

        # Create button to turn on  or turn off webcam
        self.turnOnButton = QPushButton("On", self.tabWebcam)
        self.turnOnButton.setGeometry(QRect(450, 400, 80, 30))
        self.turnOnButton.clicked.connect(self.turnOn)
        self.turnOffButton = QPushButton("Off", self.tabWebcam)
        self.turnOffButton.setGeometry(QRect(550, 400, 80, 30))
        self.turnOffButton.clicked.connect(self.turnOff)
        self.turnOnButton = QPushButton("Cancel", self.tabWebcam)
        self.turnOnButton.setGeometry(QRect(600, 400, 80, 30))
        self.turnOnButton.clicked.connect(self.turnCancel)
        # END WEBCAM TAB

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    @pyqtSlot()
    def loadImage(self):
        dialog = QFileDialog()
        folder_path, _ = dialog.getOpenFileName(options=QFileDialog.Options())
        self.imagePathI.setText(folder_path)
        image_reader = QImageReader(self.imagePathI.text())
        print(folder_path)
        if image_reader.canRead() is True:
            widget_height = self.imageView.height()
            widget_width = self.imageView.width()
            image = image_reader.read().scaled(widget_width, widget_height, Qt.KeepAspectRatio)
            item = QGraphicsPixmapItem(QPixmap.fromImage(image))
            scene = QGraphicsScene()
            scene.addItem(item)
            self.imageView.setScene(scene)
        else:
            scene = QGraphicsScene()
            self.imageView.setScene(scene)

    def loadVideo(self):
        dialog = QFileDialog()
        folder_path, _ = dialog.getOpenFileName(options=QFileDialog.Options())
        self.videoPath.setText(folder_path)

    def detectOfImage(self):
        path = self.imagePathI.text()
        s = self.scaleSpinBoxI.value()
        m = self.minNeighborSpinBoxI.value()
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, s, m)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.imwrite('result.png', img)
        cv2.imshow('img', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # self.detect_face(path,"a",s,m)

    def startVideo(self):
        self.on = True
        s = self.scaleSpinBoxV.value()
        m = self.minNeighborSpinBoxV.value()
        video = cv2.VideoCapture(self.videoPath.text())

        while (video.isOpened()):

            ret, frame = video.read()
            try:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            except:
                print("exception")
                break
            faces = face_cascade.detectMultiScale(gray, s, m)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imshow('Video', frame)
            cv2.imwrite('tempVideo.png', frame)

            image_reader = QImageReader("tempVideo.png")
            if image_reader.canRead() is True:
                widget_height = self.videoView.height()
                widget_width = self.videoView.width()
                image = image_reader.read().scaled(widget_width, widget_height, Qt.KeepAspectRatio)
                item = QGraphicsPixmapItem(QPixmap.fromImage(image))
                scene = QGraphicsScene()
                scene.addItem(item)
                self.videoView.setScene(scene)
            else:
                scene = QGraphicsScene()
                self.videoView.setScene(scene)

            if cv2.waitKey(1) & 0xFF == ord('q') or (self.on == False):
                break

        video.release()
        cv2.destroyAllWindows()

    def stopVideo(self):
        self.on = False

    def turnOn(self):
        self.on = True
        s = self.scaleSpinBox.value()
        m = self.minNeighborSpinBox.value()
        cap = cv2.VideoCapture(0)
        while (self.on):
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, s, m)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.imshow('Webcam', img)

            cv2.imwrite('tempCap.png', img)

            image_reader = QImageReader("tempCap.png")
            if image_reader.canRead() is True:
                widget_height = self.camView.height()
                widget_width = self.camView.width()
                image = image_reader.read().scaled(widget_width, widget_height, Qt.KeepAspectRatio)
                item = QGraphicsPixmapItem(QPixmap.fromImage(image))
                scene = QGraphicsScene()
                scene.addItem(item)
                self.camView.setScene(scene)
            else:
                scene = QGraphicsScene()
                self.camView.setScene(scene)
            if (cv2.waitKey(1) & 0xFF == ord('q')) or (self.on == False):
                break
        cap.release()
        cv2.destroyAllWindows()

    def turnOff(self):
        self.on = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
