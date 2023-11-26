from PyQt5.QtWidgets import QApplication, QInputDialog
from PyQt5.QtWidgets import QMainWindow, QMessageBox
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
        self.ui.create_notes.clicked.connect(self.add_note)
        self.ui.save_note.clicked.connect(self.save_note)
        self.ui.delete_notes.clicked.connect(self.del_note)
        self.ui.add_tag.clicked.connect(self.add_tag)
        self.ui.open_tag.clicked.connect(self.del_tag)

        

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


    def add_note(self):
        self.ui.titel_note_edit.clear()
        self.ui.note_text.clear()
        self.ui.tag_list.clear()

    def save_file(self):
        try:
            with open("notes.json", "w", encoding="utf-8") as file:
                json.dump(self.notes, file, ensure_ascii=False)
        except:
            message = QMessageBox
            message.setText("Не вдалося зберегти")
            message.show()
            message.exec_()

    def save_note(self):
        title = self.ui.titel_note_edit.text()
        text = self.ui.note_text.toPlainText()
        if title not in self.notes:
            self.notes[title] = {"текст": text, "теги": []}
        else:
            self.notes[title]["текст"] = text
        self.save_file()
        self.ui.list_notes.clear()
        self.ui.list_notes.addItems(self.notes)

    def del_note(self):
        title = self.ui.titel_note_edit.text()
        if title in self.notes:
            del self.notes[title]
            self.ui.list_notes.clear()
            self.ui.list_notes.addItems(self.notes)
            self.save_file()
            self.add_note()

    def add_tag(self):
        title = self.ui.titel_note_edit.text()
        tag_title, ok = QInputDialog.getText(self,"Введіть, тег", "Назва тега")
        if ok and tag_title != "" and title != "":
            self.notes[title]["теги"].append(tag_title)
            self.ui.tag_list.clear()
            self.ui.tag_list.addItems(self.notes[title]["теги"])

    def del_tag(self):
        title = self.ui.titel_note_edit.text()
        try:
            tag_title = self.ui.tag_list.selectedItems()[0].text()
        except:
            tag_title = None
        if tag_title and title != "":
            self.notes[title]["теги"].remove(tag_title)
            self.ui.tag_list.clear()
            self.ui.tag_list.addItems(self.notes[title]["теги"])





app = QApplication([])
ex = NoteWidget()
ex.show()
app.exec_()