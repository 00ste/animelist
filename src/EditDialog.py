from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QDialogButtonBox

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QDate

from functions import NULLDATE


"""

"""


class EditDialog(QWidget):

	data_signal = pyqtSignal(str, QDate, QDate)
	
	def __init__(self, start_values):
		super().__init__()
		self.initUI(start_values)
		self.show()

	def initUI(self, start_values):
		print("dialog: starting UI init")
		print(len(start_values))

		# SETTING THE TITLE
		if len(start_values) == 0:
			self.setWindowTitle("Add new entry")
		else:
			self.setWindowTitle("Edit entry")

		# SETTING UP THE MAIN GUI
		# LAYOUT
		main_l = QFormLayout(self)

		# INFO LABEL
		if len(start_values) == 0:
			title_label = QLabel("Add new entry", self)
		else:
			title_label = QLabel("Edit entry", self)
		main_l.addRow(title_label)

		# FIELDS
		self.title_input = QLineEdit(self)
		main_l.addRow("Title: ", self.title_input)

		self.start_day_input = QDateEdit(self)
		main_l.addRow('Start day: ', self.start_day_input)

		self.end_day_input = QDateEdit(self)
		self.end_day_input.setEnabled(False)
		main_l.addRow('End day: ', self.end_day_input)

		self.finished_box = QCheckBox(self)
		self.finished_box.setText("Finished")
		self.finished_box.toggled.connect(self.toggle_end_date)
		main_l.addWidget(self.finished_box)		
		
		# BUTTONS
		self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		self.buttonBox.accepted.connect(self.ok_pressed)
		self.buttonBox.rejected.connect(self.close)
		main_l.addWidget(self.buttonBox)

		# START VALUES
		if len(start_values) > 0:									# if there are previous values (edit)
			self.title_input.setText(start_values[0])
			self.start_day_input.setDate(start_values[1])
			if start_values[2] == NULLDATE:							# if the end date is null
				self.end_day_input.setDate(QDate.currentDate())
			else:													# if the end date is set
				self.end_day_input.setDate(start_values[2])
				self.finished_box.setChecked(True)
				self.end_day_input.setEnabled(True)
		else:														# if there are no previous values
			self.start_day_input.setDate(QDate.currentDate())
			self.end_day_input.setDate(QDate.currentDate())
		

	def toggle_end_date(self, state):
		self.end_day_input.setEnabled(state)
		
	def ok_pressed(self):
		print("dialog: ok was pressed")
		if self.finished_box.isChecked():
			print("dialog: checkbox enabled")
			self.data_signal.emit(self.title_input.text(), self.start_day_input.date(), self.end_day_input.date())
		else:
			print("dialog: checkbox disabled")
			self.data_signal.emit(self.title_input.text(), self.start_day_input.date(), NULLDATE)
		print("dialog: data signal was emitted")
		self.close()

"""
video bello su come passare dati tra finestre
https://www.youtube.com/watch?v=wOxzhX0QnAw

playlist bella dello stesso tipo di prima su come usare pyqt5
https://www.youtube.com/playlist?list=PLXlKT56RD3kBu2Wk6ajCTyBMkPIGx7O37
"""