import sys
import PySide6
from PySide6 import QtCore, QtGui
from PySide6.QtGui import QBrush, QPainter
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QInputDialog
from backends.mouse_action import TimeRecord, PositionalRecord
import time 
class MainApp(QMainWindow):
# class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.time_recorder = TimeRecord()
        self.position_recorder = PositionalRecord()
        self.current_point = None
        self.displayed_points = []
        self.timing = []
        self.paint_mode = False
        self.n_paints = 0
        self.initUI()
        
    
    def initUI(self):
        self.setWindowTitle("Mouse-Macro v.0.1")
        self.move(0,0)
        self.setTimer=QInputDialog(self)
        self.resetPosBtn = QPushButton("Reset Positions", self)
        self.resetPosBtn.setCheckable(True)
        self.resetPosBtn.move(0,25)
        self.submitBtn = QPushButton("Submit", self)
        self.submitBtn.setCheckable(True)
        self.submitBtn.move(0,50)

        self.setMouseTracking(True)

        # Display Mouse Track
        self.submitBtn.clicked.connect(self.submitEvent)
        self.resetPosBtn.clicked.connect(self.resetPoseEvent)


        self.setWindowOpacity(0.2)
        self.showMaximized()
        # self.showFullScreen()
        # self.show()

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        if event.type() == QtCore.QEvent.MouseButtonPress:

            if event.button() == QtCore.Qt.RightButton:
                self.position_recorder.record()
                self.paint_mode = True
                self.n_paints += 1 
                self.update()
            return super().mousePressEvent(event)

    def paintEvent(self, event: PySide6.QtGui.QPaintEvent) -> None:
        if self.paint_mode :
            self.displayed_points.append(self.current_point)
            painter=QPainter()
            painter.begin(self)
            displayed_x, displayed_y = self.displayed_points[-1]
            x_pose, y_pose = self.position_recorder.records[-1]
            print(self.position_recorder.records)
            print(self.displayed_points)
            brush = QBrush('black',QtCore.Qt.BrushStyle.SolidPattern)#QtCore.SolidPattern)
            painter.setBrush(brush)
            # painter.drawRect(x_pose-1, y_pose-1, 5, 5)
            painter.drawRect(displayed_x-1, displayed_y-1, 5, 5)
            painter.end()
            # painter.begin(self)
            # self.drawRect(painter)
            # painter.end()
            self.paint_mode = False

    def mouseMoveEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        self.current_point = [event.x(), event.y()]
        return super().mouseMoveEvent(event)

    def clearMarkerEvent(self):
        pass
    def submitEvent(self):
        self.resetPosBtn.toggle()
        pass

    def resetInputEvent(self):
        pass
    def resetPoseEvent(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainApp()
    sys.exit(app.exec())