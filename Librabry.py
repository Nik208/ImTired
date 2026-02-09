import os

class Entity:
    def __init__(self, name):
        self._name = name
    
    def name(self):
        return self._name
    
    def to_Savestate(self):
        pass
    
    @classmethod
    def to_Loadstate(cls, line):
        pass

# Классы

class Book(Entity):
    def __init__(self, name, author, status):
        super().__init__(name)
        self._author = author
        self._status = status
        self._belong = "None"

    def author(self):
        return self._author
    def status(self):
        return self._status
    def belong(self):
        return self._belong
    def status(self, value):
        self._status = value
    def belong(self, value):
        self._belong = value
    def to_Savestate(self):
        return f"Book|{self._name}|{self._author}|{self._status}|{self._belong}"
    
    @classmethod
    def to_Loadstate(cls, line):
        parts = line.strip().split('|')
        if len(parts) >= 5 and parts[0] == "Book":
            book = cls(parts[1], parts[2], parts[3] == "True")
            book.belong = parts[4]
            return book
        return None


class Library:
    def __init__(self):
        self._booklist = []
        self._userlist = [] 
        self._librarianlist = []
        self._filesavename = "library_data.txt"
        self._load_data()

    def booklist(self):
        return self._booklist
    def userlist(self):
        return self._userlist
    def librarianlist(self):
        return self._librarianlist
    
    def _save_data(self):
        try:
            
            temp_filename = self._filesavename + "TEMP"  

            with open(temp_filename, 'w', encoding='utf-8') as f:
                
                for book in self._booklist:
                    f.write(book.to_Savestate() + '\n')
                
                for user in self._userlist:
                    f.write(user.to_Savestate() + '\n')

                for librarian in self._librarianlist:
                    f.write(librarian.to_Savestate() + '\n')

            
            if os.path.exists(self._filesavename):
                os.remove(self._filesavename)

            os.rename(temp_filename, self._filesavename)

            

            print("Данные сохранены")
        except Exception:
            print("Ошибка сохранения данных")

    def _load_data(self):
        try:
            with open(self._filesavename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            self._booklist = []
            self._userlist = []
            self._librarianlist = []

            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                if line.startswith("Book|"):
                    book = Book.to_Loadstate(line)
                    if book:
                        self._booklist.append(book)
                
                elif line.startswith("User|"):
                    user = User.to_Loadstate(line)
                    if user:
                        self._userlist.append(user)
                
                elif line.startswith("Librarian|"):
                    librarian = Librarians.to_Loadstate(line)
                    if librarian:
                        self._librarianlist.append(librarian)

        except Exception as e:
            print(f"Ошибка загрузки данных {e}")
    
    def addBook(self, librarian):
        OpStatus = False
        for librarian1 in self._librarianlist:
            if librarian == librarian1.name(): 
                OpStatus = True
                print("-----Новая Книга-----")
                NameI = input("Введите название книги")
                AuthorI = input("Введите автора книги")
                StatusI = True
                AddedBook = Book(NameI, AuthorI, StatusI)
                self._booklist.append(AddedBook) 
                print(f"\n Книга {NameI} Добавлена")
                input()
                break
        if OpStatus == True:
            return
        if OpStatus == False:
            print("Библиотекарь не найден")
            input()
        

    def delBook(self, librarian):
        Nfound = True
        OpStatus = False
        for librarian1 in self._librarianlist:
            if librarian == librarian1.name():
                OpStatus = True
                print("-----Удаление Книги-----")
                NameD = input("Введите название книги: ")
                for i, Book in enumerate(self._booklist):
                    if Book.name() == NameD:
                        deleted = self._booklist.pop(i)
                        for user in self._userlist:
                            for i, book in enumerate(user.borrowlist()): 
                                if book == deleted.name():
                                    user.borrowlist().pop(i) 
                        print(f"Книга: {NameD} Удалена")
                        input()
                        Nfound = False
                        break
                    if Nfound:
                        print("Книга не найдена")
                        input()
        if OpStatus == True:
            return
        if OpStatus == False:
            print("Библиотекарь не найден")
            input()

    def viewBooks(self, librarian):
        OpStatus = False
        for librarian1 in self._librarianlist:
            if librarian == librarian1.name():  
                for Book in self._booklist:
                    print(f"Название: {Book.name()}") 
                    print(f"Автор: {Book.author()}") 
                    print(f"Свободна?: {Book.status()}") 
                    print(f"Кем Занята?: {Book.belong()} \n")  
                    input()
        if OpStatus == True:
            return
        if OpStatus == False:
            print("Библиотекарь не найден")
            input()

    def userAdd(self, librarian):
        OpStatus = False
        for librarian1 in self._librarianlist:
            if librarian == librarian1.name(): 
                OpStatus = True
                print("-----Новый Пользователь-----")
                NameU = input("Введите имя пользователя: ")
                AddedUser = User(NameU)
                self._userlist.append(AddedUser) 
                input()
        if OpStatus == True:
            return
        if OpStatus == False:
            print("Библиотекарь не найден")
            input()

    def viewUsers(self, librarian):
        OpStatus = False
        for librarian1 in self._librarianlist:
            if librarian == librarian1.name(): 
                OpStatus = True
                for User in self._userlist:
                    print(f"Имя Пользователя: {User.name()} \n")  
                    input()
        if OpStatus == True:
            return
        if OpStatus == False:
            print("Библиотекарь не найден")
            input()

    def viewFree(self):
        print("---- Список свободных книг: ----")
        for Book in self._booklist:
            if Book.status() == 1: 
                print(f"Название: {Book.name()}") 
                print(f"Автор: {Book.author()}") 
                input()

    def BorrowBook(self, user):
        Nfound = True
        for user1 in self._userlist:
            if user1.name() == user: 
                print("---- Выбор книги ----")
                Borrow = input("Напишите какую книгу вы хотите забрать: ")
                for Book in self._booklist:
                    if Book.name() == Borrow and Book.status() == True: 
                        Book.status = False
                        Book.belong = user1.name()
                        user1.borrowlist().append(Borrow) 
                        print(f"Книга: {Borrow} Выдана")
                        Nfound = False
                        input()
                        break
                if Nfound:
                    print("Книга уже выдана или не найдена")
                    input()

    def BorrowView(self, user):
        for user1 in self._userlist:
            if user1.name() == user:  
                print("---- Список выданых книг: ----")
                for Book in user1.borrowlist():  
                    print(f"Одолжена книга: {Book}")
                    input()

    def Return(self, user):
        Nfound = True
        for user1 in self._userlist:
            if user1.name() == user: 
                print("---- Возращение книги ----")
                BB = input("Напишите какую книгу вы вернуть: ")
                for i, Book in enumerate(user1.borrowlist()): 
                    for BookName in self._booklist:
                        if Book == BookName.name(): 
                            if BookName.name() == BB and BookName.status() == False and BookName.belong() == user1.name():  # КРИТИЧЕСКОЕ: добавлены скобки
                                for BookI in self._booklist:
                                    if BookI.name() == BB: 
                                        BookI.status = True
                                        BookI.belong = "None"
                                        break
                                user1.borrowlist().pop(i) 
                                print(f"Книга: {BB} Отдана")
                                Nfound = False
                                input()
                                break
                    if Nfound:
                        print("Книга не найдена или уже в библиотеке")
                        input()


class LibraryUser(Entity):
    def __init__(self, name):
        super().__init__(name)
    
    def get_role(self):
        pass


class Librarians(LibraryUser):
    def __init__(self, name):
        super().__init__(name)

    def get_role(self):
        return "Библиотекарь"

    def to_Savestate(self):
        return f"Librarian|{self._name}"
    
    @classmethod
    def to_Loadstate(cls, line):
        parts = line.strip().split('|')
        if len(parts) >= 2 and parts[0] == "Librarian":
            return cls(parts[1])
        return None


class User(LibraryUser):
    def __init__(self, name):
        super().__init__(name)
        self._borrowlist = []

    def borrowlist(self):
        return self._borrowlist

    def get_role(self):
        return "Пользователь"

    def to_Savestate(self):
        books_str = ','.join(self._borrowlist)
        return f"User|{self._name}|{books_str}"
    
    @classmethod
    def to_Loadstate(cls, line):
        parts = line.strip().split('|')
        if len(parts) >= 3 and parts[0] == "User":
            user = cls(parts[1])
            if parts[2]: 
                user._borrowlist = parts[2].split(',') 
            return user
        return None





# КОД

Library1 = Library()
RoleLoop = True
LoginLoop = True
AllTimeLoop = True


try:
    print("Добро пожаловать в Библиотеку!")
    print("Кем вы являетесь? (1. Библиотекарь / 2. Пользоваетль)")
    print("Введите числом")
    while RoleLoop:
        Role = int(input())
        if Role == 1:
            RoleLoop = False
            while LoginLoop:
                print("Введите ваше Имя")
                LoginName = input()
                for Librarian in Library1._librarianlist: 
                    found = Librarian.name() == LoginName  
                    LoginLoop = False
                    print(f"Добро Пожаловать {LoginName}")
                    if isinstance(Librarian, LibraryUser):
                        print(f"Ваша роль: {Librarian.get_role()}")
                    while AllTimeLoop:
                        print("Выберите действие (числом):")
                        print("1. Добавить книгу в библиотеку \n" \
                        "2. Удалить книгу из библиотеки \n" \
                        "3. Зарегестрировать нового пользователя \n" \
                        "4. посмотреть список пользователей \n" \
                        "5. посмотреть список книг и их статусы \n" \
                        "0. Выйти")
                        Act = int(input())
                        if Act == 1:
                            Library1.addBook(LoginName)
                        elif Act == 2:
                            Library1.delBook(LoginName)
                        elif Act == 3:
                            Library1.userAdd(LoginName)
                        elif Act == 4:
                            Library1.viewUsers(LoginName)
                        elif Act == 5:
                            Library1.viewBooks(LoginName)
                        elif Act == 0:
                            print("Выход..")
                            Library1._save_data()
                            AllTimeLoop = False
                            break
                        else:
                            print("Некорректный ввод")
                else:
                    print("Логин не найден, попробуйте ещё раз")
        elif Role == 2:
            RoleLoop = False
            while LoginLoop:
                print("Введите ваше Имя")
                LoginName = input()
                for user in Library1._userlist: 
                    found = user.name() == LoginName 
                    if found:
                        LoginLoop = False
                        print(f"Добро Пожаловать {LoginName}")
                        if isinstance(user, LibraryUser):
                            print(f"Ваша роль: {user.get_role()}")
                        while AllTimeLoop:
                            print("Выберите действие (числом):")
                            print("1. Посмотреть доступные книги \n" \
                            "2. Взять книгу \n" \
                            "3. Вернуть книгу \n" \
                            "4. Просмотреть взятые книги \n" \
                            "0. Выйти")
                            Act = int(input())
                            if Act == 1:
                                Library1.viewFree()
                            elif Act == 2:
                                Library1.BorrowBook(LoginName)
                            elif Act == 3:
                                Library1.Return(LoginName)
                            elif Act == 4:
                                Library1.BorrowView(LoginName)
                            elif Act == 0:
                                print("Выход..")
                                Library1._save_data()
                                break
                            else:
                                print("Некорректный ввод")
        else: 
            print("Неправильный ввод числа")
except ValueError:
    print("Некорректный ввод")