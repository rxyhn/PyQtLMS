import sys
from PyQt5.QtWidgets import (
    QApplication,
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
import mysql.connector

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "BMS"

db_connection = mysql.connector.connect(
    host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, database=DB_NAME
)
cursor = db_connection.cursor()


class BookManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.setWindowTitle("Library Management System")
        self.setGeometry(100, 100, 800, 600)

        self.setStyleSheet(
            """
            *{
                background-color: #24273a;
                color: #cad3f5;
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
                font-size: 18px;
                margin-bottom: 6px;
            }
        """
        )

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.show_main_page)
        self.main_layout.addWidget(self.start_button)

    def clear_layout(self):
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

    def show_main_page(self):
        self.clear_layout()

        books = self.load_all_books()

        if not books:
            message_label = QLabel(
                "No books found. Click the button below to add a new book."
            )
            self.main_layout.addWidget(message_label)
        else:
            table = QTableWidget(len(books), 6)
            table.setHorizontalHeaderLabels(
                ["ISBN", "Title", "Author", "Year", "Price", "Actions"]
            )

            for row, book in enumerate(books):
                for col, value in enumerate(book):
                    item = QTableWidgetItem(str(value))
                    table.setItem(row, col, item)

                edit_button = QPushButton("Edit")
                edit_button.setMinimumSize(40, 20)
                edit_button.setStyleSheet("padding: 4px 8px; color: #000;")
                edit_button.clicked.connect(
                    lambda _, b=book: self.show_edit_book_page(b)
                )

                delete_button = QPushButton("Delete")
                delete_button.setMinimumSize(40, 20)
                delete_button.setStyleSheet("padding: 4px 8px; color: #000;")
                delete_button.clicked.connect(
                    lambda _, b=book: self.confirm_delete_book(b)
                )

                layout = QHBoxLayout()
                layout.addWidget(edit_button)
                layout.addWidget(delete_button)

                widget = QWidget()
                widget.setLayout(layout)

                table.setCellWidget(row, 5, widget)

            # Use QScrollArea to contain the table
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)

            table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            scroll_area.setWidget(table)

            self.main_layout.addWidget(scroll_area, 1)

            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.horizontalHeader().setStretchLastSection(True)

            vertical_header = table.verticalHeader()
            vertical_header.setDefaultSectionSize(50)

        add_book_button = QPushButton("Add New Book")
        add_book_button.clicked.connect(self.show_add_book_page)
        self.main_layout.addWidget(add_book_button)

    def show_add_book_page(self):
        self.clear_layout()

        add_book_label = QLabel("Add New Book:")
        isbn_label = QLabel("ISBN:")
        title_label = QLabel("Title:")
        author_label = QLabel("Author:")
        year_label = QLabel("Year Published:")
        price_label = QLabel("Price:")

        self.isbn_input = QLineEdit()
        self.title_input = QLineEdit()
        self.author_input = QLineEdit()
        self.year_input = QLineEdit()
        self.price_input = QLineEdit()

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.add_book)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.show_main_page)

        layout = QVBoxLayout()
        layout.addWidget(add_book_label)
        layout.addWidget(isbn_label)
        layout.addWidget(self.isbn_input)
        layout.addWidget(title_label)
        layout.addWidget(self.title_input)
        layout.addWidget(author_label)
        layout.addWidget(self.author_input)
        layout.addWidget(year_label)
        layout.addWidget(self.year_input)
        layout.addWidget(price_label)
        layout.addWidget(self.price_input)
        layout.addWidget(submit_button)
        layout.addWidget(back_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.main_layout.addWidget(widget)

    def show_edit_book_page(self, book):
        self.clear_layout()

        edit_book_label = QLabel("Edit Book:")
        isbn_label = QLabel("ISBN:")
        title_label = QLabel("Title:")
        author_label = QLabel("Author:")
        year_label = QLabel("Year Published:")
        price_label = QLabel("Price:")

        self.isbn_input = QLineEdit(book[0])
        self.isbn_input.setReadOnly(True)
        self.title_input = QLineEdit(book[1])
        self.author_input = QLineEdit(book[2])
        self.year_input = QLineEdit(str(book[3]))
        self.price_input = QLineEdit(str(book[4]))

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(lambda: self.edit_book(book[0]))

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.show_main_page)

        layout = QVBoxLayout()
        layout.addWidget(edit_book_label)
        layout.addWidget(isbn_label)
        layout.addWidget(self.isbn_input)
        layout.addWidget(title_label)
        layout.addWidget(self.title_input)
        layout.addWidget(author_label)
        layout.addWidget(self.author_input)
        layout.addWidget(year_label)
        layout.addWidget(self.year_input)
        layout.addWidget(price_label)
        layout.addWidget(self.price_input)
        layout.addWidget(submit_button)
        layout.addWidget(back_button)

        widget = QWidget()
        widget.setLayout(layout)
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

        # Check if any changes were made
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

    def delete_book(self, isbn):
        try:
            query = "DELETE FROM book WHERE ISBN = %s"
            cursor.execute(query, (isbn,))
            db_connection.commit()
        except mysql.connector.Error as err:
            self.show_error_dialog(f"Error deleting book: {err}")

    def load_all_books(self):
        try:
            query = "SELECT * FROM book"
            cursor.execute(query)
            books = cursor.fetchall()
            return books
        except mysql.connector.Error as err:
            self.show_error_dialog(f"Error loading books: {err}")
            return []

    def is_isbn_duplicate(self, isbn):
        try:
            query = "SELECT COUNT(*) FROM book WHERE ISBN = %s"
            cursor.execute(query, (isbn,))
            count = cursor.fetchone()[0]
            return count > 0
        except mysql.connector.Error as err:
            self.show_error_dialog(f"Error checking duplicate ISBN: {err}")
            return False

    def insert_book(self, isbn, title, author, year, price):
        try:
            query = "INSERT INTO book (ISBN, title, author, year_published, price) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (isbn, title, author, year, price))
            db_connection.commit()
        except mysql.connector.Error as err:
            self.show_error_dialog(f"Error inserting book: {err}")

    def update_book(self, isbn, title, author, year, price):
        try:
            query = "UPDATE book SET title = %s, author = %s, year_published = %s, price = %s WHERE ISBN = %s"
            cursor.execute(query, (title, author, year, price, isbn))
            db_connection.commit()
        except mysql.connector.Error as err:
            self.show_error_dialog(f"Error updating book: {err}")

    def load_book_by_isbn(self, isbn):
        try:
            query = "SELECT * FROM book WHERE ISBN = %s"
            cursor.execute(query, (isbn,))
            book = cursor.fetchone()
            return book
        except mysql.connector.Error as err:
            self.show_error_dialog(f"Error loading book by ISBN: {err}")
            return None

    def show_success_dialog(self, message):
        QMessageBox.information(self, "Success", message, QMessageBox.Ok)

    def show_error_dialog(self, message):
        QMessageBox.critical(self, "Error", message, QMessageBox.Ok)

    def show_info_dialog(self, message):
        QMessageBox.information(self, "Information", message, QMessageBox.Ok)


def main():
    app = QApplication(sys.argv)
    main_window = BookManagementSystem()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()