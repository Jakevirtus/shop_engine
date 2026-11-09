from unittest.mock import patch

from src.models import Category, Product


def test_product_initialization():
    """Тест инициализации Product и геттера цены."""
    product = Product("Samsung", "256GB", 180000.0, 5)
    assert product.name == "Samsung"
    assert product.description == "256GB"
    assert product.price == 180000.0
    assert product.quantity == 5


def test_price_setter_valid():
    """Тест сеттера цены (корректное значение)."""
    product = Product("Samsung", "256GB", 180000.0, 5)
    product.price = 200000.0
    assert product.price == 200000.0


def test_price_setter_invalid(capsys):
    """Тест сеттера цены (некорректное значение)."""
    product = Product("Samsung", "256GB", 180000.0, 5)
    product.price = -100.0

    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product.price == 180000.0


@patch("builtins.input", side_effect=["n"])
def test_price_setter_decrease_cancel(mock_input):
    """Тест отмены понижения цены."""
    product = Product("Samsung", "256GB", 180000.0, 5)
    product.price = 150000.0
    assert product.price == 180000.0


@patch("builtins.input", side_effect=["y"])
def test_price_setter_decrease_confirm(mock_input):
    """Тест подтверждения понижения цены."""
    product = Product("Samsung", "256GB", 180000.0, 5)
    product.price = 150000.0
    assert product.price == 150000.0


def test_category_initialization(sample_category):
    """Тест инициализации Category и геттера products."""
    assert sample_category.name == "Смартфоны"
    assert "Iphone 15, 210000.0 руб. Остаток: 8 шт." in sample_category.products


def test_add_product():
    """Тест добавления товара через метод add_product."""
    # Сбрасываем счетчик в ноль, чтобы тест не зависел от других тестов
    Category.product_count = 0

    category = Category("Пустая", "Описание", [])
    assert Category.product_count == 0

    product = Product("Телефон", "Хороший", 10000.0, 2)
    category.add_product(product)

    assert "Телефон, 10000.0 руб. Остаток: 2 шт." in category.products
    assert Category.product_count == 1


def test_new_product_classmethod():
    """Тест класс-метода new_product."""
    data = {
        "name": "Ноутбук",
        "description": "Мощный",
        "price": 50000.0,
        "quantity": 3,
    }
    product = Product.new_product(data)
    assert product.name == "Ноутбук"
    assert product.price == 50000.0


def test_new_product_duplicate_bonus():
    """Тест объединения дубликатов (доп. задание)."""
    existing_prod = Product("Ноутбук", "Мощный", 50000.0, 3)
    existing_list = [existing_prod]

    data = {
        "name": "Ноутбук",
        "description": "Мощный",
        "price": 55000.0,
        "quantity": 2,
    }
    product = Product.new_product(data, existing_list)

    assert product.quantity == 5
    assert product.price == 55000.0
