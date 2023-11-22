from PySide6.QtCore import *
from PySide6.QtWidgets import *
import qtawesome as qta

from visioncar_polygon_control import colorselect

default_kv = {
    "r": "0",
    "g": "255",
    "b": "255",
    "r2": "0",
    "g2": "0",
    "b2": "0",
    "animation": "0",
    "on_time": "500",
    "off_time": "500",
    "tr_time": "20",
    "dot": "1",
    "offset": "0",
    "speed": "0",
}


class Profile(QWidget):
    updated = Signal(str, str)

    def __init__(self, name: str, kind: str, kv: dict = {}, info: dict = {}):
        QWidget.__init__(self)
        self.name = name
        self.kind = kind
        self.info = info
        self.kv = {**default_kv, **kv}

        layout = QVBoxLayout()

        color_sel = colorselect.ColorSelect(
            f"rgb({self.kv['r']}, {self.kv['g']}, {self.kv['b']})")
        color_sel.updated.connect(self.set_color)
        layout.addWidget(QLabel("Color:"))
        layout.addWidget(color_sel)

        anim = QComboBox()
        # Order must match one in FW
        anim.addItem(qta.icon("mdi6.current-dc"), "Still light")
        anim.addItem(qta.icon("mdi6.square-wave"), "Blink")
        if int(info["version"]) >= 17:
            anim.addItem(qta.icon("mdi6.sine-wave"), "Fade")
        if int(info["version"]) >= 19:
            anim.addItem(qta.icon("mdi6.dots-horizontal"), "Dotted")
        anim.setCurrentIndex(int(self.kv["animation"]))
        anim.currentIndexChanged.connect(self.set_anim)
        layout.addWidget(anim)

        if int(info["version"]) >= 18:
            self.bg_sel = colorselect.ColorSelect(
                f"rgb({self.kv['r2']}, {self.kv['g2']}, {self.kv['b2']})")
            self.bg_sel.updated.connect(self.set_bg)
            self.bg_label = QLabel("Background (off) color:")
            layout.addWidget(self.bg_label)
            layout.addWidget(self.bg_sel)

        self.times = QWidget()
        times_layout = QHBoxLayout()

        on_widget = QWidget()
        on_layout = QVBoxLayout()
        on_layout.addWidget(QLabel("On time:"))
        on = QSpinBox()
        on.setRange(50, 600000)
        on.setSingleStep(250)
        on.setSuffix("ms")
        on.setValue(int(self.kv["on_time"]))
        on.valueChanged.connect(lambda x: self.update("on_time", str(x)))
        on_layout.addWidget(on)
        on_widget.setLayout(on_layout)
        times_layout.addWidget(on_widget)

        off_widget = QWidget()
        off_layout = QVBoxLayout()
        off_layout.addWidget(QLabel("Off time:"))
        off = QSpinBox()
        off.setRange(50, 600000)
        off.setSingleStep(250)
        off.setSuffix("ms")
        off.setValue(int(self.kv["off_time"]))
        off.valueChanged.connect(lambda x: self.update("off_time", str(x)))
        off_layout.addWidget(off)
        off_widget.setLayout(off_layout)
        times_layout.addWidget(off_widget)

        self.tr_widget = QWidget()
        tr_layout = QVBoxLayout()
        tr_layout.addWidget(QLabel("Transition time:"))
        tr = QSpinBox()
        tr.setRange(0, 600000)
        tr.setSingleStep(10)
        tr.setSuffix("ms")
        tr.setValue(int(self.kv["tr_time"]))
        tr.valueChanged.connect(lambda x: self.update("tr_time", str(x)))
        tr_layout.addWidget(tr)
        self.tr_widget.setLayout(tr_layout)
        times_layout.addWidget(self.tr_widget)

        if self.kv["animation"] not in ["1", "2"]:
            self.times.hide()

        if self.kv["animation"] != "2":
            self.tr_widget.hide()

        self.times.setLayout(times_layout)
        layout.addWidget(self.times)

        dots_layout = QHBoxLayout()

        dot_widget = QWidget()
        dot_layout = QVBoxLayout()
        dot_layout.addWidget(QLabel("Dot size:"))
        dot = QSpinBox()
        dot.setRange(1, 60)
        dot.setValue(int(self.kv["dot"]))
        dot.valueChanged.connect(lambda x: self.update("dot", str(x)))
        dot_layout.addWidget(dot)
        dot_widget.setLayout(dot_layout)
        dots_layout.addWidget(dot_widget)

        offset_widget = QWidget()
        offset_layout = QVBoxLayout()
        offset_layout.addWidget(QLabel("Dot offset:"))
        offset = QSpinBox()
        offset.setRange(0, 60)
        offset.setValue(int(self.kv["offset"]))
        offset.valueChanged.connect(lambda x: self.update("offset", str(x)))
        offset_layout.addWidget(offset)
        offset_widget.setLayout(offset_layout)
        dots_layout.addWidget(offset_widget)

        speed_widget = QWidget()
        speed_layout = QVBoxLayout()
        speed_layout.addWidget(QLabel("Movement time (0 to stop):"))
        speed = QSpinBox()
        speed.setRange(-5000, 5000)
        speed.setSingleStep(25)
        speed.setSuffix("ms")
        speed.setValue(int(self.kv["speed"]))
        speed.valueChanged.connect(lambda x: self.update("speed", str(x)))
        speed_layout.addWidget(speed)
        speed_widget.setLayout(speed_layout)
        if int(info["version"]) >= 20:
            dots_layout.addWidget(speed_widget)

        self.dots = QWidget()
        self.dots.setLayout(dots_layout)
        layout.addWidget(self.dots)

        if self.kv["animation"] == "0":
            self.bg_sel.hide()
            self.bg_label.hide()

        if self.kv["animation"] != "3":
            self.dots.hide()

        self.setLayout(layout)

    def set_anim(self, v):
        v = str(v)

        if v == "0":
            self.bg_sel.hide()
            self.bg_label.hide()
        else:
            self.bg_sel.show()
            self.bg_label.show()

        if v in ["1", "2"]:
            self.times.show()
        else:
            self.times.hide()

        if v == "2":
            self.tr_widget.show()
        else:
            self.tr_widget.hide()

        if v == "3":
            self.dots.show()
        else:
            self.dots.hide()

        self.update("animation", v)

    def set_color(self, r, g, b):
        self.update("r", str(r))
        self.update("g", str(g))
        self.update("b", str(b))

    def set_bg(self, r, g, b):
        self.update("r2", str(r))
        self.update("g2", str(g))
        self.update("b2", str(b))

    def update(self, k, v):
        self.kv[k] = v
        self.updated.emit(k, v)

    def props(self):
        return self.kv
