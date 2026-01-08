import pytest

# ---------------------- 待测试的有缺陷函数 ----------------------
def divide(a, b):
    return a / b   # 缺陷1: 未检查除数为0，会抛出ZeroDivisionError

def find_max(lst):
    max_val = 0    # 缺陷2: 列表全为负数时，返回0（错误）而非真实最大值
    for x in lst:
        if x > max_val:
            max_val = x
    return max_val

def get_item(lst, idx):
    return lst[idx]  # 缺陷3: 未检查索引越界，会抛出IndexError

# ---------------------- 测试用例 ----------------------
def test_divide_normal_case_tc001():
    """TC001: divide正常场景 - a=10，b=2"""
    # 预期结果：5.0，实际执行结果：5.0（用例通过）
    assert divide(10, 2) == 5.0

def test_divide_zero_division_tc002():
    """TC002: divide除数为0场景 - a=10，b=0"""
    # 预期结果：抛出ZeroDivisionError，实际执行结果：抛出该异常（缺陷触发，用例通过）
    with pytest.raises(ZeroDivisionError) as exc_info:
        divide(10, 0)
    # 验证异常信息准确性
    assert "division by zero" in str(exc_info.value)

def test_find_max_positive_list_tc003():
    """TC003: find_max正整数列表 - lst=[1, 3, 5, 2]"""
    # 预期结果：5，实际执行结果：5（用例通过）
    assert find_max([1, 3, 5, 2]) == 5

def test_find_max_all_negative_tc004():
    """TC004: find_max全负数列表 - lst=[-5, -3, -10, -1]"""
    # 预期结果：-1，实际执行结果：0（缺陷触发，用例失败）
    assert find_max([-5, -3, -10, -1]) == -1

def test_get_item_valid_index_tc005():
    """TC005: get_item合法索引 - lst=[10,20,30,40]，idx=2"""
    # 预期结果：30，实际执行结果：30（用例通过）
    assert get_item([10, 20, 30, 40], 2) == 30

def test_get_item_out_of_range_positive_tc006():
    """TC006: get_item正索引越界 - lst=[10,20,30,40]，idx=4"""
    # 预期结果：抛出IndexError，实际执行结果：抛出该异常（缺陷触发，用例通过）
    with pytest.raises(IndexError) as exc_info:
        get_item([10, 20, 30, 40], 4)
    assert "list index out of range" in str(exc_info.value)

def test_get_item_out_of_range_negative_tc007():
    """TC007: get_item负索引越界 - lst=[10,20,30,40]，idx=-5"""
    # 预期结果：抛出IndexError，实际执行结果：抛出该异常（缺陷触发，用例通过）
    with pytest.raises(IndexError) as exc_info:
        get_item([10, 20, 30, 40], -5)
    assert "list index out of range" in str(exc_info.value)

def test_find_max_mixed_list_tc008():
    """TC008: find_max正负数混合列表 - lst=[-2, 4, -7, 9]"""
    # 预期结果：9，实际执行结果：9（用例通过）
    assert find_max([-2, 4, -7, 9]) == 9