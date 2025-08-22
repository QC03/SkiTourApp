from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QCheckBox, QPushButton,
    QTableWidget, QTableWidgetItem
)
import db

class InstructorTab(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_id = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 입력폼
        self.name_edit = QLineEdit()
        self.can_ski_chk = QCheckBox("스키 가능")
        self.can_snowboard_chk = QCheckBox("스노보드 가능")
        self.can_english_chk = QCheckBox("영어 가능")
        self.active_chk = QCheckBox("활동중")
        self.active_chk.setChecked(True)

        # 버튼
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("추가")
        self.add_btn.clicked.connect(self.add_instructor)
        self.update_btn = QPushButton("수정")
        self.update_btn.clicked.connect(self.update_instructor)
        self.delete_btn = QPushButton("삭제")
        self.delete_btn.clicked.connect(self.delete_instructor)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)

        layout.addWidget(self.name_edit)
        layout.addWidget(self.can_ski_chk)
        layout.addWidget(self.can_snowboard_chk)
        layout.addWidget(self.can_english_chk)
        layout.addWidget(self.active_chk)
        layout.addLayout(btn_layout)

        # 테이블
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "이름", "스키", "스노보드", "영어", "활동중"])
        self.table.cellClicked.connect(self.on_row_select)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.refresh()

    def refresh(self):
        rows = db.get_instructors()
        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                if c >=2:  # 체크박스 관련
                    val = "예" if val else "아니오"
                self.table.setItem(r, c, QTableWidgetItem(str(val)))

    def on_row_select(self, row, col):
        self.selected_id = int(self.table.item(row, 0).text())
        self.name_edit.setText(self.table.item(row,1).text())
        self.can_ski_chk.setChecked(self.table.item(row,2).text() == "예")
        self.can_snowboard_chk.setChecked(self.table.item(row,3).text() == "예")
        self.can_english_chk.setChecked(self.table.item(row,4).text() == "예")
        self.active_chk.setChecked(self.table.item(row,5).text() == "예")

    def add_instructor(self):
        db.add_instructor(
            self.name_edit.text(),
            int(self.can_ski_chk.isChecked()),
            int(self.can_snowboard_chk.isChecked()),
            int(self.can_english_chk.isChecked()),
            int(self.active_chk.isChecked())
        )
        self.refresh()

    def update_instructor(self):
        if self.selected_id:
            db.update_instructor(
                self.selected_id,
                self.name_edit.text(),
                int(self.can_ski_chk.isChecked()),
                int(self.can_snowboard_chk.isChecked()),
                int(self.can_english_chk.isChecked()),
                int(self.active_chk.isChecked())
            )
            self.refresh()

    def delete_instructor(self):
        if self.selected_id:
            db.delete_instructor(self.selected_id)
            self.refresh()
