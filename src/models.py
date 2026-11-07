import json
from typing import List


class Product:
    """Класс для описания товара в магазине."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        """Инициализация товара."""
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Класс для описания категории товаров."""

    # Атрибуты класса (общие для всех объектов)
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        """Инициализация категории."""
        self.name = name
        self.description = description
        self.products = products

        # Увеличиваем общий счетчик категорий
        Category.category_count += 1
        # Увеличиваем общий счетчик товаров на длину списка
        Category.product_count += len(products)


def load_categories_from_json(filepath: str) -> List[Category]:
    """Загружает категории и товары из JSON-файла."""
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

    categories = []
    for cat_data in data:
        products = []
        for prod_data in cat_data["products"]:
            product = Product(
                name=prod_data["name"],
                description=prod_data["description"],
                price=prod_data["price"],
                quantity=prod_data["quantity"],
            )
            products.append(product)

        category = Category(
            name=cat_data["name"],
            description=cat_data["description"],
            products=products,
        )
        categories.append(category)

    return categories
