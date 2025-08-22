from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QDateEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QLabel
)
from PyQt6.QtCore import QDate
import db

class ScheduleTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # 상단: 날짜 선택
        top_layout = QHBoxLayout()
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.generate_btn = QPushButton("스케줄 생성")
        self.generate_btn.clicked.connect(self.generate_schedule)
        top_layout.addWidget(QLabel("날짜 선택:"))
        top_layout.addWidget(self.date_edit)
        top_layout.addWidget(self.generate_btn)
        main_layout.addLayout(top_layout)

        # 스케줄 테이블
        self.table = QTableWidget()
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

    def generate_schedule(self):
        date = self.date_edit.date().toString("yyyy-MM-dd")

        # 강사 목록
        instructors = db.get_instructors()
        if not instructors:
            return

        instructor_names = [inst[1] for inst in instructors]
        instructor_ids = [inst[0] for inst in instructors]

        # 테이블 설정
        self.table.clear()
        self.table.setColumnCount(len(instructors) + 1)  # 0열: 시간, 나머지: 강사
        self.table.setRowCount(17)  # 06:00~22:00
        headers = ["시간"] + instructor_names
        self.table.setHorizontalHeaderLabels(headers)

        # 시간 행 설정
        for i, hour in enumerate(range(6, 23)):
            self.table.setItem(i, 0, QTableWidgetItem(f"{hour:02d}:00"))

        # 해당 날짜 예약 조회
        bookings = db.get_bookings_by_date(date)

        # 강사별 예약 배치
        schedule = {inst_id: {} for inst_id in instructor_ids}
        for b in bookings:
            # b = (id, customer_name, phone, date, start_time, duration, lesson_type, level, people_count, memo, instructor_name)
            inst_id = b[10]  # instructor_id
            if inst_id not in schedule:
                continue
            start_hour = int(b[4].split(":")[0])
            duration_hours = int(b[5]) // 60
            for h in range(start_hour, start_hour + duration_hours):
                if 6 <= h <= 22:
                    schedule[inst_id][h] = f"{b[1]} ({b[6]})"

        # 테이블에 값 입력
        for col, inst_id in enumerate(instructor_ids, start=1):
            for row, hour in enumerate(range(6, 23)):
                text = schedule[inst_id].get(hour, "")
                self.table.setItem(row, col, QTableWidgetItem(text))
