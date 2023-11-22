from PySide6.QtCore import *
from PySide6.QtWidgets import *
import qtawesome as qta


class StartPage(QWidget):
    switch = Signal(str)
    config = Signal(str)
    identify = Signal(str)

    def __init__(self):
        QWidget.__init__(self)

        self.layout = QStackedLayout()

        intro = QWidget()
        intro_layout = QVBoxLayout()
        title = QLabel("Polygon Control")
        title.setStyleSheet("QLabel { font-size: 18pt; }")
        intro_layout.addWidget(title)
        intro_layout.addWidget(
            QLabel("This program allows you to configure networked polygon elements"))
        intro_layout.addWidget(
            QLabel(
                "If you cannot find your devices listed, please check the following steps:"))
        intro_layout.addWidget(QLabel("1. Your devices are powered on"))
        intro_layout.addWidget(
            QLabel("2. They are connected to the same network as your computer"))
        intro_layout.addWidget(
            QLabel("3. Your network and computer do not block mDNS protocol"))

        load_button = QPushButton(" searching")
        load_button.setStyleSheet("border: none; font-size: 50pt")
        load_icon = qta.icon("mdi6.loading",
                             animation=qta.Spin(load_button))
        load_button.setIcon(load_icon)
        load_button.setIconSize(QSize(72, 72))
        load_button.setDisabled(True)
        load_button.setMaximumHeight(150)
        intro_layout.addWidget(load_button, stretch=5)
        intro_layout.addStretch(1)

        license_notice = QLabel(
            "This software includes qt-material, licensed under BSD 2-Clause License, Copyright (c) 2020, GCPDS")
        license_notice.setStyleSheet("QLabel { font-size: 8pt; }")
        intro_layout.addWidget(license_notice)

        about_qt = QLabel(
            "This software is built using PySide6 and Qt6. Click here to get more information about Qt")
        about_qt.setStyleSheet("QLabel { font-size: 8pt; }")
        about_qt.mousePressEvent = lambda _: QApplication.aboutQt()
        intro_layout.addWidget(about_qt)

        mgmt_btn = QPushButton("Manage devices")
        mgmt_btn.pressed.connect(lambda: self.layout.setCurrentIndex(1))
        intro_layout.addWidget(mgmt_btn)

        intro.setLayout(intro_layout)
        self.layout.addWidget(intro)

        mgmt = QWidget()
        mgmt_layout = QVBoxLayout()

        intro_btn = QPushButton("About")
        intro_btn.pressed.connect(lambda: self.layout.setCurrentIndex(0))
        mgmt_layout.addWidget(intro_btn)
        self.dev_layout = QHBoxLayout()
        dev_w = QWidget()
        dev_w.setLayout(self.dev_layout)
        mgmt_layout.addWidget(dev_w)
        mgmt.setLayout(mgmt_layout)
        self.layout.addWidget(mgmt)

        self.layout.setCurrentIndex(0)
        self.setLayout(self.layout)

        self.dev_items = {}

    def add_device(self, name: str, text_name: str):
        l = QVBoxLayout()
        w = QWidget()

        l.addWidget(QLabel(text_name))
        switch_btn = QPushButton("Switch")
        switch_btn.setMaximumHeight(250)
        switch_btn.pressed.connect(lambda: self.switch.emit(name))
        l.addWidget(switch_btn, stretch=1)
        config_btn = QPushButton("Configure")
        config_btn.pressed.connect(lambda: self.config.emit(name))
        l.addWidget(config_btn)
        id_btn = QPushButton("Identify")
        id_btn.pressed.connect(lambda: self.identify.emit(name))
        l.addWidget(id_btn)

        w.setLayout(l)
        self.dev_items[name] = w
        self.dev_layout.addWidget(w)
        self.layout.setCurrentIndex(1)

    def remove_device(self, name: str):
        if name in self.dev_items:
            self.dev_items.pop(name).deleteLater()
