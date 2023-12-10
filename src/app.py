from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QLineEdit,
    QMessageBox,
    QScrollArea,
    QSizePolicy,
    QHeaderView,
)
from PyQt5.QtCore import Qt


class BookManagementSystem(QMainWindow):
    def __init__(self, db_handler):
        super().__init__()
        self.db_handler = db_handler
        self.setup_base_window()

    def setup_base_window(self):
        self.setWindowTitle("Library Management System")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.banner_label = QLabel("Library Management System")
        self.banner_label.setAlignment(Qt.AlignCenter)
        self.banner_label.setStyleSheet("font-size: 32px; color: #8aadf4;")

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.show_main_page)
        self.main_layout.addWidget(self.banner_label)
        self.main_layout.addWidget(self.start_button)

        self.statusBar().showMessage("Welcome to Library Management System")

        self.setStyleSheet(
            """
            *{
                background-color: #24273a;
                color: #cad3f5;
                font-size: 14px;
            }
            QMainWindow {
                background-color: #24273a;
            }

            QPushButton {
                background-color: #8aadf4;
                color: #24273a;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #7dc4e4;
            }
            QLineEdit {
                padding: 6px;
                border: none;
                border-radius: 4px;
                background-color: #363a4f;
                color: #cad3f5;
            }
            QTableWidget {
                border: none;
            }
            QLabel {
                color: #cad3f5;
            }
        """
        )

    def clear_layout(self):
        for i in reversed(range(self.main_layout.count())):
            if widget := self.main_layout.itemAt(i).widget():
                widget.setParent(None)

    def create_button(self, text, clicked_handler):
        button = QPushButton(text)
        button.setMinimumSize(40, 20)
        button.setStyleSheet("padding: 4px 8px; color: #000;")
        button.clicked.connect(clicked_handler)
        return button

    def create_widget(self, layout):
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def create_line_edit(self, text, placeholder=True):
        line_edit = QLineEdit()
        if placeholder:
            line_edit.setPlaceholderText(text)
        else:
            line_edit.setText(text)

        return line_edit

    def create_scroll_area(self, widget):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        scroll_area.setWidget(widget)
        return scroll_area

    def show_main_page(self):
        self.clear_layout()

        if books := self.load_all_books():
            table = QTableWidget(len(books), 6)
            table.setHorizontalHeaderLabels(
                ["ISBN", "Title", "Author", "Year", "Price", "Actions"]
            )

            for row, book in enumerate(books):
                for col, value in enumerate(book):
                    item = QTableWidgetItem(str(value))
                    table.setItem(row, col, item)

                edit_button = self.create_button(
                    "Edit", lambda _, b=book: self.show_edit_book_page(b)
                )
                delete_button = self.create_button(
                    "Delete", lambda _, b=book: self.confirm_delete_book(b)
                )

                layout = QHBoxLayout()
                layout.addWidget(edit_button)
                layout.addWidget(delete_button)

                widget = self.create_widget(layout)

                table.setCellWidget(row, 5, widget)

            scroll_area = self.create_scroll_area(table)

            self.main_layout.addWidget(scroll_area, 1)

            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.horizontalHeader().setStretchLastSection(True)

            vertical_header = table.verticalHeader()
            vertical_header.setDefaultSectionSize(50)

        else:
            message_label = QLabel(
                "No books found. Click the button below to add a new book."
            )
            message_label.setAlignment(Qt.AlignCenter)
            message_label.setStyleSheet("font-size: 24px; color: #8aadf4;")
            self.main_layout.addWidget(message_label)
        add_book_button = QPushButton("Add New Book")
        add_book_button.clicked.connect(self.show_add_book_page)
        self.main_layout.addWidget(add_book_button)

    def show_add_book_page(self):
        self.clear_layout()

        add_book_label = QLabel("Add New Book")
        add_book_label.setStyleSheet("font-size: 24px; color: #8aadf4;")
        add_book_label.setAlignment(Qt.AlignCenter)

        self.isbn_input = self.create_line_edit("ISBN")
        self.title_input = self.create_line_edit("Title")
        self.author_input = self.create_line_edit("Author")
        self.year_input = self.create_line_edit("Year Published")
        self.price_input = self.create_line_edit("Price")

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.add_book)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.show_main_page)

        back_submit_layout = QHBoxLayout()
        back_submit_layout.addWidget(back_button)
        back_submit_layout.addWidget(submit_button)

        year_price_layout = QHBoxLayout()
        year_price_layout.addWidget(self.year_input)
        year_price_layout.addWidget(self.price_input)

        layout = QVBoxLayout()
        layout.addWidget(add_book_label)
        layout.addWidget(self.isbn_input)
        layout.addWidget(self.title_input)
        layout.addWidget(self.author_input)
        layout.addLayout(year_price_layout)
        layout.addLayout(back_submit_layout)

        widget = self.create_widget(layout)
        self.main_layout.addWidget(widget)

    def show_edit_book_page(self, book):
        self.clear_layout()

        edit_book_label = QLabel("Edit Book")
        edit_book_label.setStyleSheet("font-size: 24px; color: #8aadf4;")
        edit_book_label.setAlignment(Qt.AlignCenter)

        self.isbn_input = self.create_line_edit(book[0], placeholder=False)
        self.isbn_input.setReadOnly(True)
        self.title_input = self.create_line_edit(book[1], placeholder=False)
        self.author_input = self.create_line_edit(book[2], placeholder=False)
        self.year_input = self.create_line_edit(str(book[3]), placeholder=False)
        self.price_input = self.create_line_edit(str(book[4]), placeholder=False)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(lambda: self.edit_book(book[0]))

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.show_main_page)

        back_submit_layout = QHBoxLayout()
        back_submit_layout.addWidget(back_button)
        back_submit_layout.addWidget(submit_button)

        year_price_layout = QHBoxLayout()
        year_price_layout.addWidget(self.year_input)
        year_price_layout.addWidget(self.price_input)

        layout = QVBoxLayout()
        layout.addWidget(edit_book_label)
        layout.addWidget(self.isbn_input)
        layout.addWidget(self.title_input)
        layout.addWidget(self.author_input)
        layout.addLayout(year_price_layout)
        layout.addLayout(back_submit_layout)

        widget = self.create_widget(layout)
        self.main_layout.addWidget(widget)

    def add_book(self):
        isbn = self.isbn_input.text()
        title = self.title_input.text()
        author = self.author_input.text()
        year = self.year_input.text()
        price = self.price_input.text()

        if not isbn or not title or not author or not year or not price:
            self.show_error_dialog("All fields must be filled.")
            return

        try:
            year = int(year)
            price = int(price)
            if year < 1900 or year > 2024:
                raise ValueError("Year must be between 1900 and 2024.")
            if price <= 0:
                raise ValueError("Price must be greater than 0.")
        except ValueError as e:
            self.show_error_dialog(str(e))
            return

        if self.is_isbn_duplicate(isbn):
            self.show_error_dialog("ISBN already exists.")
            return

        self.insert_book(isbn, title, author, year, price)
        self.show_success_dialog("Book added successfully.")
        self.show_main_page()

    def edit_book(self, isbn):
        title = self.title_input.text()
        author = self.author_input.text()
        year = self.year_input.text()
        price = self.price_input.text()

        current_values = self.load_book_by_isbn(isbn)
        if (
            title == current_values[1]
            and author == current_values[2]
            and year == str(current_values[3])
            and price == str(current_values[4])
        ):
            self.show_info_dialog("No changes made. Book remains the same.")
            self.show_main_page()
            return

        try:
            year = int(year)
            price = int(price)
            if year < 1900 or year > 2024:
                raise ValueError("Year must be between 1900 and 2024.")
            if price <= 0:
                raise ValueError("Price must be greater than 0.")
        except ValueError as e:
            self.show_error_dialog(str(e))
            return

        if not title or not author:
            self.show_error_dialog("Title and Author fields must be filled.")
            return

        self.update_book(isbn, title, author, year, price)

        self.show_success_dialog("Book updated successfully.")

        self.show_main_page()

    def confirm_delete_book(self, book):
        confirmation = QMessageBox.question(
            self,
            "Confirmation",
            f"Do you want to delete the book with ISBN: {book[0]}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if confirmation == QMessageBox.Yes:
            self.delete_book(book[0])

            self.show_success_dialog("Book deleted successfully.")

            self.show_main_page()

    def load_all_books(self):
        query = "SELECT * FROM book"
        return self.db_handler.fetch_data(query)

    def is_isbn_duplicate(self, isbn):
        query = "SELECT COUNT(*) FROM book WHERE ISBN = %s"
        count = self.db_handler.fetch_data(query, (isbn,))[0][0]
        return count > 0

    def insert_book(self, isbn, title, author, year, price):
        query = "INSERT INTO book (ISBN, title, author, year_published, price) VALUES (%s, %s, %s, %s, %s)"
        self.db_handler.execute_query(query, (isbn, title, author, year, price))

    def update_book(self, isbn, title, author, year, price):
        query = "UPDATE book SET title = %s, author = %s, year_published = %s, price = %s WHERE ISBN = %s"
        self.db_handler.execute_query(query, (title, author, year, price, isbn))

    def delete_book(self, isbn):
        query = "DELETE FROM book WHERE ISBN = %s"
        self.db_handler.execute_query(query, (isbn,))

    def load_book_by_isbn(self, isbn):
        query = "SELECT * FROM book WHERE ISBN = %s"
        return self.db_handler.fetch_data(query, (isbn,))[0]

    def show_success_dialog(self, message):
        QMessageBox.information(self, "Success", message, QMessageBox.Ok)

    def show_error_dialog(self, message):
        QMessageBox.critical(self, "Error", message, QMessageBox.Ok)

    def show_info_dialog(self, message):
        QMessageBox.information(self, "Information", message, QMessageBox.Ok)
