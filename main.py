import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
import db

from ui.instructor import InstructorTab
from ui.booking import BookingTab
from ui.schedule import ScheduleTab
from ui.report import ReportTab
from ui.reservation import ReservationTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ski Tour Management System")
        self.resize(1000, 700)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tabs.addTab(BookingTab(), "예약 관리")
        self.tabs.addTab(ReservationTab(), "예약")
        self.tabs.addTab(ScheduleTab(), "당일 스케줄")
        self.tabs.addTab(ReportTab(), "통계")
        self.tabs.addTab(InstructorTab(), "강사")


def main():
    db.init_db()
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
