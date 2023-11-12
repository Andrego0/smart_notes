from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from ui import Ui_MainWindow

import json

class NoteWidget(QMainWindow):
    def   __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.notes = {}
        self.read_notes()
        self.connects()

    def connects(self):
        self.ui.list_notes.itemClicked.connect(self.show_note)

    def read_notes(self):
        try:
            with open("notes.json", "r", encoding="utf-8") as file:
                self.notes = json.load(file)
        except:
            self.notes = {"Ласкаво просимо в Розумні замітки!":{
                "текст": "Додайте свою першу замітку!", "теги":[]
            }}
        self.ui.list_notes.addItems(self.notes)

    def show_note(self):
        name = self.ui.list_notes.selectedItems()[0].text()
        self.ui.titel_note_edit.setText(name)
        self.ui.note_text.setText(self.notes[name]["текст"])
        self.ui.tag_list.clear()
        self.ui.tag_list.addItems(self.notes[name]["теги"])

app = QApplication([])
ex = NoteWidget()
ex.show()
app.exec_()