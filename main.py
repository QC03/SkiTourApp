
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout,
    QLabel, QStatusBar, QToolBar
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

from db import init_db
from ui_instructor import InstructorTab

import sys


APP_TITLE = "Ski Lesson Scheduler"

def placeholder_tab(title: str, subtitle: str = "") -> QWidget:
    w = QWidget()
    layout = QVBoxLayout(w)
    h = QLabel(f"<h2 style='margin:0'>{title}</h2>")
    h.setTextFormat(Qt.TextFormat.RichText)
    s = QLabel(subtitle or "이 탭은 다음 단계에서 구현됩니다.")
    layout.addWidget(h)
    layout.addWidget(s)
    layout.addStretch(1)
    return w

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.resize(1100, 700)

        self.tabs = QTabWidget()
        self.tabs.addTab(placeholder_tab("예약 관리"), "예약")
        self.tabs.addTab(placeholder_tab("강사 관리"), "강사")
        self.tabs.addTab(placeholder_tab("스케줄"), "스케줄")
        self.tabs.addTab(placeholder_tab("출력 / 리포트"), "출력")
        self.tabs.addTab(placeholder_tab("설정"), "설정")
        self.setCentralWidget(self.tabs)

        # Toolbar
        tb = QToolBar("Main")
        self.addToolBar(tb)

        act_quit = QAction("종료", self)
        act_quit.triggered.connect(self.close)
        tb.addAction(act_quit)

        # Status bar
        sb = QStatusBar()
        sb.showMessage("Step 1: 프로젝트 골격 준비 완료")
        self.setStatusBar(sb)

        # Ready To Database
        init_db()

        # Connect to ui_instructor.py
        self.tabs = QTabWidget()
        self.tabs.addTab(QWidget(), "예약")   # 다음 단계에서 구현
        self.tabs.addTab(InstructorTab(), "강사")
        self.tabs.addTab(QWidget(), "스케줄")
        self.tabs.addTab(QWidget(), "출력")
        self.tabs.addTab(QWidget(), "설정")
        self.setCentralWidget(self.tabs)

    def closeEvent(self, e):
        # 이후 단계에서 저장/확인 로직을 추가할 수 있습니다.
        e.accept()

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
