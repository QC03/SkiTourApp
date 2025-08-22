from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDateEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog
)
from PyQt6.QtCore import QDate
import db
import csv

class ReportTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 날짜 선택
        h_layout = QHBoxLayout()
        h_layout.addWidget(QLabel("통계 날짜:"))
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        h_layout.addWidget(self.date_edit)

        # 버튼
        self.generate_btn = QPushButton("통계 생성")
        self.generate_btn.clicked.connect(self.generate_report)
        self.export_btn = QPushButton("CSV로 내보내기")
        self.export_btn.clicked.connect(self.export_csv)
        h_layout.addWidget(self.generate_btn)
        h_layout.addWidget(self.export_btn)

        layout.addLayout(h_layout)

        # 테이블
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "강사", "강습 건수", "총 강습 시간(시간)", "초급", "중급", "상급"
        ])
        layout.addWidget(self.table)

        self.setLayout(layout)

    # ---------------------------
    # 통계 생성
    # ---------------------------
    def generate_report(self):
        date = self.date_edit.date().toString("yyyy-MM-dd")
        bookings = db.get_bookings_by_date(date)
        
        stats = {}
        for b in bookings:
            instructor = b[11] if len(b) > 11 else f"ID:{b[10]}" # 강사 이름
            level = b[7]        # 레벨
            duration_hours = int(b[5]) // 60

            if instructor not in stats:
                stats[instructor] = {"count":0, "hours":0, "초급":0, "중급":0, "상급":0}

            stats[instructor]["count"] += 1
            stats[instructor]["hours"] += duration_hours
            stats[instructor][level] += 1

        self.table.setRowCount(len(stats))
        for r, (instr, data) in enumerate(stats.items()):
            self.table.setItem(r, 0, QTableWidgetItem(instr))
            self.table.setItem(r, 1, QTableWidgetItem(str(data["count"])))
            self.table.setItem(r, 2, QTableWidgetItem(str(data["hours"])))
            self.table.setItem(r, 3, QTableWidgetItem(str(data["초급"])))
            self.table.setItem(r, 4, QTableWidgetItem(str(data["중급"])))
            self.table.setItem(r, 5, QTableWidgetItem(str(data["상급"])))

    # ---------------------------
    # CSV 내보내기
    # ---------------------------
    def export_csv(self):
        # today
        today_str = QDate.currentDate().toString("yyyy-MM-dd")
        default_filename = f"{today_str}_예약통계.csv"

        path, _ = QFileDialog.getSaveFileName(self, "CSV로 저장", default_filename, "CSV Files (*.csv)")
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                # 헤더
                writer.writerow(["강사","강습 건수","총 강습 시간","초급","중급","상급"])
                # 데이터
                for row in range(self.table.rowCount()):
                    writer.writerow([self.table.item(row, col).text() for col in range(self.table.columnCount())])
            QMessageBox.information(self, "완료", f"CSV가 저장되었습니다:\n{path}")
        except Exception as e:
            QMessageBox.warning(self, "오류", f"CSV 저장 중 오류 발생:\n{e}")
