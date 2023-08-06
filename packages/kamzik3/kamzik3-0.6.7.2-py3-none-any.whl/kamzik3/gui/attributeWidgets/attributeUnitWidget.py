from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFrame, QComboBox, QLabel, QHBoxLayout
from pint import UndefinedUnitError

from kamzik3 import units
from kamzik3.constants import UNIT
from kamzik3.snippets.snippetsUnits import get_attribute_unit_range
from kamzik3.snippets.snippetsWidgets import clear_layout


class AttributeUnitWidget(QFrame):
    current_unit = None
    sig_unit_changed = pyqtSignal("QString")
    combox = None

    def __init__(self, attribute, config=None, parent=None):
        self.attribute = attribute
        self.config = config
        if self.config is None:
            self.config = {}
        QFrame.__init__(self, parent=parent)
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.set_unit(attribute[UNIT])

    def set_unit(self, unit):
        if self.combox is not None:
            try:
                self.combox.currentTextChanged.disconnect()
            except TypeError:
                pass
            self.combox = None
        clear_layout(self, self.layout())
        self.layout().addWidget(self.get_unit_widget(unit))
        # self.sig_unit_changed.emit(unit)

    def get_unit_widget(self, unit):
        if unit is not None:
            if unit in units.derived_units or self.config.get("static_unit", False):
                return self._get_static_unit_widget(unit)
            else:
                try:
                    return self._get_combox_unit_widget(unit)
                except (UndefinedUnitError, AttributeError, KeyError):
                    return self._get_static_unit_widget(unit)
        else:
            return QLabel(u"")

    def _get_static_unit_widget(self, unit):
        if unit == u"percent":
            unit = u"%"
        return QLabel(u" {}".format(unit))

    def _get_combox_unit_widget(self, unit):
        self.combox = QComboBox()
        self.combox.addItems(
            get_attribute_unit_range(self.attribute)
        )

        # Signal proxy
        self.combox.currentTextChanged.connect(self.sig_unit_changed.emit)
        self.combox.wheelEvent = lambda *args: None
        index = self.combox.findText("{:~}".format(units.Unit(unit)))
        if index == -1:
            self.combox.setCurrentIndex(0)
        else:
            self.combox.setCurrentIndex(index)
        return self.combox

    def close(self):
        self.sig_unit_changed.disconnect()
        clear_layout(self, self.layout())
        self.attribute = None
        self.config = None
