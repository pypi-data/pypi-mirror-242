import asyncio
import time
import signal
import sys
import zeroconf

from PySide6.QtCore import *
from PySide6.QtWidgets import *
import qt_material
import qtawesome as qta

from visioncar_polygon_control import device
from visioncar_polygon_control import startpage


class AppMain(QWidget, zeroconf.ServiceListener):
    def __init__(self):
        QWidget.__init__(self)
        self.resize(600, 400)
        self.setWindowTitle("Polygon Control")
        self.setWindowIcon(qta.icon("mdi6.lightbulb-on-outline"))

        self.tabs = QTabWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)

        self.setLayout(layout)

        self.dev = {}
        self.dev_tabs = {}

        self.start_page = startpage.StartPage()
        self.tabs.addTab(self.start_page, qta.icon(
            "mdi6.view-dashboard-variant"), "Start")
        self.start_page.switch.connect(lambda x: self.dev[x].next_profile())
        self.start_page.config.connect(
            lambda x: self.tabs.setCurrentIndex(
                self.dev_tabs[x]))
        self.start_page.identify.connect(lambda x: self.dev[x].identify())

    @Slot(str, str, int)
    def add(self, name: str, ip: str, port: int):
        dev = device.Device(name, ip, port)
        self.dev_tabs[name] = self.tabs.addTab(dev, dev.icon, dev.text_name)
        dev.disconnected.connect(lambda: self.remove(name))
        self.dev[name] = dev
        self.start_page.add_device(name, dev.text_name)

    @Slot(str)
    def remove(self, name: str):
        if name in self.dev:
            del self.dev[name]
        if name in self.dev_tabs:
            self.tabs.removeTab(self.dev_tabs.pop(name))
        self.start_page.remove_device(name)

    def add_service(self, zc: zeroconf.Zeroconf, type_: str, name: str):
        time.sleep(0.5)  # Let device become ready

        info = zc.get_service_info(type_, name)
        if info:
            ip = info.addresses[0]
            QMetaObject.invokeMethod(
                self,
                "add",
                Qt.QueuedConnection,
                Q_ARG(str, name),
                Q_ARG(str, f"{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}"),
                Q_ARG(int, info.port)
            )

    def update_service(self, zc: zeroconf.Zeroconf, type_: str, name: str):
        pass

    def remove_service(self, zc_, type_, name: str):
        QMetaObject.invokeMethod(
            self,
            "remove",
            Qt.QueuedConnection,
            Q_ARG(
                str,
                name))

def run():
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    qt_material.apply_stylesheet(app, theme='dark_teal.xml')

    app_main = AppMain()
    zc = zeroconf.Zeroconf()
    zeroconf.ServiceBrowser(zc, "_v-gate._tcp.local.", app_main)
    zeroconf.ServiceBrowser(zc, "_sq-gate._tcp.local.", app_main)
    zeroconf.ServiceBrowser(zc, "_hex-gate._tcp.local.", app_main)
    app_main.show()

    app.exec()
    zc.close()
