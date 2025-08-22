from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDateEdit,
    QTableWidget, QTableWidgetItem, QPushButton
)
from PyQt6.QtCore import QDate
import db

class ReservationTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 날짜 선택
        h_layout = QHBoxLayout()
        h_layout.addWidget(QLabel("날짜 선택:"))
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.dateChanged.connect(self.refresh_table)
        h_layout.addWidget(self.date_edit)
        layout.addLayout(h_layout)

        # 예약 테이블
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "고객 이름", "전화번호", "강습 종류", "레벨",
            "강사", "시작 시간", "강습 시간(분)", "인원 수", "메모"
        ])
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.refresh_table()

    # ---------------------------
    # 테이블 갱신
    # ---------------------------
    def refresh_table(self):
        date = self.date_edit.date().toString("yyyy-MM-dd")
        bookings = db.get_bookings_by_date(date)
        self.table.setRowCount(len(bookings))

        for r, b in enumerate(bookings):
            # b 구조: (id, name, phone, date, start_time, duration_minutes,
            #          lesson_type, level, people_count, memo, instructor_id, instructor_name)
            self.table.setItem(r, 0, QTableWidgetItem(b[1]))  # 고객 이름
            self.table.setItem(r, 1, QTableWidgetItem(b[2]))  # 전화번호
            self.table.setItem(r, 2, QTableWidgetItem(b[6]))  # 강습 종류
            self.table.setItem(r, 3, QTableWidgetItem(b[7]))  # 레벨
            self.table.setItem(r, 4, QTableWidgetItem(b[11])) # 강사 이름
            self.table.setItem(r, 5, QTableWidgetItem(b[4]))  # 시작 시간
            self.table.setItem(r, 6, QTableWidgetItem(str(b[5])))  # 강습 시간
            self.table.setItem(r, 7, QTableWidgetItem(str(b[8])))  # 인원 수
            self.table.setItem(r, 8, QTableWidgetItem(b[9]))  # 메모
