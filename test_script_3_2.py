# test_dateutil_parser
import pytest
from dateutil.parser import parse
from datetime import datetime
import re


def test_parse_standard_date_format():
    """测试标准日期格式解析 - 正常分支"""
    # 测试ISO格式日期
    result = parse("2023-12-25")
    assert isinstance(result, datetime)
    assert result.year == 2023
    assert result.month == 12
    assert result.day == 25

    # 测试带时间的ISO格式
    result2 = parse("2023-12-25 14:30:00")
    assert result2.hour == 14
    assert result2.minute == 30


def test_parse_human_readable_date():
    """测试人类可读日期格式 - 另一个正常分支"""
    # 测试自然语言格式
    result = parse("December 25, 2023")
    assert result.year == 2023
    assert result.month == 12
    assert result.day == 25

    # 测试简写格式
    result2 = parse("25 Dec 2023")
    assert result2.year == 2023
    assert result2.month == 12
    assert result2.day == 25


def test_parse_with_timezone_info():
    """测试带时区的日期解析 - 包含异常处理分支"""
    # 测试带时区的日期
    result = parse("2023-12-25T14:30:00+08:00")
    assert result.year == 2023
    assert result.hour == 14

    # 测试无效日期 - 触发异常分支
    with pytest.raises(ValueError):
        parse("Not a date string")

    # 测试模糊日期 - 使用模糊解析分支
    result2 = parse("Today is 2023-12-25", fuzzy=True)
    assert result2.year == 2023
    assert result2.month == 12

    # 测试模糊解析关闭时的情况
    with pytest.raises(ValueError):
        parse("Today is 2023-12-25", fuzzy=False)


def test_parse_with_locale_specific():
    """测试区域特定的日期格式 - 覆盖更多分支"""
    # 测试多种分隔符
    test_cases = [
        ("2023/12/25", 2023, 12, 25),
        ("2023.12.25", 2023, 12, 25),
        ("25-12-2023", 2023, 12, 25),  # DD-MM-YYYY格式
    ]

    for date_str, year, month, day in test_cases:
        result = parse(date_str, dayfirst=True)
        assert result.year == year
        assert result.month == month
        assert result.day == day


# 如果需要运行特定测试，可以使用pytest.mark
@pytest.mark.parametrize("date_str,expected", [
    ("2023-12-25", (2023, 12, 25)),
    ("2024-01-01", (2024, 1, 1)),
    ("2022-06-15", (2022, 6, 15)),
])
def test_parse_parametrized(date_str, expected):
    """使用参数化测试多个日期"""
    result = parse(date_str)
    assert (result.year, result.month, result.day) == expected


# 测试日期的组件提取
def test_date_components_extraction():
    """测试日期组件的正确提取"""
    date_strings = [
        "2023-12-25 14:30:45",
        "Dec 25 2023 2:30 PM",
        "25/12/2023 14:30"
    ]

    for date_str in date_strings:
        result = parse(date_str)
        # 验证基本组件都存在
        assert hasattr(result, 'year')
        assert hasattr(result, 'month')
        assert hasattr(result, 'day')
        assert hasattr(result, 'hour')
        assert hasattr(result, 'minute')
        assert hasattr(result, 'second')

        # 验证合理性
        assert 1900 <= result.year <= 2100
        assert 1 <= result.month <= 12
        assert 1 <= result.day <= 31
        assert 0 <= result.hour <= 23
        assert 0 <= result.minute <= 59
        assert 0 <= result.second <= 59


if __name__ == "__main__":
    # 可以直接运行测试
    pytest.main([__file__, "-v"])
