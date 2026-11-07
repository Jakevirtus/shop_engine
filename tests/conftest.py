import pytest

from src.models import Category, Product


@pytest.fixture
def sample_products():
    """Фикстура со списком товаров."""
    return [
        Product("Iphone 15", "512GB", 210000.0, 8),
        Product("Xiaomi", "1024GB", 31000.0, 14),
    ]


@pytest.fixture
def sample_category(sample_products):
    """Фикстура с категорией, которая использует товары из фикстуры выше."""
    return Category("Смартфоны", "Описание смартфонов", sample_products)
