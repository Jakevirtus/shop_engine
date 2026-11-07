from src.models import Category, Product


def test_product_initialization():
    """Тест корректности инициализации Product."""
    product = Product("Samsung", "256GB", 180000.0, 5)

    # Проверяем, что все атрибуты сохранились правильно
    assert product.name == "Samsung"
    assert product.description == "256GB"
    assert product.price == 180000.0
    assert product.quantity == 5


def test_category_initialization(sample_category):
    """Тест корректности инициализации Category (использует фикстуру)."""
    assert sample_category.name == "Смартфоны"
    assert sample_category.description == "Описание смартфонов"
    # Проверяем, что в категорию попали 2 товара из фикстуры
    assert len(sample_category.products) == 2


def test_category_counters():
    """Тест подсчета категорий и товаров."""
    # Сбрасываем счетчики в ноль перед тестом, чтобы они не зависели от других тестов
    Category.category_count = 0
    Category.product_count = 0

    # Создаем первую категорию без товаров
    Category("Телевизоры", "Описание", [])
    assert Category.category_count == 1
    assert Category.product_count == 0

    # Создаем вторую категорию с одним товаром
    prod = Product("LG", "4K", 100000.0, 3)
    Category("Ноутбуки", "Описание", [prod])

    # Проверяем, что счетчики увеличились
    assert Category.category_count == 2
    assert Category.product_count == 1
