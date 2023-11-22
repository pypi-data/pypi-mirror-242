import qtawesome as qta
from requests import get
import urllib.parse

from PySide6.QtCore import *
from PySide6.QtWidgets import *

from visioncar_polygon_control import profile
from visioncar_polygon_control import decorators

device_icons = {
    "vertical": "fa5s.grip-lines-vertical",
    "square": "fa5.square",
    "hexagon": "mdi6.hexagon-outline",
    "unknown": "fa5s.question",
}


class Device(QWidget):
    disconnected = Signal()

    def __init__(self, name: str, ip: str, port: int):
        QWidget.__init__(self)
        self.name = name
        self.ip = ip
        self.port = port

        if "v-gate" in name:
            self.kind = "vertical"
        elif "sq-gate" in name:
            self.kind = "square"
        elif "hex-gate" in name:
            self.kind = "hexagon"
        else:
            self.kind = "unknown"

        self.icon = qta.icon(device_icons[self.kind])
        self.text_name = self.name.split(".")[0]
        self.addr = f"http://{ip}:{port}"

        info = get(self.addr + "/info").json()
        if "version" not in info or int(info["version"]) < 16:
            raise ValueError("Unsupported HW version")
        self.info = info

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"{self.text_name} (v{self.info['version']})"))

        self.profiles = []
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        id_btn = QPushButton("Identify")
        id_btn.setToolTip("Blink the light to identify it")
        id_btn.clicked.connect(self.identify)
        save_btn = QPushButton("Set as default")
        save_btn.setToolTip("Make device start in the same state as it is now")
        save_btn.clicked.connect(self.save)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(id_btn)
        buttons_layout.addWidget(save_btn)

        buttons = QWidget()
        buttons.setLayout(buttons_layout)
        layout.addWidget(buttons)
        self.setLayout(layout)

        # default: 2 profiles
        self.create_profile(get(self.addr + "/get_params").json())
        self.create_profile({"r": "0", "g": "0", "b": "0"})
        self.tabs.currentChanged.connect(self.switch_profile)
        self.switch_profile(0)

    @Slot()
    def identify(self):
        self.request("/identify")

    @Slot()
    def save(self):
        ret = self.request("/save")
        if ret:
            b = QMessageBox()
            b.setIcon(QMessageBox.Icon.Information)
            b.setText(
                "Saved device preferences, it will start in the same condition")
            b.exec()

    def create_profile(self, kv: dict = {}):
        i = len(self.profiles)
        pr = profile.Profile(self.name, self.kind, kv, self.info)
        pr.updated.connect(lambda k, v: self.update(pr.props()))
        self.profiles.append(pr)
        self.tabs.addTab(pr, f"Profile {i + 1}")

    @Slot(int)
    def switch_profile(self, i: int):
        self.profile = i
        prof = self.profiles[i].props()
        try:
            self.do_update(prof)
        except Exception as err:
            b = QMessageBox()
            b.setIcon(QMessageBox.Icon.Warning)
            b.setText(f"Failed to set profile: {err}")
            b.exec()

    # pass -1 to go backwards
    def next_profile(self, inc: int = 1):
        i = self.profile + inc
        if i < 0:
            i = len(self.profiles) - 1
        if i >= len(self.profiles):
            i = 0
        self.tabs.setCurrentIndex(i)
        self.switch_profile(i)

    @decorators.debounce(0.5)
    def update(self, kv: dict):
        return self.do_update(kv)

    # Undebounced version for immediate changes
    def do_update(self, kv: dict):
        return self.request("/set_params?" + urllib.parse.urlencode(kv))

    def request(self, url: str, throw: bool = False):
        print(url)
        code = 0
        if throw:
            code = get(self.addr + url).status_code
            if code != 200:
                raise ValueError(code)
        else:
            try:
                code = get(self.addr + url).status_code
                if code != 200:
                    raise ValueError(code)
            except Exception as err:
                b = QMessageBox()
                b.setIcon(QMessageBox.Icon.Warning)
                b.setText(f"Failed to send command: {err} {code}")
                b.exec()
                return False
        return True
