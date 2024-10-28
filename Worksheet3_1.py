# Maria Estrada - Worksheet 3.1 Abstraction 

class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.__isbn = isbn
        self.__is_checked_out = False

    # Public method to get book details
    def get_details(self):
        return {
            'Title': self.title,
            'Author': self.author,
            'ISBN': self.__isbn,
            'Available': not self.__is_checked_out
        }

    def check_out(self):
        # If book is checked in True - If book is checked out False
        if not self.__is_checked_out:
            self.__is_checked_out = True
            return True
        return False

    def return_book(self):
        self.__is_checked_out = False


class Member:
    # Keep member details private
    def __init__(self, name, member_id):
        self.__name = name
        self.__member_id = member_id
        self.__checked_out_books = []

    #Public method to get member details
    def get_member_details(self):
        return {
            'Name': self.__name,
            'Member ID': self.__member_id,
            'Books Checked Out': [book.get_details()['Title'] for book in self.__checked_out_books]
        }

    # Let member check out book if in library
    def check_out_book(self, book):
        if book.check_out():
            self.__checked_out_books.append(book)
            return f"{self.__name} checked out '{book.get_details()['Title']}'." #------------------
        return f"'{book.get_details()['Title']}' is not available."

    def return_book(self, book):
        if book in self.__checked_out_books:
            book.return_book()
            self.__checked_out_books.remove(book)
            return f"{self.__name} returned '{book.get_details()['Title']}'."


class Library:
    def __init__(self):
        self.__books = []
        self.__members = []

    #Add new book to library
    def add_book(self, book):
        self.__books.append(book)

    # Add new member to library
    def add_member(self, member):
        self.__members.append(member)

    # List of all books and status
    def list_books(self):
        return [book.get_details() for book in self.__books]

    # List of all members and checked out books
    def list_members(self):
        return [member.get_member_details() for member in self.__members]

    # Check out a book to a member
    def check_out_book(self, member, book_title):
        for book in self.__books:
            if book.get_details()['Title'] == book_title:
                return member.check_out_book(book)
        return f"Book '{book_title}' not found in the library."

    # Return book
    def return_book(self, member, book_title):
        for book in member.get_member_details()['Books Checked Out']:
            if book == book_title:
                return member.return_book(book)
        return f"Book '{book_title}' is not checked out."

library = Library()

# Adding books to the library
book1 = Book("1984", "George Orwell", "123456789")
book2 = Book("To Kill a Mockingbird", "Harper Lee", "987654321")
library.add_book(book1)
library.add_book(book2)

# Adding a member
member1 = Member("Maria", "12345")
library.add_member(member1)

# Listing books
print()
print("Books in the library:", library.list_books())
print()

# Member checking out a book
print(member1.check_out_book(book1))
print()

# Listing books after checkout
print("Books in the library after checkout:", library.list_books())
print()

# Returning the book
print(member1.return_book(book1))
print()

# Listing books after return
print("Books in the library after return:", library.list_books())
print()
