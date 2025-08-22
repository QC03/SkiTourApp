from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QCheckBox, QTableWidget, QTableWidgetItem, QMessageBox
)
import db

class InstructorTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)

        # 왼쪽: 테이블
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "이름", "스키", "보드", "영어", "활성"])
        self.table.cellClicked.connect(self.on_row_select)
        layout.addWidget(self.table, 2)

        # 오른쪽: 입력폼 + 버튼
        right = QVBoxLayout()
        self.name_input = QLineEdit()
        self.chk_ski = QCheckBox("스키")
        self.chk_snow = QCheckBox("보드")
        self.chk_eng = QCheckBox("영어 가능")
        self.chk_active = QCheckBox("활성")

        right.addWidget(self.name_input)
        right.addWidget(self.chk_ski)
        right.addWidget(self.chk_snow)
        right.addWidget(self.chk_eng)
        right.addWidget(self.chk_active)

        btn_add = QPushButton("추가")
        btn_add.clicked.connect(self.add)
        btn_update = QPushButton("수정")
        btn_update.clicked.connect(self.update)
        btn_delete = QPushButton("삭제")
        btn_delete.clicked.connect(self.delete)

        right.addWidget(btn_add)
        right.addWidget(btn_update)
        right.addWidget(btn_delete)
        right.addStretch(1)

        layout.addLayout(right, 1)

        self.selected_id = None
        self.refresh()

    def refresh(self):
        rows = db.get_instructors()
        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(val)))

    def on_row_select(self, row, col):
        self.selected_id = int(self.table.item(row, 0).text())
        self.name_input.setText(self.table.item(row, 1).text())
        self.chk_ski.setChecked(self.table.item(row, 2).text() == "1")
        self.chk_snow.setChecked(self.table.item(row, 3).text() == "1")
        self.chk_eng.setChecked(self.table.item(row, 4).text() == "1")
        self.chk_active.setChecked(self.table.item(row, 5).text() == "1")

    def add(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "오류", "이름을 입력하세요.")
            return
        db.add_instructor(name, self.chk_ski.isChecked(),
                          self.chk_snow.isChecked(),
                          self.chk_eng.isChecked(),
                          self.chk_active.isChecked())
        self.refresh()

    def update(self):
        if not self.selected_id:
            return
        db.update_instructor(self.selected_id,
                             self.name_input.text(),
                             self.chk_ski.isChecked(),
                             self.chk_snow.isChecked(),
                             self.chk_eng.isChecked(),
                             self.chk_active.isChecked())
        self.refresh()

    def delete(self):
        if not self.selected_id:
            return
        db.delete_instructor(self.selected_id)
        self.refresh()
