import sys
import os
import ast
import shutil
import tempfile
import webbrowser

from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtGui import QFont, QColor, QKeySequence, QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
    QTreeWidget,
    QTreeWidgetItem,
    QTabWidget,
    QFileDialog,
    QPushButton,
    QLabel,
    QPlainTextEdit,
    QMessageBox,
    QAction,
    QLineEdit,
    QCheckBox,
    QComboBox,
)

from PyQt5.Qsci import (
    QsciScintilla,
    QsciLexerPython,
    QsciLexerJavaScript,
    QsciLexerHTML,
    QsciLexerCSS,
    QsciLexerCPP,
)


# ============================================================
# LANGUAGE INFORMATION
# ============================================================

LANGUAGES = {
    "Python": [".py"],
    "PHP": [".php", ".phtml"],
    "HTML": [".html", ".htm"],
    "CSS": [".css"],
    "JavaScript": [".js", ".jsx", ".mjs"],
    "TypeScript": [".ts", ".tsx"],
    "C": [".c", ".h"],
    "C++": [".cpp", ".cc", ".cxx", ".hpp"],
    "Java": [".java"],
    "C#": [".cs"],
    "Rust": [".rs"],
    "Go": [".go"],
    "Ruby": [".rb"],
    "Kotlin": [".kt", ".kts"],
    "Swift": [".swift"],
    "SQL": [".sql"],
    "JSON": [".json"],
    "XML": [".xml"],
    "Markdown": [".md", ".markdown"],
    "Shell": [".sh", ".bash"],
    "PowerShell": [".ps1"],
    "Lua": [".lua"],
    "Plain Text": [".txt"],
}


def language_for_extension(extension):
    extension = extension.lower()

    for language, extensions in LANGUAGES.items():
        if extension in extensions:
            return language

    return "Plain Text"


# ============================================================
# CODE EDITOR
# ============================================================

class CodeEditor(QsciScintilla):

    def __init__(self, filename=""):
        super().__init__()

        self.filename = filename
        self.zoom_level = 0

        self.setup_editor()
        self.setup_lexer()

    # --------------------------------------------------------
    # EDITOR
    # --------------------------------------------------------

    def setup_editor(self):

        font = QFont("Cascadia Code", 11)

        if not font.exactMatch():
            font = QFont("Consolas", 11)

        self.setFont(font)
        self.setMarginsFont(font)
        self.setUtf8(True)

        self.setTabWidth(4)
        self.setIndentationWidth(4)
        self.setIndentationsUseTabs(False)
        self.setAutoIndent(True)
        self.setIndentationGuides(True)

        self.setBraceMatching(
            QsciScintilla.SloppyBraceMatch
        )

        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(
            QColor("#252526")
        )

        self.setPaper(QColor("#1e1e1e"))
        self.setColor(QColor("#d4d4d4"))

        self.setCaretForegroundColor(
            QColor("#ffffff")
        )

        self.setSelectionBackgroundColor(
            QColor("#264f78")
        )

        self.setSelectionForegroundColor(
            QColor("#ffffff")
        )

        self.setMarginType(
            0,
            QsciScintilla.NumberMargin
        )

        self.setMarginWidth(
            0,
            "00000"
        )

        self.setMarginsBackgroundColor(
            QColor("#181818")
        )

        self.setMarginsForegroundColor(
            QColor("#858585")
        )

        self.setFolding(
            QsciScintilla.BoxedTreeFoldStyle,
            2
        )

        self.setFoldMarginColors(
            QColor("#181818"),
            QColor("#181818")
        )

        self.SendScintilla(
            QsciScintilla.SCI_SETMOUSEWHEELCAPTURES,
            True
        )

        self.SendScintilla(
            QsciScintilla.SCI_SETENDATLASTLINE,
            False
        )

    # --------------------------------------------------------
    # LEXER
    # --------------------------------------------------------

    def setup_lexer(self):

        extension = os.path.splitext(
            self.filename
        )[1].lower()

        lexer = None

        if extension == ".py":
            lexer = QsciLexerPython()

        elif extension in (
            ".js",
            ".jsx",
            ".mjs",
            ".ts",
            ".tsx"
        ):
            lexer = QsciLexerJavaScript()

        elif extension in (
            ".html",
            ".htm",
            ".php",
            ".phtml"
        ):
            lexer = QsciLexerHTML()

        elif extension == ".css":
            lexer = QsciLexerCSS()

        elif extension in (
            ".c",
            ".h",
            ".cpp",
            ".cc",
            ".cxx",
            ".hpp",
            ".java",
            ".cs",
            ".rs",
            ".go",
            ".swift",
            ".kt",
            ".kts"
        ):
            lexer = QsciLexerCPP()

        if lexer is None:
            self.setLexer(None)
            self.setPaper(QColor("#1e1e1e"))
            self.setColor(QColor("#d4d4d4"))
            return

        font = QFont("Cascadia Code", 11)

        if not font.exactMatch():
            font = QFont("Consolas", 11)

        lexer.setDefaultFont(font)
        lexer.setDefaultPaper(QColor("#1e1e1e"))
        lexer.setDefaultColor(QColor("#d4d4d4"))

        for style in range(128):
            try:
                lexer.setPaper(
                    QColor("#1e1e1e"),
                    style
                )

                lexer.setFont(
                    font,
                    style
                )

            except Exception:
                pass

        # ----------------------------------------------------
        # Python
        # ----------------------------------------------------

        if isinstance(lexer, QsciLexerPython):

            lexer.setColor(
                QColor("#d4d4d4"),
                QsciLexerPython.Default
            )

            lexer.setColor(
                QColor("#6A9955"),
                QsciLexerPython.Comment
            )

            lexer.setColor(
                QColor("#CE9178"),
                QsciLexerPython.SingleQuotedString
            )

            lexer.setColor(
                QColor("#CE9178"),
                QsciLexerPython.DoubleQuotedString
            )

            lexer.setColor(
                QColor("#569CD6"),
                QsciLexerPython.Keyword
            )

            lexer.setColor(
                QColor("#B5CEA8"),
                QsciLexerPython.Number
            )

            lexer.setColor(
                QColor("#DCDCAA"),
                QsciLexerPython.FunctionMethodName
            )

            lexer.setColor(
                QColor("#4EC9B0"),
                QsciLexerPython.ClassName
            )

        # ----------------------------------------------------
        # JavaScript / TypeScript
        # ----------------------------------------------------

        elif isinstance(lexer, QsciLexerJavaScript):

            lexer.setColor(
                QColor("#D4D4D4"),
                QsciLexerJavaScript.Default
            )

            lexer.setColor(
                QColor("#6A9955"),
                QsciLexerJavaScript.Comment
            )

            lexer.setColor(
                QColor("#CE9178"),
                QsciLexerJavaScript.SingleQuotedString
            )

            lexer.setColor(
                QColor("#CE9178"),
                QsciLexerJavaScript.DoubleQuotedString
            )

            lexer.setColor(
                QColor("#569CD6"),
                QsciLexerJavaScript.Keyword
            )

            lexer.setColor(
                QColor("#B5CEA8"),
                QsciLexerJavaScript.Number
            )

        # ----------------------------------------------------
        # CSS
        # ----------------------------------------------------

        elif isinstance(lexer, QsciLexerCSS):

            lexer.setColor(
                QColor("#D4D4D4"),
                QsciLexerCSS.Default
            )

            lexer.setColor(
                QColor("#6A9955"),
                QsciLexerCSS.Comment
            )

            lexer.setColor(
                QColor("#CE9178"),
                QsciLexerCSS.DoubleQuotedString
            )

            lexer.setColor(
                QColor("#CE9178"),
                QsciLexerCSS.SingleQuotedString
            )

        # ----------------------------------------------------
        # HTML / PHP
        # ----------------------------------------------------

        elif isinstance(lexer, QsciLexerHTML):

            lexer.setColor(
                QColor("#D4D4D4"),
                QsciLexerHTML.Default
            )

            lexer.setColor(
                QColor("#569CD6"),
                QsciLexerHTML.Tag
            )

            lexer.setColor(
                QColor("#9CDCFE"),
                QsciLexerHTML.Attribute
            )

            lexer.setColor(
                QColor("#CE9178"),
                QsciLexerHTML.DoubleQuotedString
            )

            lexer.setColor(
                QColor("#CE9178"),
                QsciLexerHTML.SingleQuotedString
            )

            lexer.setColor(
                QColor("#6A9955"),
                QsciLexerHTML.Comment
            )

        # ----------------------------------------------------
        # C / C++ / Java / C# / Rust / Go
        # ----------------------------------------------------

        elif isinstance(lexer, QsciLexerCPP):

            lexer.setColor(
                QColor("#D4D4D4"),
                QsciLexerCPP.Default
            )

            lexer.setColor(
                QColor("#6A9955"),
                QsciLexerCPP.Comment
            )

            lexer.setColor(
                QColor("#CE9178"),
                QsciLexerCPP.SingleQuotedString
            )

            lexer.setColor(
                QColor("#CE9178"),
                QsciLexerCPP.DoubleQuotedString
            )

            lexer.setColor(
                QColor("#569CD6"),
                QsciLexerCPP.Keyword
            )

            lexer.setColor(
                QColor("#B5CEA8"),
                QsciLexerCPP.Number
            )

        self.setLexer(lexer)

        self.setPaper(QColor("#1e1e1e"))
        self.setColor(QColor("#d4d4d4"))

        self.setCaretForegroundColor(
            QColor("#ffffff")
        )

        self.setSelectionBackgroundColor(
            QColor("#264f78")
        )

        self.setSelectionForegroundColor(
            QColor("#ffffff")
        )

        self.setCaretLineVisible(True)

        self.setCaretLineBackgroundColor(
            QColor("#252526")
        )

        self.setMarginsBackgroundColor(
            QColor("#181818")
        )

        self.setMarginsForegroundColor(
            QColor("#858585")
        )

    # --------------------------------------------------------
    # SCROLLING
    # --------------------------------------------------------

    def wheelEvent(self, event):

        modifiers = event.modifiers()

        if modifiers & Qt.ControlModifier:

            if event.angleDelta().y() > 0:
                self.zoomIn()
            else:
                self.zoomOut()

            event.accept()
            return

        if modifiers & Qt.ShiftModifier:

            delta = event.angleDelta().y()
            bar = self.horizontalScrollBar()

            bar.setValue(
                bar.value() - delta
            )

            event.accept()
            return

        delta = event.angleDelta().y()

        steps = int(delta / 120)

        if steps == 0:
            steps = 1 if delta > 0 else -1

        speed = 4

        bar = self.verticalScrollBar()

        bar.setValue(
            bar.value()
            - steps * speed * bar.singleStep()
        )

        event.accept()

    # --------------------------------------------------------
    # ZOOM
    # --------------------------------------------------------

    def zoomIn(self):

        if self.zoom_level < 8:
            super().zoomIn()
            self.zoom_level += 1

    def zoomOut(self):

        if self.zoom_level > -5:
            super().zoomOut()
            self.zoom_level -= 1


# ============================================================
# OUTPUT
# ============================================================

class OutputPanel(QPlainTextEdit):

    def __init__(self):
        super().__init__()

        self.setReadOnly(True)

        self.setFont(
            QFont("Cascadia Code", 10)
        )

        self.setStyleSheet("""
            QPlainTextEdit {
                background: #111111;
                color: #d4d4d4;
                border: none;
                padding: 8px;
                selection-background-color: #264f78;
            }

            QScrollBar:vertical {
                background: #111111;
                width: 12px;
            }

            QScrollBar::handle:vertical {
                background: #424242;
                border-radius: 6px;
                min-height: 30px;
            }

            QScrollBar::handle:vertical:hover {
                background: #5a5a5a;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0;
            }
        """)

    def log(self, text):

        if text:
            self.appendPlainText(
                text.rstrip("\n")
            )


# ============================================================
# SEARCH BAR
# ============================================================

class SearchBar(QWidget):

    def __init__(self, editor=None):
        super().__init__()

        self.editor = editor

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(6)

        label = QLabel("Find")

        label.setStyleSheet(
            "color: #aaaaaa; font-weight: bold;"
        )

        layout.addWidget(label)

        self.search = QLineEdit()

        self.search.setPlaceholderText(
            "Search code..."
        )

        self.search.setClearButtonEnabled(True)
        self.search.setMinimumWidth(300)

        self.search.returnPressed.connect(
            self.find_next
        )

        layout.addWidget(self.search)

        self.previous_button = QPushButton("↑")

        self.previous_button.setToolTip(
            "Find previous"
        )

        self.previous_button.clicked.connect(
            self.find_previous
        )

        layout.addWidget(
            self.previous_button
        )

        self.next_button = QPushButton("↓")

        self.next_button.setToolTip(
            "Find next"
        )

        self.next_button.clicked.connect(
            self.find_next
        )

        layout.addWidget(
            self.next_button
        )

        self.case_checkbox = QCheckBox(
            "Match case"
        )

        layout.addWidget(
            self.case_checkbox
        )

        close_button = QPushButton("×")

        close_button.setToolTip(
            "Close search"
        )

        close_button.clicked.connect(
            self.close_search
        )

        layout.addWidget(close_button)

        layout.addStretch()

        self.setStyleSheet("""
            QWidget {
                background: #252526;
                border-bottom: 1px solid #333333;
            }

            QLineEdit {
                background: #1e1e1e;
                color: #dddddd;
                border: 1px solid #444444;
                border-radius: 4px;
                padding: 6px 9px;
            }

            QLineEdit:focus {
                border: 1px solid #007acc;
            }

            QPushButton {
                background: #333333;
                color: #dddddd;
                border: 1px solid #444444;
                border-radius: 4px;
                padding: 5px 10px;
            }

            QPushButton:hover {
                background: #444444;
            }

            QCheckBox {
                color: #aaaaaa;
            }
        """)

        self.search.textChanged.connect(
            self.find_next
        )

    def focus_search(self):

        self.show()
        self.search.setFocus()

        if self.editor and self.editor.hasSelectedText():
            self.search.setText(
                self.editor.selectedText()
            )

        self.search.selectAll()

    def find_next(self):

        if not self.editor:
            return

        text = self.search.text()

        if not text:
            return

        found = self.editor.findFirst(
            text,
            False,
            self.case_checkbox.isChecked(),
            False,
            True,
            True
        )

        if not found:

            self.editor.setCursorPosition(
                0,
                0
            )

            self.editor.findFirst(
                text,
                False,
                self.case_checkbox.isChecked(),
                False,
                True,
                True
            )

    def find_previous(self):

        if not self.editor:
            return

        text = self.search.text()

        if not text:
            return

        line, index = self.editor.getCursorPosition()

        found = self.editor.findFirst(
            text,
            False,
            self.case_checkbox.isChecked(),
            False,
            True,
            False,
            line,
            index
        )

        if not found:

            last_line = self.editor.lines() - 1

            self.editor.setCursorPosition(
                last_line,
                self.editor.lineLength(last_line)
            )

            self.editor.findFirst(
                text,
                False,
                self.case_checkbox.isChecked(),
                False,
                True,
                False
            )

    def close_search(self):

        self.hide()

        if self.editor:
            self.editor.setFocus()


# ============================================================
# MAIN WINDOW
# ============================================================

class PlanscautStudio(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Planscaut Studio")

        if os.path.exists("code_editor_logo.png"):
            self.setWindowIcon(
                QIcon("code_editor_logo.png")
            )

        self.resize(1550, 950)

        self.project_path = None
        self.process = None

        self.build_ui()
        self.build_menu()
        self.build_toolbar()
        self.apply_theme()

        self.new_python_file()

    # ========================================================
    # UI
    # ========================================================

    def build_ui(self):

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        layout.setContentsMargins(
            0, 0, 0, 0
        )

        layout.setSpacing(0)

        main_splitter = QSplitter(
            Qt.Horizontal
        )

        # ----------------------------------------------------
        # EXPLORER
        # ----------------------------------------------------

        explorer = QWidget()

        explorer_layout = QVBoxLayout(
            explorer
        )

        explorer_layout.setContentsMargins(
            0, 0, 0, 0
        )

        explorer_layout.setSpacing(0)

        title = QLabel("  EXPLORER")

        title.setObjectName(
            "panelTitle"
        )

        explorer_layout.addWidget(title)

        self.file_tree = QTreeWidget()

        self.file_tree.setHeaderHidden(True)

        self.file_tree.itemDoubleClicked.connect(
            self.tree_double_click
        )

        explorer_layout.addWidget(
            self.file_tree
        )

        main_splitter.addWidget(
            explorer
        )

        # ----------------------------------------------------
        # CENTER
        # ----------------------------------------------------

        center = QSplitter(
            Qt.Vertical
        )

        editor_container = QWidget()

        editor_layout = QVBoxLayout(
            editor_container
        )

        editor_layout.setContentsMargins(
            0, 0, 0, 0
        )

        editor_layout.setSpacing(0)

        self.tabs = QTabWidget()

        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setDocumentMode(True)

        self.tabs.tabCloseRequested.connect(
            self.close_tab
        )

        self.tabs.currentChanged.connect(
            self.editor_changed
        )

        editor_layout.addWidget(
            self.tabs
        )

        self.search_bar = SearchBar()
        self.search_bar.hide()

        editor_layout.addWidget(
            self.search_bar
        )

        center.addWidget(
            editor_container
        )

        # ----------------------------------------------------
        # OUTPUT
        # ----------------------------------------------------

        output_widget = QWidget()

        output_layout = QVBoxLayout(
            output_widget
        )

        output_layout.setContentsMargins(
            0, 0, 0, 0
        )

        output_header = QHBoxLayout()

        output_title = QLabel(
            "  TERMINAL / OUTPUT"
        )

        output_title.setObjectName(
            "panelTitle"
        )

        output_header.addWidget(
            output_title
        )

        output_header.addStretch()

        clear_button = QPushButton(
            "Clear"
        )

        clear_button.clicked.connect(
            self.clear_output
        )

        output_header.addWidget(
            clear_button
        )

        output_layout.addLayout(
            output_header
        )

        self.output = OutputPanel()

        output_layout.addWidget(
            self.output
        )

        center.addWidget(
            output_widget
        )

        center.setSizes([
            700,
            250
        ])

        main_splitter.addWidget(
            center
        )

        main_splitter.setSizes([
            280,
            1270
        ])

        layout.addWidget(
            main_splitter
        )

        self.statusBar().showMessage(
            "Ready"
        )

    # ========================================================
    # MENU
    # ========================================================

    def build_menu(self):

        menu = self.menuBar()

        file_menu = menu.addMenu("File")

        new_menu = file_menu.addMenu(
            "New File"
        )

        for language, extension in [
            ("Python", ".py"),
            ("PHP", ".php"),
            ("HTML", ".html"),
            ("CSS", ".css"),
            ("JavaScript", ".js"),
            ("TypeScript", ".ts"),
            ("C", ".c"),
            ("C++", ".cpp"),
            ("Java", ".java"),
            ("C#", ".cs"),
            ("Rust", ".rs"),
            ("Go", ".go"),
            ("Ruby", ".rb"),
            ("SQL", ".sql"),
            ("JSON", ".json"),
            ("XML", ".xml"),
            ("Markdown", ".md"),
            ("Plain Text", ".txt"),
        ]:

            action = QAction(
                language,
                self
            )

            action.triggered.connect(
                lambda checked=False,
                ext=extension,
                lang=language:
                self.new_file(ext, lang)
            )

            new_menu.addAction(action)

        file_menu.addSeparator()

        open_action = QAction(
            "Open File...",
            self
        )

        open_action.setShortcut(
            QKeySequence.Open
        )

        open_action.triggered.connect(
            self.open_file
        )

        file_menu.addAction(
            open_action
        )

        folder_action = QAction(
            "Open Folder...",
            self
        )

        folder_action.triggered.connect(
            self.open_folder
        )

        file_menu.addAction(
            folder_action
        )

        file_menu.addSeparator()

        save_action = QAction(
            "Save",
            self
        )

        save_action.setShortcut(
            QKeySequence.Save
        )

        save_action.triggered.connect(
            self.save_file
        )

        file_menu.addAction(
            save_action
        )

        save_as = QAction(
            "Save As...",
            self
        )

        save_as.triggered.connect(
            self.save_as
        )

        file_menu.addAction(
            save_as
        )

        file_menu.addSeparator()

        exit_action = QAction(
            "Exit",
            self
        )

        exit_action.triggered.connect(
            self.close
        )

        file_menu.addAction(
            exit_action
        )

        # ----------------------------------------------------
        # EDIT
        # ----------------------------------------------------

        edit_menu = menu.addMenu("Edit")

        find_action = QAction(
            "Find...",
            self
        )

        find_action.setShortcut(
            QKeySequence.Find
        )

        find_action.triggered.connect(
            self.show_search
        )

        edit_menu.addAction(
            find_action
        )

        # ----------------------------------------------------
        # RUN
        # ----------------------------------------------------

        run_menu = menu.addMenu("Run")

        run_action = QAction(
            "▶ Run",
            self
        )

        run_action.setShortcut("F5")

        run_action.triggered.connect(
            self.run_current
        )

        run_menu.addAction(
            run_action
        )

        check_action = QAction(
            "✓ Check Python Code",
            self
        )

        check_action.setShortcut("F8")

        check_action.triggered.connect(
            self.check_code
        )

        run_menu.addAction(
            check_action
        )

        stop_action = QAction(
            "■ Stop",
            self
        )

        stop_action.setShortcut(
            "Shift+F5"
        )

        stop_action.triggered.connect(
            self.stop_process
        )

        run_menu.addAction(
            stop_action
        )

        # ----------------------------------------------------
        # VIEW
        # ----------------------------------------------------

        view_menu = menu.addMenu("View")

        zoom_in = QAction(
            "Zoom In",
            self
        )

        zoom_in.setShortcut("Ctrl+=")

        zoom_in.triggered.connect(
            self.zoom_in
        )

        view_menu.addAction(
            zoom_in
        )

        zoom_out = QAction(
            "Zoom Out",
            self
        )

        zoom_out.setShortcut("Ctrl+-")

        zoom_out.triggered.connect(
            self.zoom_out
        )

        view_menu.addAction(
            zoom_out
        )

    # ========================================================
    # TOOLBAR
    # ========================================================

    def build_toolbar(self):

        toolbar = self.addToolBar(
            "Main"
        )

        toolbar.setMovable(False)

        new_button = QPushButton(
            "+ New"
        )

        new_button.clicked.connect(
            self.new_python_file
        )

        toolbar.addWidget(
            new_button
        )

        open_button = QPushButton(
            "Open"
        )

        open_button.clicked.connect(
            self.open_file
        )

        toolbar.addWidget(
            open_button
        )

        save_button = QPushButton(
            "Save"
        )

        save_button.clicked.connect(
            self.save_file
        )

        toolbar.addWidget(
            save_button
        )

        toolbar.addSeparator()

        run_button = QPushButton(
            "▶  Run"
        )

        run_button.setObjectName(
            "runButton"
        )

        run_button.clicked.connect(
            self.run_current
        )

        toolbar.addWidget(
            run_button
        )

        check_button = QPushButton(
            "✓  Check"
        )

        check_button.clicked.connect(
            self.check_code
        )

        toolbar.addWidget(
            check_button
        )

        stop_button = QPushButton(
            "■  Stop"
        )

        stop_button.clicked.connect(
            self.stop_process
        )

        toolbar.addWidget(
            stop_button
        )

        toolbar.addSeparator()

        search_button = QPushButton(
            "⌕  Search"
        )

        search_button.clicked.connect(
            self.show_search
        )

        toolbar.addWidget(
            search_button
        )

        toolbar.addSeparator()

        language_label = QLabel(
            " Language:"
        )

        language_label.setStyleSheet(
            "color: #999999; padding-left: 8px;"
        )

        toolbar.addWidget(
            language_label
        )

        self.language_combo = QComboBox()

        self.language_combo.addItems(
            ["All Languages"] +
            list(LANGUAGES.keys())
        )

        self.language_combo.setCurrentText(
            "All Languages"
        )

        toolbar.addWidget(
            self.language_combo
        )

        toolbar.addSeparator()

        zoom_label = QLabel(
            "Ctrl + Wheel = Zoom"
        )

        zoom_label.setStyleSheet(
            "color: #777777; padding-left: 8px;"
        )

        toolbar.addWidget(
            zoom_label
        )

    # ========================================================
    # NEW FILE
    # ========================================================

    def new_file(self, extension, language):

        filename = "untitled" + extension

        editor = CodeEditor(filename)

        if language == "Python":

            editor.setText(
                "# Planscaut Studio\n"
                "# Python\n\n"
                "print(\"Hello from Planscaut Studio!\")\n"
            )

        elif language == "PHP":

            editor.setText(
                "<?php\n\n"
                "echo \"Hello from Planscaut Studio!\";\n\n"
                "?>\n"
            )

        elif language == "HTML":

            editor.setText(
                "<!DOCTYPE html>\n"
                "<html>\n"
                "<head>\n"
                "    <title>Planscaut</title>\n"
                "</head>\n"
                "<body>\n"
                "    <h1>Hello from Planscaut Studio!</h1>\n"
                "</body>\n"
                "</html>\n"
            )

        elif language == "CSS":

            editor.setText(
                "body {\n"
                "    background: #111;\n"
                "    color: white;\n"
                "}\n"
            )

        elif language in (
            "JavaScript",
            "TypeScript"
        ):

            editor.setText(
                "console.log("
                "\"Hello from Planscaut Studio!\""
                ");\n"
            )

        elif language in (
            "C",
            "C++",
            "Java",
            "C#",
            "Rust",
            "Go",
            "Ruby",
        ):

            editor.setText(
                "// Planscaut Studio\n"
                "// " + language + "\n\n"
            )

        else:

            editor.setText(
                "# Planscaut Studio\n\n"
            )

        editor.setModified(False)

        self.add_editor_tab(
            editor,
            filename
        )

    def new_python_file(self):

        self.new_file(
            ".py",
            "Python"
        )

    # ========================================================
    # ADD TAB
    # ========================================================

    def add_editor_tab(
        self,
        editor,
        title
    ):

        editor.modificationChanged.connect(
            lambda modified,
            e=editor:
            self.update_tab_title(e)
        )

        index = self.tabs.addTab(
            editor,
            title
        )

        self.tabs.setCurrentIndex(
            index
        )

        editor.setFocus()

        self.update_search_editor()

    # ========================================================
    # OPEN FILE
    # ========================================================

    def open_file(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "All Languages / Files (*);;"
            "Python (*.py);;"
            "PHP (*.php *.phtml);;"
            "HTML (*.html *.htm);;"
            "CSS (*.css);;"
            "JavaScript (*.js *.jsx *.mjs);;"
            "TypeScript (*.ts *.tsx);;"
            "C/C++ (*.c *.h *.cpp *.cc *.cxx *.hpp);;"
            "Java (*.java);;"
            "C# (*.cs);;"
            "Rust (*.rs);;"
            "Go (*.go);;"
            "Ruby (*.rb);;"
            "SQL (*.sql);;"
            "JSON (*.json);;"
            "XML (*.xml);;"
            "Markdown (*.md *.markdown)"
        )

        if path:
            self.load_file(path)

    def load_file(self, path):

        try:

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as file:

                content = file.read()

        except UnicodeDecodeError:

            try:

                with open(
                    path,
                    "r",
                    encoding="latin-1"
                ) as file:

                    content = file.read()

            except Exception as error:

                QMessageBox.critical(
                    self,
                    "Open Error",
                    str(error)
                )

                return

        except Exception as error:

            QMessageBox.critical(
                self,
                "Open Error",
                str(error)
            )

            return

        editor = CodeEditor(path)

        editor.setText(content)
        editor.setModified(False)

        self.add_editor_tab(
            editor,
            os.path.basename(path)
        )

        self.statusBar().showMessage(
            "Opened " +
            os.path.basename(path)
        )

    # ========================================================
    # SAVE
    # ========================================================

    def save_file(self):

        editor = self.current_editor()

        if editor is None:
            return False

        if (
            not editor.filename
            or editor.filename.startswith("untitled.")
        ):

            return self.save_as()

        try:

            with open(
                editor.filename,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    editor.text()
                )

            editor.setModified(False)

            self.update_tab_title(editor)

            self.statusBar().showMessage(
                "Saved " +
                os.path.basename(editor.filename)
            )

            return True

        except Exception as error:

            QMessageBox.critical(
                self,
                "Save Error",
                str(error)
            )

            return False

    def save_as(self):

        editor = self.current_editor()

        if editor is None:
            return False

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "",
            "All Files (*.*)"
        )

        if not path:
            return False

        editor.filename = path

        editor.setup_lexer()

        self.tabs.setTabText(
            self.tabs.currentIndex(),
            os.path.basename(path)
        )

        return self.save_file()

    # ========================================================
    # CURRENT EDITOR
    # ========================================================

    def current_editor(self):

        widget = self.tabs.currentWidget()

        if isinstance(widget, CodeEditor):
            return widget

        return None

    def editor_changed(self, index):

        self.update_search_editor()

    def update_search_editor(self):

        if not self.search_bar:
            return

        editor = self.current_editor()

        self.search_bar.editor = editor

    # ========================================================
    # SEARCH
    # ========================================================

    def show_search(self):

        editor = self.current_editor()

        if editor is None:
            return

        self.search_bar.editor = editor
        self.search_bar.show()
        self.search_bar.focus_search()

    # ========================================================
    # TABS
    # ========================================================

    def update_tab_title(self, editor):

        index = self.tabs.indexOf(editor)

        if index < 0:
            return

        if editor.filename:

            name = os.path.basename(
                editor.filename
            )

        else:

            name = "untitled.py"

        if editor.isModified():
            name = "● " + name

        self.tabs.setTabText(
            index,
            name
        )

    def close_tab(self, index):

        editor = self.tabs.widget(index)

        if editor is None:
            return

        if editor.isModified():

            result = QMessageBox.question(
                self,
                "Unsaved Changes",
                "This file has unsaved changes.\n\n"
                "Do you want to save it?",
                QMessageBox.Save |
                QMessageBox.Discard |
                QMessageBox.Cancel
            )

            if result == QMessageBox.Save:

                self.tabs.setCurrentIndex(index)

                if not self.save_file():
                    return

            elif result == QMessageBox.Cancel:

                return

        self.tabs.removeTab(index)
        editor.deleteLater()

        if self.tabs.count() == 0:
            self.new_python_file()

    # ========================================================
    # CODE CHECK
    # ========================================================

    def check_code(self):

        editor = self.current_editor()

        if editor is None:
            return

        self.output.clear()

        extension = self.get_extension(editor)

        if extension in ("", ".py"):

            try:

                ast.parse(
                    editor.text()
                )

                self.output.log(
                    "✓ Python syntax is valid."
                )

                self.statusBar().showMessage(
                    "No Python syntax errors"
                )

            except SyntaxError as error:

                line = error.lineno or 1
                column = error.offset or 1

                self.output.log(
                    "✗ PYTHON SYNTAX ERROR"
                )

                self.output.log(
                    f"Line {line}, column {column}"
                )

                self.output.log(
                    error.msg
                )

                self.statusBar().showMessage(
                    f"Syntax error on line {line}"
                )

        elif extension == ".php":

            self.check_php(editor)

        else:

            self.output.log(
                "✓ No built-in syntax checker is "
                "configured for this language yet."
            )

            self.output.log(
                "The editor still provides syntax highlighting."
            )

    def check_php(self, editor):

        php = shutil.which("php")

        if not php:

            self.output.log(
                "PHP syntax checking requires php.exe."
            )

            self.output.log(
                "Install PHP and add it to PATH."
            )

            return

        temp_path = None

        try:

            if (
                editor.filename
                and not editor.filename.startswith("untitled.")
            ):

                path = editor.filename

            else:

                temp_path = os.path.join(
                    tempfile.gettempdir(),
                    "planscaut_check.php"
                )

                with open(
                    temp_path,
                    "w",
                    encoding="utf-8"
                ) as file:

                    file.write(
                        editor.text()
                    )

                path = temp_path

            process = QProcess(self)

            process.start(
                php,
                ["-l", path]
            )

            process.waitForFinished(5000)

            output = bytes(
                process.readAllStandardOutput()
            ).decode(
                "utf-8",
                errors="replace"
            )

            errors = bytes(
                process.readAllStandardError()
            ).decode(
                "utf-8",
                errors="replace"
            )

            result = output + errors

            self.output.log(
                result
                if result
                else "PHP check completed."
            )

        finally:

            if (
                temp_path
                and os.path.exists(temp_path)
            ):

                try:
                    os.remove(temp_path)

                except OSError:
                    pass

    # ========================================================
    # RUN
    # ========================================================

    def run_current(self):

        editor = self.current_editor()

        if editor is None:
            return

        self.output.clear()

        extension = self.get_extension(editor)

        if extension in ("", ".py"):

            self.run_python(editor)

        elif extension == ".php":

            self.run_php(editor)

        elif extension in (
            ".js",
            ".mjs"
        ):

            self.run_javascript(editor)

        elif extension in (
            ".html",
            ".htm"
        ):

            self.run_html(editor)

        else:

            self.output.log(
                f"Running {extension or 'this'} files "
                "is not supported yet."
            )

            self.output.log(
                "You can still edit and save the file."
            )

    def get_extension(self, editor):

        if editor.filename:

            return os.path.splitext(
                editor.filename
            )[1].lower()

        title = self.tabs.tabText(
            self.tabs.currentIndex()
        )

        title = title.replace(
            "● ",
            ""
        )

        return os.path.splitext(
            title
        )[1].lower()

    # ========================================================
    # PYTHON
    # ========================================================

    def run_python(self, editor):

        if (
            not editor.filename
            or editor.filename.startswith("untitled.")
        ):

            run_path = os.path.join(
                tempfile.gettempdir(),
                "planscaut_temp.py"
            )

            try:

                with open(
                    run_path,
                    "w",
                    encoding="utf-8"
                ) as file:

                    file.write(
                        editor.text()
                    )

            except Exception as error:

                self.output.log(
                    "✗ " + str(error)
                )

                return

        else:

            if not self.save_file():
                return

            run_path = editor.filename

        self.output.log(
            "▶ Running Python..."
        )

        self.output.log("")

        self.start_process(
            sys.executable,
            [run_path],
            os.path.dirname(run_path)
        )

    # ========================================================
    # PHP
    # ========================================================

    def run_php(self, editor):

        php = shutil.which("php")

        if not php:

            self.output.log(
                "✗ PHP was not found."
            )

            self.output.log(
                "Install PHP and add php.exe to PATH."
            )

            return

        if (
            not editor.filename
            or editor.filename.startswith("untitled.")
        ):

            run_path = os.path.join(
                tempfile.gettempdir(),
                "planscaut_temp.php"
            )

            try:

                with open(
                    run_path,
                    "w",
                    encoding="utf-8"
                ) as file:

                    file.write(
                        editor.text()
                    )

            except Exception as error:

                self.output.log(
                    "✗ " + str(error)
                )

                return

        else:

            if not self.save_file():
                return

            run_path = editor.filename

        self.output.log(
            "▶ Running PHP..."
        )

        self.output.log("")

        self.start_process(
            php,
            [run_path],
            os.path.dirname(run_path)
        )

    # ========================================================
    # JAVASCRIPT
    # ========================================================

    def run_javascript(self, editor):

        node = shutil.which("node")

        if not node:

            self.output.log(
                "✗ Node.js was not found."
            )

            self.output.log(
                "Install Node.js and add node.exe to PATH."
            )

            return

        if (
            not editor.filename
            or editor.filename.startswith("untitled.")
        ):

            run_path = os.path.join(
                tempfile.gettempdir(),
                "planscaut_temp.js"
            )

            try:

                with open(
                    run_path,
                    "w",
                    encoding="utf-8"
                ) as file:

                    file.write(
                        editor.text()
                    )

            except Exception as error:

                self.output.log(
                    "✗ " + str(error)
                )

                return

        else:

            if not self.save_file():
                return

            run_path = editor.filename

        self.output.log(
            "▶ Running JavaScript..."
        )

        self.start_process(
            node,
            [run_path],
            os.path.dirname(run_path)
        )

    # ========================================================
    # HTML
    # ========================================================

    def run_html(self, editor):

        if (
            not editor.filename
            or editor.filename.startswith("untitled.")
        ):

            path, _ = QFileDialog.getSaveFileName(
                self,
                "Save HTML",
                "",
                "HTML Files (*.html)"
            )

            if not path:
                return

            editor.filename = path

            if not self.save_file():
                return

        else:

            if not self.save_file():
                return

        url = (
            "file:///"
            +
            os.path.abspath(
                editor.filename
            ).replace(
                "\\",
                "/"
            )
        )

        webbrowser.open(url)

        self.output.log(
            "✓ HTML opened in your browser."
        )

    # ========================================================
    # PROCESS
    # ========================================================

    def start_process(
        self,
        program,
        arguments,
        working_directory
    ):

        self.stop_process()

        self.process = QProcess(self)

        if working_directory:
            self.process.setWorkingDirectory(
                working_directory
            )

        self.process.setProcessChannelMode(
            QProcess.MergedChannels
        )

        self.process.readyRead.connect(
            self.read_process_output
        )

        self.process.finished.connect(
            self.process_finished
        )

        self.process.errorOccurred.connect(
            self.process_error
        )

        self.process.start(
            program,
            arguments
        )

        if not self.process.waitForStarted(2000):

            self.output.log(
                "✗ Could not start process."
            )

    def read_process_output(self):

        if not self.process:
            return

        data = self.process.readAll()

        text = bytes(data).decode(
            "utf-8",
            errors="replace"
        )

        if text:
            self.output.log(text)

    def process_finished(
        self,
        exit_code,
        exit_status
    ):

        if exit_code == 0:

            self.output.log("")
            self.output.log(
                "✓ Process finished successfully."
            )

            self.statusBar().showMessage(
                "Finished"
            )

        else:

            self.output.log("")
            self.output.log(
                f"✗ Process exited with code "
                f"{exit_code}."
            )

            self.statusBar().showMessage(
                "Process failed"
            )

        self.process = None

    def process_error(self, error):

        if self.process:

            self.output.log(
                "✗ " +
                self.process.errorString()
            )

    def stop_process(self):

        if self.process:

            if (
                self.process.state()
                != QProcess.NotRunning
            ):

                self.process.kill()

                self.process.waitForFinished(
                    1000
                )

                self.output.log(
                    "■ Process stopped."
                )

            self.process.deleteLater()
            self.process = None

    # ========================================================
    # EXPLORER
    # ========================================================

    def open_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Open Project Folder"
        )

        if not folder:
            return

        self.project_path = folder

        self.file_tree.clear()

        root = QTreeWidgetItem([
            os.path.basename(folder)
        ])

        root.setData(
            0,
            Qt.UserRole,
            folder
        )

        self.file_tree.addTopLevelItem(
            root
        )

        self.populate_tree(
            root,
            folder
        )

        root.setExpanded(True)

        self.statusBar().showMessage(
            "Opened project: " +
            os.path.basename(folder)
        )

    def populate_tree(
        self,
        parent,
        path
    ):

        try:

            names = sorted(
                os.listdir(path),
                key=lambda name: (
                    not os.path.isdir(
                        os.path.join(path, name)
                    ),
                    name.lower()
                )
            )

            for name in names:

                if name.startswith("."):
                    continue

                if name in (
                    "__pycache__",
                    "node_modules",
                    ".git",
                    ".venv",
                    "venv"
                ):
                    continue

                full_path = os.path.join(
                    path,
                    name
                )

                if os.path.isdir(full_path):

                    item = QTreeWidgetItem([
                        "📁 " + name
                    ])

                    item.setData(
                        0,
                        Qt.UserRole,
                        full_path
                    )

                    parent.addChild(item)

                    self.populate_tree(
                        item,
                        full_path
                    )

                else:

                    item = QTreeWidgetItem([
                        "   " + name
                    ])

                    item.setData(
                        0,
                        Qt.UserRole,
                        full_path
                    )

                    parent.addChild(item)

        except PermissionError:
            pass

        except OSError:
            pass

    def tree_double_click(
        self,
        item,
        column
    ):

        path = item.data(
            0,
            Qt.UserRole
        )

        if path and os.path.isfile(path):

            self.load_file(path)

    # ========================================================
    # ZOOM
    # ========================================================

    def zoom_in(self):

        editor = self.current_editor()

        if editor:
            editor.zoomIn()

    def zoom_out(self):

        editor = self.current_editor()

        if editor:
            editor.zoomOut()

    # ========================================================
    # OUTPUT
    # ========================================================

    def clear_output(self):

        self.output.clear()

    # ========================================================
    # KEYBOARD SHORTCUT
    # ========================================================

    def keyPressEvent(self, event):

        if event.matches(
            QKeySequence.Find
        ):

            self.show_search()
            return

        super().keyPressEvent(event)

    # ========================================================
    # THEME
    # ========================================================

# ========================================================
# THEME
# ========================================================

    # ========================================================
    # KEYBOARD SHORTCUT
    # ========================================================

    def keyPressEvent(self, event):

        if event.matches(
            QKeySequence.Find
        ):
            self.show_search()
            return

        super().keyPressEvent(event)

    # ========================================================
    # THEME
    # ========================================================

    def apply_theme(self):

        self.setStyleSheet("""
            QMainWindow {
                background: #0f1117;
                color: #e6e9ef;
            }

            QWidget {
                font-family: "Segoe UI";
                font-size: 10pt;
            }

            QMenuBar {
                background: #11141b;
                color: #b9c0cc;
                border: none;
                padding: 3px 6px;
            }

            QMenuBar::item {
                background: transparent;
                padding: 7px 11px;
                border-radius: 6px;
            }

            QMenuBar::item:hover,
            QMenuBar::item:selected {
                background: #202631;
                color: #ffffff;
            }

            QMenu {
                background: #171b23;
                color: #d9dee8;
                border: 1px solid #2b313d;
                padding: 6px;
            }

            QMenu::item {
                padding: 8px 32px 8px 12px;
            }

            QMenu::item:selected {
                background: #263142;
                color: white;
            }

            QMenu::separator {
                height: 1px;
                background: #2b313d;
                margin: 5px 8px;
            }

            QToolBar {
                background: #11141b;
                border: none;
                border-bottom: 1px solid #252b35;
                padding: 7px 10px;
                spacing: 7px;
            }

            QToolBar::separator {
                background: #2b313d;
                width: 1px;
                margin: 5px;
            }

            QPushButton {
                background: #1b2029;
                color: #cbd2dd;
                border: 1px solid #303744;
                border-radius: 7px;
                padding: 7px 14px;
                min-height: 17px;
            }

            QPushButton:hover {
                background: #252c38;
                border-color: #465161;
                color: white;
            }

            QPushButton:pressed {
                background: #303846;
            }

            QPushButton:disabled {
                color: #626a77;
                background: #171a20;
                border-color: #252a32;
            }

            QPushButton#runButton {
                background: #2563eb;
                color: white;
                border: 1px solid #3b82f6;
                font-weight: bold;
                padding-left: 17px;
                padding-right: 17px;
            }

            QPushButton#runButton:hover {
                background: #3474f0;
                border-color: #60a5fa;
            }

            QPushButton#runButton:pressed {
                background: #1d4ed8;
            }

            QComboBox {
                background: #1b2029;
                color: #cbd2dd;
                border: 1px solid #303744;
                border-radius: 7px;
                padding: 7px 30px 7px 10px;
                min-width: 125px;
            }

            QComboBox:hover {
                border-color: #465161;
            }

            QComboBox:focus {
                border-color: #3b82f6;
            }

            QComboBox::drop-down {
                border: none;
                width: 25px;
            }

            QComboBox QAbstractItemView {
                background: #171b23;
                color: #d9dee8;
                border: 1px solid #303744;
                selection-background-color: #263f68;
                selection-color: white;
                padding: 5px;
            }

            QTreeWidget {
                background: #11141b;
                color: #b8c0cc;
                border: none;
                outline: none;
                padding: 5px 4px;
            }

            QTreeWidget::item {
                padding: 5px 7px;
                margin: 1px 3px;
            }

            QTreeWidget::item:hover {
                background: #1d232d;
                color: #ffffff;
            }

            QTreeWidget::item:selected {
                background: #263142;
                color: #ffffff;
            }

            QLabel#panelTitle {
                background: #11141b;
                color: #7f8998;
                font-size: 10px;
                font-weight: bold;
                padding: 11px 12px 9px 12px;
                border-bottom: 1px solid #252b35;
            }

            QTabWidget::pane {
                background: #141820;
                border: none;
            }

            QTabBar {
                background: #11141b;
            }

            QTabBar::tab {
                background: #171b23;
                color: #747d8b;
                padding: 10px 18px;
                min-width: 100px;
                border: none;
                border-right: 1px solid #11141b;
            }

            QTabBar::tab:hover {
                background: #1d232d;
                color: #cbd2dd;
            }

            QTabBar::tab:selected {
                background: #141820;
                color: #ffffff;
                border-top: 2px solid #3b82f6;
            }

            QStatusBar {
                background: #11141b;
                color: #8993a3;
                border-top: 1px solid #252b35;
                padding: 3px 8px;
            }

            QSplitter::handle {
                background: #20252e;
            }

            QSplitter::handle:hover {
                background: #344052;
            }

            QSplitter::handle:horizontal {
                width: 2px;
            }

            QSplitter::handle:vertical {
                height: 2px;
            }

            QScrollBar:vertical {
                background: #141820;
                width: 12px;
            }

            QScrollBar::handle:vertical {
                background: #343b47;
                min-height: 35px;
                border-radius: 6px;
                margin: 2px;
            }

            QScrollBar::handle:vertical:hover {
                background: #485363;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0;
            }

            QScrollBar:horizontal {
                background: #141820;
                height: 12px;
            }

            QScrollBar::handle:horizontal {
                background: #343b47;
                min-width: 35px;
                border-radius: 6px;
                margin: 2px;
            }

            QScrollBar::handle:horizontal:hover {
                background: #485363;
            }

            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                width: 0;
            }

            QLineEdit {
                background: #171b23;
                color: #e2e6ed;
                border: 1px solid #303744;
                border-radius: 7px;
                padding: 7px 10px;
                selection-background-color: #28518a;
            }

            QLineEdit:hover {
                border-color: #465161;
            }

            QLineEdit:focus {
                border-color: #3b82f6;
            }

            QCheckBox {
                color: #9da6b4;
                spacing: 7px;
            }

            QCheckBox:hover {
                color: #dce1e8;
            }

            QPlainTextEdit {
                background: #0d1015;
                color: #cbd2dd;
                border: none;
                selection-background-color: #264f78;
                padding: 8px;
            }
        """)

    # ========================================================
    # WINDOW CLOSE
    # ========================================================

    def closeEvent(self, event):

        for index in range(
            self.tabs.count() - 1,
            -1,
            -1
        ):

            editor = self.tabs.widget(index)

            if editor and editor.isModified():

                self.tabs.setCurrentIndex(index)

                filename = (
                    os.path.basename(editor.filename)
                    if editor.filename
                    else "untitled"
                )

                result = QMessageBox.question(
                    self,
                    "Unsaved Changes",
                    f"Save changes to {filename}?",
                    QMessageBox.Save |
                    QMessageBox.Discard |
                    QMessageBox.Cancel
                )

                if result == QMessageBox.Save:

                    if not self.save_file():
                        event.ignore()
                        return

                elif result == QMessageBox.Cancel:

                    event.ignore()
                    return

        self.stop_process()
        event.accept()


# ========================================================
# START
# ========================================================

def main():

    app = QApplication(sys.argv)

    app.setApplicationName(
        "Planscaut Studio"
    )

    app.setStyle("Fusion")

    window = PlanscautStudio()

    window.show()

    sys.exit(
        app.exec_()
    )


if __name__ == "__main__":
    main()

# ============================================================
# START
# ============================================================

def main():

    app = QApplication(sys.argv)

    app.setApplicationName(
        "Plancsaut Studio"
    )

    app.setStyle("Fusion")

    window = PlanscautStudio()

    window.show()

    sys.exit(
        app.exec_()
    )


if __name__ == "__main__":
    main()