import pytest
import allure


def pytest_runtest_makereport(item, call):
    """Добавление скриншотов в Allure (для API не нужно, но оставим для совместимости)"""
    pass
