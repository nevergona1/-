import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor
from spellchecker import SpellChecker

class SpellCheckApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Проверка орфографических ошибок')
        self.setGeometry(100, 100, 1000, 700)

        self.text_edit = QTextEdit(self)
        self.text_edit.textChanged.connect(self.autoCheckSpelling)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)

        self.correct_button = QPushButton('Исправить', self)
        self.correct_button.clicked.connect(self.correctSpelling)
        layout.addWidget(self.correct_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

        # Создайте экземпляр SpellChecker без указания языка
        self.spell_checker = SpellChecker()

    def autoCheckSpelling(self):
        self.text_edit.textChanged.disconnect(self.autoCheckSpelling)

        text = self.text_edit.toPlainText().lower()  # Преобразовать весь текст в нижний регистр
        misspelled = self.spell_checker.unknown(text.split())

        cursor = self.text_edit.textCursor()
        default_format = QTextCharFormat()
        default_format.setForeground(QColor('black'))

        cursor.setPosition(0)
        cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
        cursor.setCharFormat(default_format)

        red_underline_format = QTextCharFormat()
        red_underline_format.setUnderlineColor(QColor('red'))
        red_underline_format.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)

        for word in misspelled:
            pos = text.find(word)
            while pos != -1:
                if pos > 0 and not text[pos - 1].isalpha():
                    end = pos + len(word)
                    cursor.setPosition(pos)
                    cursor.setPosition(end, QTextCursor.KeepAnchor)
                    cursor.mergeCharFormat(red_underline_format)
                pos = text.find(word, pos + 1)

        self.text_edit.textChanged.connect(self.autoCheckSpelling)

    def correctSpelling(self):
        cursor = self.text_edit.textCursor()
        text = self.text_edit.toPlainText()
        misspelled = self.spell_checker.unknown(text.split())

        for word in misspelled:
            corrected_word = self.spell_checker.correction(word)
            pos = text.lower().find(word)  # Преобразовать текст к нижнему регистру для поиска
            while pos != -1:
                cursor.setPosition(pos)
                cursor.setPosition(pos + len(word), QTextCursor.KeepAnchor)
                cursor.insertText(corrected_word)
                pos = text.lower().find(word, pos + 1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    spell_check_app = SpellCheckApp()
    spell_check_app.show()
    sys.exit(app.exec_())
