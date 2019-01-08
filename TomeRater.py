class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = { }
        #print("!!! USER "+email+" created")

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        return self.email+" has been changed to: "+address

    def __repr__(self):
        return "User: "+self.name+", "+self.email+", "+"# books "+str(len(self.books))

    def __eq__(self, other_user):
        if other_user.name == self.name and other_user.email == self.email:
            return True
        else:
            return False

    def read_book(self,book,rating=None):
        self.books[book] = rating

    #added ability to disregard "None" ratings in the average calculation
    def get_average_rating(self):
        total=0
        none_count = 0
        for rating in self.books.values():
            try:    
                total+=rating
            except TypeError:
                none_count +=1

        actual_ratings = (len(self.books)-none_count)
        
        return (total/actual_ratings)

class Book(object):
    def __init__(self,title,isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = [ ]

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self,new_isbn):
        self.isbn = new_isbn
        return self.title+" ISBN # has been changed to: "+str(self.isbn)

    def add_rating(self,rating):
        if rating == None:
            pass
        elif rating>=0 and rating<=4:
            self.ratings.append(rating)
        else:
            return "Invalid rating. Please rate 0,1,2,3 or 4 stars."

    def __eq__(self,other_book):
        if self.title == other_book.title and self.isbn == other_book.isbn:
            return True
        else:
            return False

    #written so None does not impact the average rating
    def get_average_rating(self):
        total=0
        none_count=0
        for rating in self.ratings:
            if rating == "None":
                none_count += 1
            else:
                total+=rating

        actual_ratings = (len(self.ratings)-none_count)
        
        return (total/actual_ratings)

    def __hash__(self):
        return hash((self.title, self.isbn))

    def __repr__(self):
        return "{t} ISBN: {i}".format(t=self.title,i=self.isbn) #Book: before {t}

class Fiction(Book):
    def __init__(self,title,author,isbn):
        super().__init__(title,isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{t} by {a}".format(t=self.title,a=self.author)

class Non_Fiction(Book):

    def __init__(self,title,subject,level,isbn):
        super().__init__(title,isbn)
        self.subject = subject
        self.level   = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{t}, a {l} text on {s}".format(t=self.title,l=self.level,s=self.subject)

class TomeRater(object):

    def __init__(self):
        self.users = { }
        self.books = { }

    def create_book(self,title,isbn):
        new_book = Book(title,isbn)
        self.books.update({new_book:None})
        return new_book

    def create_novel(self,title,author,isbn):
        new_novel = Fiction(title,author,isbn)
        self.books.update({new_novel:None})
        return new_novel
        
    def create_non_fiction(self,title,subject,level,isbn):
        new_nf = Non_Fiction(title,subject,level,isbn)
        self.books.update({new_nf:None})
        return new_nf

    def add_book_to_user(self,book,email,rating=None):
        if email in self.users.keys():
            user = self.users[email]
            user.read_book(book,rating)
            book.add_rating(rating)
            if book in self.books:
                if self.books[book]==None:
                    self.books[book] = 1
                elif self.books[book] >= 0:
                    self.books[book] += 1
            else:
                self.books[book] = 1
        else:
            return "No user with email {email}".format(email=email)

    def add_user(self,name,email,user_books=None):
        if email not in self.users.keys():
            new_user = User(name,email)
            self.users.update({email:new_user})
        else:
            return "User already found."
        if user_books != None:
            for book in user_books:
                self.add_book_to_user(book,email)

    def print_catalog(self):
        for book in self.books.keys(): 
            print(book)

    def print_users(self):
        for user in self.users.keys():
            print(user)

    #method returns a list of all books read the most # of times
    def get_most_read_book(self):
        most_read_rating = -111111111
        most_read_list = [ ]
           
        for book in self.books.values():
            if book == None:
                book = 0
            if book>most_read_rating:
                most_read_rating=book
        for key,value in self.books.items():
            if value == most_read_rating:
                most_read_list.append(key)
        return most_read_list

    #returns a list of book(s) with the highest avg rating
    def highest_rated_book(self):
        highest_rating = -1111111 # -math.inf
        rated_highest = [ ]
        avg_ratings = [ ]

        for book in self.books:
            avg_ratings.append(book.get_average_rating())

        rating_dict={key:value for key,value in zip(self.books.keys(),avg_ratings)}

        for rating in rating_dict.values():
            if rating>highest_rating:
                highest_rating=rating
        for key,value in rating_dict.items():
            if value == highest_rating:
                rated_highest.append(key)
        return rated_highest

    #returns a list of user(s) with highest "positivity"
    def most_positive_user(self):
        highest_rating = -11111111
        rated_highest = [ ]
        avg_ratings = [ ]

        for user in self.users.values():
            avg_ratings.append(user.get_average_rating())

        rating_dict={key:value for key,value in zip(self.users.keys(),avg_ratings)}

        for rating in rating_dict.values():
            if rating>highest_rating:
                highest_rating=rating
        for key,value in rating_dict.items():
            if value == highest_rating:
                rated_highest.append(key)
        return rated_highest
