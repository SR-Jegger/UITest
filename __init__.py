"""
Test Agent - Markdown驱动的自动化测试框架

支持PyQt5 UI自动化测试和API测试
"""

__version__ = "1.0.0"
__author__ = "Test Agent Team"

from .parser.markdown_parser import MarkdownTestParser, TestCase, TestStep
from .executor.test_executor import TestExecutor, TestResult

__all__ = [
    "MarkdownTestParser",
    "TestCase", 
    "TestStep",
    "TestExecutor",
    "TestResult"
]
