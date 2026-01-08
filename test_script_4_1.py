import pytest
from test_script_4_1_target_library import Library, User, Book, borrow_book


class TestBookBorrowing:
    """测试借书功能"""

    def setup_method(self):
        """每个测试方法前的准备工作"""
        self.library = Library()

        # 添加测试用户
        self.library.add_user(User("U001", "张三"))
        self.library.add_user(User("U002", "李四"))
        self.library.add_user(User("U003", "王五"))

        # 添加测试图书
        self.library.add_book(Book("B001", "Python编程", "Guido", 3))
        self.library.add_book(Book("B002", "算法导论", "Cormen", 1))
        self.library.add_book(Book("B003", "设计模式", "Gamma", 0))  # 库存为0
        self.library.add_book(Book("B004", "数据库系统", "Date", 2))

    def test_borrow_book_success(self):
        """测试正常借书 - 成功情况"""
        # 第一次借阅
        result = borrow_book(self.library, "U001", "B001")
        assert result['success'] == True
        assert "成功借阅" in result['message']
        assert result['remaining_copies'] == 2

        # 验证用户借阅记录
        user = self.library.get_user_info("U001")
        assert "B001" in user.borrowed_books

        # 验证图书库存减少
        book = self.library.get_book_info("B001")
        assert book.copies == 2

    def test_borrow_book_user_not_exist(self):
        """测试异常情况 - 用户不存在"""
        with pytest.raises(ValueError) as exc_info:
            borrow_book(self.library, "U999", "B001")

        assert "用户 U999 不存在" in str(exc_info.value)

    def test_borrow_book_not_exist(self):
        """测试异常情况 - 图书不存在"""
        with pytest.raises(ValueError) as exc_info:
            borrow_book(self.library, "U001", "B999")

        assert "图书 B999 不存在" in str(exc_info.value)

    def test_borrow_book_no_inventory(self):
        """测试异常情况 - 库存为0"""
        with pytest.raises(ValueError) as exc_info:
            borrow_book(self.library, "U001", "B003")

        assert "库存不足" in str(exc_info.value)
        assert "当前库存: 0" in str(exc_info.value)

    def test_borrow_book_already_borrowed(self):
        """测试异常情况 - 重复借阅同一本书"""
        # 第一次借阅成功
        borrow_book(self.library, "U001", "B001")

        # 第二次借阅同本书应该失败
        with pytest.raises(ValueError) as exc_info:
            borrow_book(self.library, "U001", "B001")

        assert "已借阅" in str(exc_info.value)

    def test_borrow_book_multiple_users(self):
        """测试多用户借阅同一本书"""
        # 用户1借阅
        result1 = borrow_book(self.library, "U001", "B002")
        assert result1['success'] == True
        assert result1['remaining_copies'] == 0

        # 用户2尝试借阅（应该失败，因为库存已为0）
        with pytest.raises(ValueError) as exc_info:
            borrow_book(self.library, "U002", "B002")

        assert "库存不足" in str(exc_info.value)

    def test_borrow_book_update_inventory_correctly(self):
        """测试库存更新是否正确"""
        # 初始库存为3
        initial_book = self.library.get_book_info("B001")
        assert initial_book.copies == 3

        # 借阅两次
        borrow_book(self.library, "U001", "B001")
        borrow_book(self.library, "U002", "B001")

        # 验证库存减少到1
        final_book = self.library.get_book_info("B001")
        assert final_book.copies == 1

    def test_borrow_record_keeping(self):
        """测试借阅记录是否正确保存"""
        # 借阅两本书
        borrow_book(self.library, "U001", "B001")
        borrow_book(self.library, "U001", "B004")

        # 验证借阅记录
        assert len(self.library.borrow_records) == 2
        assert self.library.borrow_records[0]['user_id'] == "U001"
        assert self.library.borrow_records[0]['book_id'] == "B001"
        assert self.library.borrow_records[1]['book_id'] == "B004"

    def test_concurrent_borrowing_scenario(self):
        """测试并发借阅场景（模拟）"""
        # 用户1借阅图书B004（库存2）
        result1 = borrow_book(self.library, "U001", "B004")
        assert result1['remaining_copies'] == 1

        # 用户2借阅同一本书
        result2 = borrow_book(self.library, "U002", "B004")
        assert result2['remaining_copies'] == 0

        # 用户3尝试借阅应该失败
        with pytest.raises(ValueError) as exc_info:
            borrow_book(self.library, "U003", "B004")

        assert "库存不足" in str(exc_info.value)

        # 验证每个用户的借阅记录
        user1 = self.library.get_user_info("U001")
        user2 = self.library.get_user_info("U002")
        user3 = self.library.get_user_info("U003")

        assert "B004" in user1.borrowed_books
        assert "B004" in user2.borrowed_books
        assert "B004" not in user3.borrowed_books


if __name__ == "__main__":
    # 运行所有测试
    pytest.main(["-v", __file__])