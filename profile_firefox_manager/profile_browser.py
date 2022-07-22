import sys
import threading
import math

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from profile_firefox_manager.file_profile_firefox import FileProfileFirefox
from profile_firefox_manager.profile_browser_form import Ui_profileBrowser


def thread(my_func):

    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=my_func, args=args, kwargs=kwargs)
        my_thread.start()

    return wrapper


class Overlay(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        palette = QPalette(self.palette())
        palette.setColor(palette.Background, Qt.transparent)
        self.setPalette(palette)
        self.setGeometry(parent.childrenRect())

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.fillRect(event.rect(), QBrush(QColor(255, 255, 255, 127)))
        painter.setPen(QPen(Qt.NoPen))

        for i in range(6):
            if self.counter % 6 == i:

                painter.setBrush(QBrush(QColor(255, 127, 127)))
            else:
                painter.setBrush(QBrush(QColor(127, 127, 127)))
            painter.drawEllipse(
                int(self.width() / 2 + 30 * math.cos(2 * math.pi * i / 6.0) - 10),
                int(self.height() / 2 + 30 * math.sin(2 * math.pi * i / 6.0) - 10),
                20, 20)

        painter.end()

    def showEvent(self, event):
        self.timer = self.startTimer(500)
        self.counter = 0

    def kill(self):
        self.killTimer(self.timer)
        self.hide()

    def timerEvent(self, event):
        self.counter += 1
        self.update()


class ProfileBrowser(QMainWindow, Ui_profileBrowser):

    _signal_kill_overlay = Signal(str, name='_signal_kill_overlay')
    _signal_show_title = Signal(str, name='_signal_show_title')

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.tableProfile.setColumnCount(2)

        self.tableProfile.clicked.connect(lambda: self._set_selection())

        self.editSearch.textChanged.connect(lambda: self._filling_table())

        self.buttSave.clicked.connect(self._save)

        self.buttDown.clicked.connect(self._down)
        self.buttUp.clicked.connect(self._up)

        self.buttImport.clicked.connect(self._import)
        self.buttExport.clicked.connect(self._export)
        self.buttClearSelection.clicked.connect(lambda: (self.cfg_prof.clear_selection(), self._filling_table()))

        self.buttEnableProxy.clicked.connect(self._enable_proxy)
        self.buttDisableProxy.clicked.connect(lambda: self.cfg_prof.disable_proxy())

        self.cfg_prof = FileProfileFirefox()
        self._filling_table()

        self._signal_kill_overlay.connect(self._kill_overlay, Qt.QueuedConnection)
        self._signal_show_title.connect(self.setWindowTitle, Qt.QueuedConnection)

    def _start_overlay(self):
        self.overlay = Overlay(self.centralwidget)
        self.overlay.show()

    def _kill_overlay(self, data):
        if data is None or data == "":
            self.setWindowTitle('Profile Browser')
        else:
            self.setWindowTitle(data)
        self.overlay.kill()
        self._filling_table()

    def _show_message(self, text: str, title: str = "Warning"):
        self._message_box = QMessageBox()
        self._message_box.setText(str(text))
        self._message_box.setWindowTitle(str(title))
        self._message_box.setStandardButtons(QMessageBox.Ok)
        self._message_box.show()

    def _enable_proxy(self):
        ip, ok = QInputDialog.getText(self, 'Setting proxy server', 'Enter ip:port:')
        if ok:
            self.cfg_prof.enable_proxy(ip.split(":")[0], int(ip.split(":")[1]))

    def _import(self):
        self._start_overlay()
        t_import_folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        print(t_import_folder)
        self._import_processing(t_import_folder, self._signal_kill_overlay, self._signal_show_title)

    @thread
    def _import_processing(self, import_folder: str, signal_end, signal_show):
        try:
            self.cfg_prof.import_profile(import_folder, signal_show)
        except Exception as E:
            signal_end.emit("Error import")
            return

        signal_end.emit("")

    def _export(self):
        if len(self.cfg_prof.only_selection()) == 0:
            self._show_message("Not selected profile")
            return

        self._start_overlay()
        t_export_folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        print(t_export_folder)
        self._export_processing(t_export_folder, self._signal_kill_overlay, self._signal_show_title)

    @thread
    def _export_processing(self, export_folder: str, signal_end, signal_show):
        self.cfg_prof.export_profile(export_folder, signal_show)
        signal_end.emit("")

    def _save(self):
        self.cfg_prof.save()
        self._filling_table()

    def _set_selection(self):
        for prof in self.cfg_prof:
            prof.selected = False

        for el in self.tableProfile.selectedItems():
            self.cfg_prof[el.row()].selected = True

    def _get_selected(self):
        t_result = []
        for el in self.tableProfile.selectedRanges():
            t_result.append(el.topRow())
        return t_result

    def _up(self):
        t_index_selected: list = self._get_selected()
        for index in t_index_selected:
            if index != 0:
                self.cfg_prof[index], self.cfg_prof[index-1] = self.cfg_prof[index-1], self.cfg_prof[index]
            else:
                break
        self._filling_table()

    def _down(self):
        t_index_selected: list = self._get_selected()
        t_index_selected.reverse()
        for index in t_index_selected:
            if index < len(self.cfg_prof)-1:
                self.cfg_prof[index+1], self.cfg_prof[index] = self.cfg_prof[index], self.cfg_prof[index+1]
            else:
                break
        self._filling_table()

    def _filling_table(self):
        self.cfg_prof.filling(self.editSearch.text())

        self.tableProfile.setRowCount(len(self.cfg_prof))

        for num, prof in enumerate(list(self.cfg_prof)):
            self.tableProfile.setItem(num, 0, QTableWidgetItem(str(prof.index)))
            self.tableProfile.setItem(num, 1, QTableWidgetItem(prof.name))
            if prof.selected:
                self.tableProfile.setRangeSelected(QTableWidgetSelectionRange(num, 0, num, 1), True)
            else:
                self.tableProfile.setRangeSelected(QTableWidgetSelectionRange(num, 0, num, 1), False)

        self.tableProfile.resizeColumnsToContents()


def main():
    app = QApplication(sys.argv)
    window = ProfileBrowser()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
