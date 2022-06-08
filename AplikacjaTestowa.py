from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QLabel, QToolBar, QStatusBar
from PySide6.QtCore import Slot, QSize
from PySide6.QtGui import QCloseEvent, QAction, QIcon
import sys


@Slot()
def say_hello():
    print("Button clicked, Hello!")


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 200, 200)
        self.setWindowTitle("APLIKACJA TESTOWA")

        label = QLabel("Aplikacja HL7", self)
        label.setGeometry(60, 20, 200, 40)
        label.show()


        btn = QPushButton("Zapisz", self)
        btn.setGeometry(0, 60, 200, 40)
        btn.setStyleSheet("background-color: grey")
        btn.clicked.connect(say_hello)
        btn.show()

        btn1 = QPushButton("Edytuj", self)
        btn1.setGeometry(0, 100, 200, 40)
        btn1.setStyleSheet("background-color: grey")

        btn_quit = QPushButton("Wyjście", self)
        btn_quit.clicked.connect(QApplication.instance().quit)
        btn_quit.resize(btn_quit.sizeHint())
        btn_quit.move(90, 100)
        btn_quit.setGeometry(0, 140, 200, 40)
        btn_quit.setStyleSheet("background-color: grey")

        button_action = QAction(QIcon("folder.jpg"), "&Open", self)
        button_action.setStatusTip("Open file")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        button_action.setCheckable(True)

        self.setStatusBar(QStatusBar(self))

        menu = self.menuBar()

        file_menu = menu.addMenu(QIcon('folder.jpg'), "&File")
        file_menu.addAction(button_action)

        self.show()

    def onMyToolBarButtonClick(self, s):
        print("click", s)

    def closeEvent(self, event: QCloseEvent):
        reply = QMessageBox.question(self, 'Wiadomość', 'Jesteś pewny, że chcesz zamknąć?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
