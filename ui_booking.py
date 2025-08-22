from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox,
    QPushButton, QDateEdit, QSpinBox, QTextEdit, QMessageBox,
    QTableWidget, QTableWidgetItem, QHBoxLayout
)
from PyQt6.QtCore import QDate
import db


class BookingTab(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_id = None
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        form = QFormLayout()

        # 고객 정보
        self.customer_name = QLineEdit()
        self.customer_name.textChanged.connect(self.check_returning_customer)
        self.customer_phone = QLineEdit()
        self.customer_phone.textChanged.connect(self.check_returning_customer)

        # 날짜
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)

        # 시작 시간 (1시간 단위)
        self.time_combo = QComboBox()
        for h in range(6, 23):
            self.time_combo.addItem(f"{h:02d}:00")

        # 강습 시간
        self.duration = QSpinBox()
        self.duration.setRange(1, 8)
        self.duration.setValue(2)
        self.duration.setSuffix(" 시간")

        # 강습 정보
        self.lesson_type = QLineEdit()
        self.level = QComboBox()
        self.level.addItems(["초급", "중급", "상급"])
        self.people_count = QSpinBox()
        self.people_count.setRange(1, 10)
        self.memo = QTextEdit()

        # 강사 선택
        self.instructor_combo = QComboBox()
        self.load_instructors()

        # 폼 배치
        form.addRow("이름:", self.customer_name)
        form.addRow("전화번호:", self.customer_phone)
        form.addRow("날짜:", self.date_edit)
        form.addRow("시작 시간:", self.time_combo)
        form.addRow("강습 시간:", self.duration)
        form.addRow("강습 종류:", self.lesson_type)
        form.addRow("레벨:", self.level)
        form.addRow("인원 수:", self.people_count)
        form.addRow("메모:", self.memo)
        form.addRow("강사:", self.instructor_combo)
        main_layout.addLayout(form)

        # 강사 새로고침 & 예약 저장 버튼
        self.refresh_btn = QPushButton("강사 목록 새로고침")
        self.refresh_btn.clicked.connect(self.load_instructors)
        self.save_btn = QPushButton("예약 저장")
        self.save_btn.clicked.connect(self.save_booking)
        main_layout.addWidget(self.refresh_btn)
        main_layout.addWidget(self.save_btn)

        # 예약 테이블
        self.table = QTableWidget()
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels([
            "ID", "고객 이름", "전화번호", "날짜", "시작 시간", "강습 시간(분)",
            "강습 종류", "레벨", "인원 수", "메모", "강사"
        ])
        self.table.cellClicked.connect(self.on_row_select)
        main_layout.addWidget(self.table)

        # 수정/삭제 버튼
        btn_layout = QHBoxLayout()
        self.update_btn = QPushButton("예약 수정")
        self.update_btn.clicked.connect(self.update_booking)
        self.delete_btn = QPushButton("예약 삭제")
        self.delete_btn.clicked.connect(self.delete_booking)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)
        self.refresh_table()

    # ---------------------------
    # 재방문 고객 표시 기능
    # ---------------------------
    def check_returning_customer(self):
        name = self.customer_name.text().strip()
        phone = self.customer_phone.text().strip()
        if not name or not phone:
            self.customer_name.setStyleSheet("")
            return
        cid = db.find_customer(name, phone)
        if cid:
            self.customer_name.setStyleSheet("background-color: #ffff99")  # 연노랑
            self.customer_name.setToolTip(f"재방문 고객 (ID: {cid})")
            
            if(len(self.memo.toPlainText().strip()) == 0):
                self.memo.setText(f"재방문 고객 (ID: {cid})")
        else:
            self.customer_name.setStyleSheet("")  # 일반

    # ---------------------------
    # 나머지 기존 함수
    # ---------------------------
    def load_instructors(self):
        self.instructor_combo.clear()
        instructors = db.get_instructors()
        for inst in instructors:
            self.instructor_combo.addItem(inst[1], inst[0])

    def save_booking(self):
        name = self.customer_name.text().strip()
        phone = self.customer_phone.text().strip()
        date = self.date_edit.date().toString("yyyy-MM-dd")
        start_time = self.time_combo.currentText()
        duration = self.duration.value() * 60  # 시간 → 분
        lesson_type = self.lesson_type.text().strip()
        level = self.level.currentText()
        people_count = self.people_count.value()
        memo = self.memo.toPlainText().strip()
        instructor_id = self.instructor_combo.currentData()

        if not name or not phone:
            QMessageBox.warning(self, "오류", "고객 이름과 전화번호를 입력하세요.")
            return

        customer_id = db.find_customer(name, phone)
        if not customer_id:
            customer_id = db.add_customer(name, phone)

        db.add_booking(customer_id, date, start_time, duration,
                       lesson_type, level, people_count, memo, instructor_id)
        QMessageBox.information(self, "완료", "예약이 저장되었습니다.")
        self.clear_form()
        self.refresh_table()

    def refresh_table(self):
        rows = db.get_bookings()
        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(val)))

    def clear_form(self):
        self.customer_name.clear()
        self.customer_phone.clear()
        self.customer_name.setStyleSheet("")
        self.date_edit.setDate(QDate.currentDate())
        self.time_combo.setCurrentIndex(0)
        self.duration.setValue(2)
        self.lesson_type.clear()
        self.level.setCurrentIndex(0)
        self.people_count.setValue(1)
        self.memo.clear()
        if self.instructor_combo.count() > 0:
            self.instructor_combo.setCurrentIndex(0)
        self.selected_id = None

    def on_row_select(self, row, col):
        self.selected_id = int(self.table.item(row, 0).text())
        self.customer_name.setText(self.table.item(row, 1).text())
        self.customer_phone.setText(self.table.item(row, 2).text())
        self.check_returning_customer()
        self.date_edit.setDate(QDate.fromString(self.table.item(row, 3).text(), "yyyy-MM-dd"))
        self.time_combo.setCurrentText(self.table.item(row, 4).text())
        self.duration.setValue(int(self.table.item(row, 5).text()) // 60)
        self.lesson_type.setText(self.table.item(row, 6).text())
        self.level.setCurrentText(self.table.item(row, 7).text())
        self.people_count.setValue(int(self.table.item(row, 8).text()))
        self.memo.setPlainText(self.table.item(row, 9).text())
        self.instructor_combo.setCurrentText(self.table.item(row, 10).text() if self.table.item(row, 10) else "")

    def update_booking(self):
        if not self.selected_id:
            return

        name = self.customer_name.text().strip()
        phone = self.customer_phone.text().strip()
        date = self.date_edit.date().toString("yyyy-MM-dd")
        start_time = self.time_combo.currentText()
        duration = self.duration.value() * 60
        lesson_type = self.lesson_type.text().strip()
        level = self.level.currentText()
        people_count = self.people_count.value()
        memo = self.memo.toPlainText().strip()
        instructor_id = self.instructor_combo.currentData()

        customer_id = db.find_customer(name, phone)
        if not customer_id:
            customer_id = db.add_customer(name, phone)

        db.update_booking(self.selected_id, customer_id, date, start_time, duration,
                          lesson_type, level, people_count, memo, instructor_id)
        QMessageBox.information(self, "완료", "예약이 수정되었습니다.")
        self.clear_form()
        self.refresh_table()

    def delete_booking(self):
        if not self.selected_id:
            return
        db.delete_booking(self.selected_id)
        QMessageBox.information(self, "완료", "예약이 삭제되었습니다.")
        self.clear_form()
        self.refresh_table()
