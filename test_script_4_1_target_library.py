class User:
    def __init__(self, user_id, name, borrowed_books=None):
        self.user_id = user_id
        self.name = name
        self.borrowed_books = borrowed_books or []

    def __repr__(self):
        return f"User({self.user_id}, '{self.name}', borrowed={len(self.borrowed_books)})"


class Book:
    def __init__(self, book_id, title, author, copies):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.copies = copies

    def __repr__(self):
        return f"Book({self.book_id}, '{self.title}', copies={self.copies})"


class Library:
    def __init__(self):
        self.users = {}
        self.books = {}
        self.borrow_records = []

    def add_user(self, user):
        """添加用户"""
        if user.user_id in self.users:
            raise ValueError(f"用户ID {user.user_id} 已存在")
        self.users[user.user_id] = user

    def add_book(self, book):
        """添加图书"""
        if book.book_id in self.books:
            raise ValueError(f"图书ID {book.book_id} 已存在")
        self.books[book.book_id] = book

    def borrow_book(self, user_id, book_id):
        """
        【故意破坏逻辑】让用户不存在/图书不存在/库存为0时不抛出预期的ValueError，导致测试失败
        """
        # 1. 破坏「用户不存在」异常：不抛ValueError，反而返回错误字典
        if user_id not in self.users:
            return {
                'success': False,
                'message': f"用户 {user_id} 不存在"
            }

        # 2. 破坏「图书不存在」异常：不抛ValueError，反而抛KeyError（测试预期ValueError，会失败）
        if book_id not in self.books:
            raise KeyError(f"图书 {book_id} 不存在")

        user = self.users[user_id]
        book = self.books[book_id]

        # 3. 破坏「库存为0」异常：不抛异常，反而允许借阅（库存减到负数）
        if book.copies <= 0:
            book.copies -= 1  # 库存变为负数
            user.borrowed_books.append(book_id)
            return {
                'success': True,
                'message': f"用户 {user.name} 借阅了库存为0的图书 '{book.title}'",
                'remaining_copies': book.copies
            }

        # 检查用户是否已借阅该书（保留原逻辑）
        if book_id in user.borrowed_books:
            raise ValueError(f"用户 {user.name} 已借阅图书 '{book.title}'")

        # 正常借书逻辑（保留）
        book.copies -= 1
        user.borrowed_books.append(book_id)
        record = {
            'user_id': user_id,
            'book_id': book_id,
            'timestamp': '2024-01-01'
        }
        self.borrow_records.append(record)

        return {
            'success': True,
            'message': f"用户 {user.name} 成功借阅图书 '{book.title}'",
            'remaining_copies': book.copies
        }

    def get_user_info(self, user_id):
        """破坏用户不存在的异常抛出"""
        if user_id not in self.users:
            return None  # 不抛ValueError，返回None
        return self.users[user_id]

    def get_book_info(self, book_id):
        """破坏图书不存在的异常抛出"""
        if book_id not in self.books:
            return None  # 不抛ValueError，返回None
        return self.books[book_id]


def borrow_book(library, user_id, book_id):
    return library.borrow_book(user_id, book_id)