import sys
from tkinter.tix import ButtonBox
import PySide6
from PySide6 import (QtCore, 
                    QtGui)
from PySide6.QtGui import (QBrush, 
                          QPainter)
from PySide6.QtWidgets import (QApplication,
                              QDialog,
                              QWidget,
                              QDialogButtonBox,
                              QMainWindow, 
                              QPushButton, 
                              QInputDialog,
                              QVBoxLayout,
                              QFormLayout,
                              QLineEdit)
from backends.mouse_action import (TimeRecord, 
                                PositionalRecord)
from typing import Optional

import time 

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.time_recorder = TimeRecord()
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
        
        self.controllerBtn = QPushButton("Control Box", self)
        self.controllerBtn.setCheckable(True)
        self.controllerBtn.move(0, 25)

        self.resetPosBtn = QPushButton("Reset Positions", self)
        self.resetPosBtn.setCheckable(True)
        self.resetPosBtn.move(0, 50)

        self.submitBtn = QPushButton("Submit", self)
        self.submitBtn.setCheckable(True)
        self.submitBtn.move(0, 75)

        # self.layout_button = QVBoxLayout()
        # self.layout_button.setAlignment(QtCore.Qt.AlignRight)
        # self.layout_button.addWidget(self.resetPosBtn, alignment=QtCore.Qt.AlignRight)
        # self.layout_button.addWidget(self.submitBtn, alignment=QtCore.Qt.AlignRight)
        # self.setLayout(self.layout_button)
        self.setMouseTracking(True)

        # Display Mouse Track
        self.submitBtn.clicked.connect(self.submitEvent)
        self.resetPosBtn.clicked.connect(self.resetPoseEvent)
        self.controllerBtn.clicked.connect(self.popupController)

        self.setWindowOpacity(0.5)
        self.showMaximized()

    def popupController(self):
        dialog = ControlInputDialog(self)
        dialog.exec()
        self.time_inputs = dialog.getInputs()
        # controlWindow.setWindowTitle("controller")

        # controlWindow.exec()
        pass

    def mousePressEvent(self, 
                        event: PySide6.QtGui.QMouseEvent) -> None:
        if event.type() == QtCore.QEvent.MouseButtonPress:

            if event.button() == QtCore.Qt.RightButton:
                self.position_recorder.record()
                self.paint_mode = True
                self.n_paints += 1 
                self.update()
            return super().mousePressEvent(event)

    def paintEvent(self, 
                   event: PySide6.QtGui.QPaintEvent) -> None:
        if self.paint_mode :
            self.displayed_points.append(self.current_point)
            painter=QPainter()
            painter.begin(self)
            displayed_x, displayed_y = self.displayed_points[-1]
            x_pose, y_pose = self.position_recorder.records[-1]
            print(self.position_recorder.records)
            print(self.displayed_points)
            brush = QBrush('red', QtCore.Qt.BrushStyle.SolidPattern)
            painter.setBrush(brush)
            painter.drawRect(displayed_x-5,displayed_y-5, 10, 10)
            painter.end()
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

class ControlInputDialog(QDialog):
    def __init__(self,
                parent: Optional[PySide6.QtWidgets.QWidget] = ...,) -> None:
        super().__init__(parent)

        self.target_time = QLineEdit(self)
        self.sec_delay = QLineEdit(self)
        self.milisec_delay = QLineEdit(self)
        self.loop_delay = QLineEdit(self)
    
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

        layout = QFormLayout(self)
        layout.addRow("Target Time (HH:MM, ex: 2200)", self.target_time)
        layout.addRow("sd: Second_delay (0~59)", self.sec_delay)
        layout.addRow("md: milisecond_delay", self.milisec_delay)
        layout.addRow("ld: loop_delay", self.loop_delay)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return (self.target_time.text(), 
                self.sec_delay.text(), 
                self.milisec_delay.text(), 
                self.loop_delay.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainApp()
    sys.exit(app.exec())