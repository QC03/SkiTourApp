from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox,
    QPushButton, QDateEdit, QTimeEdit, QSpinBox, QTextEdit, QMessageBox
)
from PyQt6.QtCore import QDate, QTime
import db


class BookingTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        form = QFormLayout()

        # 고객 정보
        self.customer_name = QLineEdit()
        self.customer_phone = QLineEdit()

        # 날짜/시간
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)

        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime.currentTime())

        self.duration = QSpinBox()
        self.duration.setRange(60, 480)  # 1시간 ~ 8시간
        self.duration.setSingleStep(30)
        self.duration.setValue(120)  # 기본 2시간

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

        # 폼에 추가
        form.addRow("이름:", self.customer_name)
        form.addRow("전화번호:", self.customer_phone)
        form.addRow("날짜:", self.date_edit)
        form.addRow("시작 시간:", self.time_edit)
        form.addRow("강습 시간(분):", self.duration)
        form.addRow("강습 종류:", self.lesson_type)
        form.addRow("레벨:", self.level)
        form.addRow("인원 수:", self.people_count)
        form.addRow("메모:", self.memo)
        form.addRow("강사:", self.instructor_combo)

        layout.addLayout(form)

        # 버튼
        self.save_btn = QPushButton("예약 저장")
        self.save_btn.clicked.connect(self.save_booking)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def load_instructors(self):
        self.instructor_combo.clear()
        instructors = db.get_instructors()
        for inst in instructors:
            self.instructor_combo.addItem(inst[1], inst[0])  # name, id

    def save_booking(self):
        name = self.customer_name.text().strip()
        phone = self.customer_phone.text().strip()
        date = self.date_edit.date().toString("yyyy-MM-dd")
        start_time = self.time_edit.time().toString("HH:mm")
        duration = self.duration.value()
        lesson_type = self.lesson_type.text().strip()
        level = self.level.currentText()
        people_count = self.people_count.value()
        memo = self.memo.toPlainText().strip()
        instructor_id = self.instructor_combo.currentData()

        if not name or not phone:
            QMessageBox.warning(self, "오류", "고객 이름과 전화번호를 입력하세요.")
            return

        # 고객 확인 (기존 고객이면 id 사용, 없으면 새로 추가)
        customer_id = db.find_customer(name, phone)
        if not customer_id:
            customer_id = db.add_customer(name, phone)

        db.add_booking(customer_id, date, start_time, duration,
                       lesson_type, level, people_count, memo, instructor_id)

        QMessageBox.information(self, "완료", "예약이 저장되었습니다.")
        self.clear_form()

    def clear_form(self):
        self.customer_name.clear()
        self.customer_phone.clear()
        self.date_edit.setDate(QDate.currentDate())
        self.time_edit.setTime(QTime.currentTime())
        self.duration.setValue(120)
        self.lesson_type.clear()
        self.level.setCurrentIndex(0)
        self.people_count.setValue(1)
        self.memo.clear()
        if self.instructor_combo.count() > 0:
            self.instructor_combo.setCurrentIndex(0)
