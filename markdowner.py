import sys
import markdown
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QFileDialog, QSplitter, QVBoxLayout, QWidget


class MarkdownEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.markdown_edit = QTextEdit(self)
        self.html_preview = QTextEdit(self)
        self.html_preview.setReadOnly(True)

        self.markdown_edit.textChanged.connect(self.update_preview)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.markdown_edit)
        splitter.addWidget(self.html_preview)
        splitter.setSizes([400, 400])

        layout = QVBoxLayout()
        layout.addWidget(splitter)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        open_file_action = QAction(f"\U0001F4C2 Open", self)
        open_file_action.triggered.connect(self.open_file)
        save_file_action = QAction(f"\U0001F4BE Save", self)
        save_file_action.triggered.connect(self.save_file)
        quit_action = QAction(f"\U0001F5D1 Quit", self)
        quit_action.triggered.connect(self.close)

        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(open_file_action)
        toolbar.addAction(save_file_action)
        toolbar.addAction(quit_action)

        # Apply custom style to the toolbar and buttons
        toolbar.setStyleSheet("""
            QToolBar {
                background: #2d2d2d;
                border: none;
            }

            QToolButton {
                background: #2d2d2d;
                color: white;
                padding: 5px;
            }

            QToolButton:hover {
                background: #5a5a5a;
            }
        """)

        self.setWindowTitle('Markdowner')
        self.setGeometry(300, 300, 800, 600)
        self.show()

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "Markdown Files (*.md);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                file_content = file.read()
                self.markdown_edit.setPlainText(file_content)

    def save_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "Markdown Files (*.md);;All Files (*)", options=options)
        if file_name:
            markdown_content = self.markdown_edit.toPlainText()
            with open(file_name, 'w') as file:
                file.write(markdown_content)

    def update_preview(self):
        markdown_content = self.markdown_edit.toPlainText()
        html_content = markdown.markdown(markdown_content)
        self.html_preview.setHtml(html_content)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    md_editor = MarkdownEditor()
    sys.exit(app.exec())
