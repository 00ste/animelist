from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QDialogButtonBox

from PyQt5.QtCore import pyqtSignal

class NewDialog(QDialog):
	data_signal = pyqtSignal(str, str, str)

	def __init__(self, mode):
		super().__init__()
		self.initUI(mode)
		self.exec_()
	
	def initUI(self, mode):
		print("EditDialog: initiating UI")

		# SETTING THE TITLE
		if mode == "add":
			self.setWindowTitle("Add new entry")
		elif mode == "edit":
			self.setWindowTitle("Edit entry")
		else:
			self.setWindowTitle("Dialog")

		# SETTING UP THE MAIN GUI
		# LAYOUT
		main_l = QFormLayout(self)

		# INFO LABEL
		if mode == "add":
			title_label = QLabel("Add new entry", self)
		else:
			title_label = QLabel("Edit entry", self)
		main_l.addRow(title_label)

		# FIELDS
		self.title_input = QLineEdit(self)
		main_l.addRow("Title: ", self.title_input)

		self.start_day_input = QLineEdit(self)
		main_l.addRow('Start day: ', self.start_day_input)

		self.end_day_input = QLineEdit(self)
		main_l.addRow('End day: ', self.end_day_input)

		# BUTTONS
		self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		self.buttonBox.accepted.connect(self.ok_pressed)
		self.buttonBox.rejected.connect(self.close)
		main_l.addWidget(self.buttonBox)

		print("EditDialog: configuration ended, now executing")


	def ok_pressed(self):
		print("dialog: ok was pressed")
		self.data_signal.emit(self.title_input.text(), self.start_day_input.text(), self.end_day_input.text())
		print("dialog: data signal was emitted")
		self.accept()