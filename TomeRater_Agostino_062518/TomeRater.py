class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("New email: {email}".format(email=address))

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        rate = 0
        for ra in self.books.values():
            # print(ra)
            if type(ra) == int:
                rate += ra
        return rate/len(self.books.values())

    def __repr__(self):
        return "User: {user}, email: {email}".format(user=self.name, email=self.email)

    def __eq__(self, other_user):
        if isinstance(other_user, self.__class__):
            return self.name == other_user.name and self.email == other_user.email
        return False


class Book:

    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, newIsbn):
        self.isbn = newIsbn
        print("{book} ISBN has been updated to {isbn}".format(book=self.title, isbn=self.isbn))

    def add_rating(self, rating):
        if rating is not None:
            if rating >= 0 and rating <= 4:
                return self.ratings.append(rating)
            else:
                print("\n Invalid Rating \n")

    def get_average_rating(self):
        if len(self.ratings) != 0:
            self.aver = sum(self.ratings)/len(self.ratings)
            return int(self.aver)
        else:
            return "No ratings"

    def __eq__(self, another_book):
        if isinstance(another_book, self.__class__):
            return self.title == another_book.title and self.isbn == another_book.isbn
        return False

    def __hash__(self):
        return hash((self.title, self.isbn))


class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "\"{title}\" by {author}".format(title=self.title, author=self.author)


class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "\"{title},\" a {level} manual on {subject}".format(title=self.title, level=self.level, subject=self.subject)


class TomeRater:
    def __init__(self):
        self.users = {}
        self.books = {}
        self.isbnDic = {}

    def create_book(self, title, isbn):
        self.isbnDic[title] = isbn
        return Book(title, isbn)

    def create_novel(self, title, author, isbn):
        self.isbnDic[title] = isbn
        return Fiction(title, author, isbn)

    def create_non_fiction(self, title, subject, level, isbn):
        self.isbnDic[title] = isbn
        return Non_Fiction(title, subject, level, isbn)

    def add_book_to_user(self, book, email, rating=None):
        if email not in self.users.keys():
            return "No user with email {}".format(email)
        else:
            self.users[email].read_book(book, rating)
            book.add_rating(rating)
            if book not in self.books.keys():
                self.books[book] = 1
            else:
                self.books[book] += 1

    def add_user(self, name, email, user_books=None):
        validEmail = [".com", ".edu", ".org"]
        if email not in self.users.keys():
            if email[-4:] in validEmail and "@" in email:
                self.users[email] = User(name, email)
                if user_books is not None:
                    for boo in user_books:
                        self.add_book_to_user(boo, email)
            else:
                print("Invalid email for {user} {email}".format(user=name, email=email))
        else:
            print("{} user already exists.".format(self.users[email]))

    def print_catalog(self):
        for boo in self.books.keys():
            print(boo)

    def print_users(self):
        for us in self.users.values():
            print(us)

    def print_isbnDic(self):
        for key, val in self.isbnDic.items():
            print(key, val)

    def get_most_read_book(self):
        newKey = ""
        newVal = 0
        for key, val in self.books.items():
            if val > newVal:
                newVal = val
                newKey = key.title
        return newKey, newVal

    def highest_rated_book(self):
        newKey = ""
        newVal = 0
        for key in self.books.keys():
            if key.get_average_rating() == "No ratings":
                continue
            elif key.get_average_rating() > newVal:
                newVal = key.get_average_rating()
                newKey = key.title
        return newKey, newVal

    def most_positive_user(self):
        posUser = ""
        newVal = 0
        for use in self.users.values():
            if use.get_average_rating() > newVal:
                posUser = use
                newVal = use.get_average_rating()
        return posUser, newVal

    def __repr__(self):
        numUsers = len(self.users.values())
        numBooks = len(self.books.keys())
        return "There are {numUsers} users and {numBooks} books in TomeRater!".format(numUsers=numUsers, numBooks=numBooks)


Tome_Rater = TomeRater()

# Create some books:
book1 = Tome_Rater.create_book("Society of Mind", 12345678)
novel1 = Tome_Rater.create_novel("Alice In Wonderland", "Lewis Carroll", 12345)
novel1.set_isbn(9781536831139)
nonfiction1 = Tome_Rater.create_non_fiction(
    "Automate the Boring Stuff", "Python", "beginner", 1929452)
nonfiction2 = Tome_Rater.create_non_fiction(
    "Computing Machinery and Intelligence", "AI", "advanced", 11111938)
novel2 = Tome_Rater.create_novel("The Diamond Age", "Neal Stephenson", 10101010)
novel3 = Tome_Rater.create_novel("There Will Come Soft Rains", "Ray Bradbury", 10001000)

# Create users:
Tome_Rater.add_user("Alan Turing", "alan@turing.com")
Tome_Rater.add_user("David Marr", "david@computation.org")

# Add a user with three books already read:
Tome_Rater.add_user("Marvin Minsky", "marvin@mit.edu", user_books=[book1, novel1, nonfiction1])

# Add books to a user one by one, with ratings:
Tome_Rater.add_book_to_user(book1, "alan@turing.com", 1)
Tome_Rater.add_book_to_user(novel1, "alan@turing.com", 3)
Tome_Rater.add_book_to_user(nonfiction1, "alan@turing.com", 3)
Tome_Rater.add_book_to_user(nonfiction2, "alan@turing.com", 4)
Tome_Rater.add_book_to_user(novel3, "alan@turing.com", 1)

Tome_Rater.add_book_to_user(novel2, "marvin@mit.edu", 2)
Tome_Rater.add_book_to_user(novel3, "marvin@mit.edu", 2)
Tome_Rater.add_book_to_user(novel3, "david@computation.org", 4)
Tome_Rater.add_book_to_user(novel3, "bin@computation.org", 20)


# Uncomment these to test your functions:
print("\nCatalog: \n")
Tome_Rater.print_catalog()
print("\nUsers: \n")
Tome_Rater.print_users()
print("\nISBN: \n")
Tome_Rater.print_isbnDic()
print("\n \n")
