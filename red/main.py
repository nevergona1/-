import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
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

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

        self.spell_en = SpellChecker(language='en')

    def autoCheckSpelling(self):
        # Disconnect the textChanged signal to avoid recursion
        self.text_edit.textChanged.disconnect(self.autoCheckSpelling)

        text = self.text_edit.toPlainText()
        misspelled = self.spell_en.unknown(text.split())

        cursor = self.text_edit.textCursor()
        format = QTextCharFormat()
        format.setUnderlineColor(QColor('red'))
        format.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)

        # Reset underlining before rechecking
        cursor.setPosition(0)
        cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
        cursor.setCharFormat(QTextCharFormat())

        for word in misspelled:
            pos = text.find(word)
            while pos != -1:
                cursor.setPosition(pos)
                cursor.movePosition(QTextCursor.NextWord, QTextCursor.KeepAnchor, len(word))
                cursor.mergeCharFormat(format)
                pos = text.find(word, pos + 1)

        # Reconnect the textChanged signal
        self.text_edit.textChanged.connect(self.autoCheckSpelling)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    spell_check_app = SpellCheckApp()
    spell_check_app.show()
    sys.exit(app.exec_())
твой прошлый код был стерт. здесь только английский язык но можно поставть и для русского, нужно в 27 строке указать значение ru. я пробовал сделать два языка сразу но чот не получилось и показывало что все слова не правильыне
