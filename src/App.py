from http.client import ACCEPTED
import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QDate

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog

from PyQt5.QtGui import QIcon

from EditDialog import EditDialog
from NewDialog import NewDialog
from functions import load_data
from functions import save_data
from functions import qdate_to_string
from functions import NULLDATE
from functions import NULLINDEX


"""
DEADLINE: 15/05/2022 - 23:59

TODO: ADD AN OPTION TO DELETE AN ENTRY FROM THE LIST
TODO: IMPLEMENT DATE INFORMATION USING A DEDICATED CLASS RATHER THAN A STRING
TODO: PROJECT DOCUMENTATION
"""


class App(QWidget):
	def __init__(self):
		super().__init__()

		self.animelist = []
		self.load_animelist()
		self.index = NULLINDEX

		self.initUI()
	
	def initUI(self):                           # basic initialization:


		# ========= WINDOW SETTINGS ========= #

		self.resize(1200, 800)                   # setting dimensions
		self.move(200, 100)                     # setting position
		self.setWindowTitle("Anime List")       # setting title
		self.setWindowIcon(QIcon('assets/web.png'))    # setting an icon


		# ========= MAIN LAYOUT ========= #

		main_l = QVBoxLayout()      # the main elements are arranged vertically within the whole window
		self.setLayout(main_l)
		main_l.addWidget(QLabel("Anime list v.1.2", self))  # title


		# ========= TABLE ========= #

		self.main_table = QTableWidget(0, 3, self)       # the table has 3 columns
		self.main_table.setColumnWidth(0, 400)           # the first col containing the title should be larger
		main_l.addWidget(self.main_table)
		"""self.update_table()"""

		for i in range(len(self.animelist)):        # inserting data in the table
			self.main_table.insertRow(i)

			# TITLE
			buffer_title = QTableWidgetItem()
			print("title:", self.animelist[i][0])
			buffer_title.setText(self.animelist[i][0])
			self.main_table.setItem(i, 0, buffer_title)

			# START DATE
			buffer_start = QTableWidgetItem()
			print("start date:", self.animelist[i][1])
			buffer_start.setText(qdate_to_string(self.animelist[i][1]))
			self.main_table.setItem(i, 1, buffer_start)
			
			# END DATE
			buffer_end = QTableWidgetItem()
			print("end date:", self.animelist[i][2])
			if self.animelist[i][2] == NULLDATE:
				buffer_end.setText("")
			else:
				buffer_end.setText(qdate_to_string(self.animelist[i][2]))
			self.main_table.setItem(i, 2, buffer_end)
		
		self.main_table.cellPressed.connect(self.item_selected)


		# ========= BUTTONS ========= #
		
		buttons_l = QHBoxLayout()       # the buttons will be layed out horizontally
		main_l.addLayout(buttons_l)
		
		add_button = QPushButton("Add", self)       # [ADD] button for adding entries
		add_button.setMaximumSize(100, 10000)
		add_button.clicked.connect(self.add_clicked)
		buttons_l.addWidget(add_button)

		self.edit_button = QPushButton("Edit", self)     # [EDIT] button for editing selected entry
		self.edit_button.setMaximumSize(100, 10000)
		self.edit_button.setEnabled(False)					# editing should be disabled if no entry is selected
		self.edit_button.clicked.connect(self.edit_clicked)
		buttons_l.addWidget(self.edit_button)

		self.delete_button = QPushButton("Delete", self)     # [DELETE] button for deleting selected entry
		self.delete_button.setMaximumSize(100, 10000)
		self.delete_button.setEnabled(False)					# editing should be disabled if no entry is selected
		self.delete_button.clicked.connect(self.delete_clicked)
		buttons_l.addWidget(self.delete_button)

		self.export_button = QPushButton("Export Data to *.txt", self)
		self.export_button.setMaximumSize(150, 10000)
		self.export_button.clicked.connect(self.export_clicked)
		buttons_l.addWidget(self.export_button)

		self.show()                             # making the window visible


	def item_selected(self, row, col):
		print(row, col)
		self.index = row
		self.edit_button.setEnabled(True)
		self.delete_button.setEnabled(True)


	def add_clicked(self):
		print("spawning add dialog...")
		self.dialog = EditDialog(start_values=[])
		self.dialog.data_signal.connect(self.add_entry)
	

	def edit_clicked(self):
		print("spawning edit dialog...")
		self.dialog = EditDialog(self.animelist[self.index])
		self.dialog.data_signal.connect(self.edit_entry)
	

	def delete_clicked(self):
		print("spawning delete dialog")
		qm = QMessageBox()
		ret = qm.question(self,'', "Do you want to delete this entry?", qm.Yes | qm.No)
		if ret == qm.Yes:
			print("initiating deleting procedure...")
			self.delete_entry()
		else:
			print("the user changed their mind about deleting this entry")


	def export_clicked(self):
		file_name = QFileDialog().getSaveFileName(parent=self, caption="Save file", filter="Text files (*.txt)")
		print("destination:", file_name[0])
		if len(file_name[0]) > 0:
			file = open(file_name[0], "a")
			watched_list = []
			file.write("Anime list, generated on " + qdate_to_string(QDate.currentDate()) + "\n\n")
			file.write("WATCHING:\n")
			for i in range(len(self.animelist)):
				print("cycle n.", format(i))
				if self.animelist[i][2] == NULLDATE:
					print(self.animelist[i][0], "WATCHING")
					file.write(self.animelist[i][0])
					file.write(" (" + qdate_to_string(self.animelist[i][1]) + ")\n")
				else:
					print(self.animelist[i][0], "WATCHED")
					watched_list.append(self.animelist[i])
			file.write("\nFINISHED:\n")
			for i in range(len(watched_list)):
				file.write(watched_list[i][0])
				file.write(" (" + qdate_to_string(self.animelist[i][1]) + " - " + qdate_to_string(self.animelist[i][2]) + ")\n")
			file.close()
		
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Information)
			msg.setText("The current anime list was successfully exported")
			msg.setWindowTitle("Operation successful")
			msg.setStandardButtons(QMessageBox.Ok)
			msg.exec_()


	@pyqtSlot(str, QDate, QDate)
	def add_entry(self, title, start_day, end_day):
		print("adding data...")

		buffer = [title, start_day, end_day]
		self.animelist.append(buffer)
		print("new animelist:", self.animelist)

		self.save_animelist()

		print(len(self.animelist))

		self.main_table.insertRow(len(self.animelist)-1)
		
		# TITLE
		buffer_title = QTableWidgetItem()
		print("title:", self.animelist[-1][0])
		buffer_title.setText(self.animelist[-1][0])
		self.main_table.setItem(len(self.animelist)-1, 0, buffer_title)

		# START DATE
		buffer_start = QTableWidgetItem()
		print("start date:", self.animelist[-1][1])
		buffer_start.setText(qdate_to_string(self.animelist[-1][1]))
		self.main_table.setItem(len(self.animelist)-1, 1, buffer_start)
		
		# END DATE
		buffer_end = QTableWidgetItem()
		print("end date:", self.animelist[-1][2])
		if self.animelist[-1][2] == NULLDATE:
			buffer_end.setText("")
		else:
			buffer_end.setText(qdate_to_string(self.animelist[-1][2]))
		self.main_table.setItem(len(self.animelist)-1, 2, buffer_end)
		

	@pyqtSlot(str, QDate, QDate)
	def edit_entry(self, title, start_day, end_day):
		print("editing data...")

		buffer = [title, start_day, end_day]
		self.animelist[self.index] = buffer
		print("new animelist:", self.animelist)

		self.save_animelist()

		# TITLE
		buffer_title = QTableWidgetItem()
		print("title:", self.animelist[self.index][0])
		buffer_title.setText(self.animelist[self.index][0])
		self.main_table.setItem(self.index, 0, buffer_title)

		# START DATE
		buffer_start = QTableWidgetItem()
		print("start date:", self.animelist[self.index][1])
		buffer_start.setText(qdate_to_string(self.animelist[self.index][1]))
		self.main_table.setItem(self.index, 1, buffer_start)
		
		# END DATE
		buffer_end = QTableWidgetItem()
		print("end date:", self.animelist[self.index][2])
		if self.animelist[self.index][2] == NULLDATE:
			buffer_end.setText("")
		else:
			buffer_end.setText(qdate_to_string(self.animelist[self.index][2]))
		self.main_table.setItem(self.index, 2, buffer_end)

		
	def delete_entry(self):
		print("deleting entry...")
		self.animelist.pop(self.index)
		self.save_animelist()

		print("starting point is", format(self.index))

		if self.index < len(self.animelist):
			for i in range(self.index, len(self.animelist)):
				for j in range(len(self.animelist[i])):
					buffer = self.main_table.item(i+1, j)
					self.main_table.setItem(i, j, buffer)
		self.main_table.removeRow(self.index)
		self.index = NULLINDEX
		self.edit_button.setEnabled(False)
		self.delete_button.setEnabled(False)


	def save_animelist(self):
		buffer = []
		
		for i in range(len(self.animelist)):
			buffer.append([])
			buffer[i].append(self.animelist[i][0])
			for j in range(2):
				temp_date = [
					self.animelist[i][j+1].day(),
					self.animelist[i][j+1].month(),
					self.animelist[i][j+1].year()
				]
				buffer[i].append(temp_date)
		save_data(buffer)

	
	def load_animelist(self):
		buffer = load_data()			# loading the data from the file into a temporary object
		
		for i in range(len(buffer)):
			self.animelist.append([])
			# TITLE
			# put title from buffer directly into the title of animelist[0]
			self.animelist[i].append(buffer[i][0])

			# START DATE (WITH CONVERSION FROM STRING TO QDATE)
			temp_date = QDate(buffer[i][1][2], buffer[i][1][1], buffer[i][1][0])
			self.animelist[i].append(temp_date)

			# END DATE (WITH CONVERSION FROM STRING TO QDATE)
			if len(buffer[i][2]) != 3:
				self.animelist[i].append(NULLDATE)
			else:
				temp_date = QDate(buffer[i][2][2], buffer[i][2][1], buffer[i][2][0])
				self.animelist[i].append(temp_date)

		
		print(self.animelist)



def main():
	app = QApplication(sys.argv)    # creation of the application object
	sw = App()              # creation of the small window object
	sys.exit(app.exec_())           # this code will stop and only the app will continue to run (?)

if __name__ == "__main__":          # main() will only be called if this is run directly and not imported in some other code
	main()