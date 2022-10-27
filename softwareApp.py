import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QAction
from PyQt5.QtGui import QIcon


class App(QWidget):
	def __init__(self):
		super().__init__()
		self.title = 'Data Science'
		self.left = 10
		self.top = 10
		self.width = 640
		self.height = 480
		self.createMenu()
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.show()

	def createMenu(self):
		headerMenu = self.menuBar()

		# header menus
		fileMenu = headerMenu.addMenu('File')
		editMenu = headerMenu.addMenu('Edit')
		viewMenu = headerMenu.addMenu('View')
		helpMenu = headerMenu.addMenu('Help')

		# Actions within 'Edit' menu
		copyAction = QAction(QIcon("Copy.png"), 'Copy', self)
		copyAction.setShortcut("Ctrl + C")
		pasteAction = QAction(QIcon("Paste.png"), 'Paste', self)
		pasteAction.setShortcut("Ctrl + V")
		editMenu.addAction(copyAction)
		editMenu.addAction(pasteAction)

		# Actions within 'File' menu
		saveAction = QAction(QIcon("Save.png"), 'Save', self)
		saveAction.setShortcut("Ctrl + S")
		fileMenu.addAction(saveAction)


if __name__ == '__main__':
	App = QApplication(sys.argv)
	app = App()
	sys.exit(App.exec_())
