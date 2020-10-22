from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QMessageBox
from ...buttons.data_group_buttons import DataGroupButtons  # pylint: disable=E0402
from ...dialogs.data_dialog import DataDialog  # pylint: disable=E0402
from ...tables.data_table import DataTable  # pylint: disable=E0402


class DataSettingsWidget(QWidget):

    addDatasetSignal = pyqtSignal(str, str)
    deleteDatasetSignal = pyqtSignal(list)
    changeDatasetSignal = pyqtSignal(int, str, str)
    clearSignal = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        layouts = QHBoxLayout()
        self.__table = DataTable(self)
        self.__buttons = DataGroupButtons(self)
        layouts.addWidget(self.__table)
        layouts.addWidget(self.__buttons)
        self.setLayout(layouts)
        self.__set_connections()

    def __set_connections(self):
        self.__buttons.get_buttons()['Add information'].clicked.connect(self.__show_dialog_add_dataset)
        self.__buttons.get_buttons()['Delete information'].clicked.connect(self.__click_delete_button)
        self.__buttons.get_buttons()['Change information'].clicked.connect(self.__show_dialog_change_dataset)
        self.__buttons.get_buttons()['Clear table'].clicked.connect(self.clearSignal.emit)

    def __show_dialog_add_dataset(self):
        dialog = DataDialog(self)
        if dialog.exec():
            self.addDatasetSignal.emit(*dialog.get_values())

    def __show_dialog_change_dataset(self):
        if len(self.__table.get_selected_rows()) != 1:
            QMessageBox.warning(self, "Warning!", "Choose one row!")
            return
        dialog = DataDialog(self)
        row = self.__table.get_selected_rows()[0]
        idx = 0
        for tag in dialog.tags:
            dialog.edits[tag].setText(self.__table.item(row, idx).text())
            idx += 1
        if dialog.exec():
            self.changeComputerSignal.emit(row, *dialog.get_values())
        self.__table.remove_selection()

    def __click_delete_button(self):
        self.delDatasetSignal.emit(self.__table.get_selected_rows())
        self.__table.remove_selection()

    def get_selected_rows(self):
        return self.__table.get_selected_rows()

    def update(self, model):
        self.__table.update(model.get_data())
