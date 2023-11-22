from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class ColorSelect(QWidget):
    updated = Signal(int, int, int)

    def __init__(self, value: str):
        QWidget.__init__(self)
        self.value = value

        layout = QHBoxLayout()

        btn = QPushButton("Select color")
        btn.pressed.connect(self.clicked)
        layout.addWidget(btn)

        self.swatch = QPushButton("")
        self.swatch.setStyleSheet("background-color: %s;" % self.value)
        layout.addWidget(self.swatch)

        self.setLayout(layout)

    @Slot()
    def clicked(self):
        w = QColorDialog(self)
        w.setCurrentColor(QColor(self.value))

        if w.exec():
            self.value = w.currentColor().name()
            qc = QColor(self.value)
            self.updated.emit(qc.red(), qc.green(), qc.blue())
            self.swatch.setStyleSheet("background-color: %s;" % self.value)
