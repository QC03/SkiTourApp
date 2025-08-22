import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
import db

from ui_instructor import InstructorTab
from ui_booking import BookingTab
from ui_schedule import ScheduleTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("스키 강습 관리 프로그램")
        self.resize(1000, 700)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tabs.addTab(InstructorTab(), "강사")
        self.tabs.addTab(BookingTab(), "예약 관리")
        self.tabs.addTab(ScheduleTab(), "당일 스케줄")


def main():
    db.init_db()
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
