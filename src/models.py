import json
from typing import Any, Dict, List


class Product:
    """Класс для описания товара в магазине."""

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ):
        self.name = name
        self.description = description
        self.__price = price  # Приватный атрибут
        self.quantity = quantity

    def __str__(self) -> str:
        """Возвращает строковое представление товара."""
        return (
            f"{self.name}, {self.price} руб. "
            f"Остаток: {self.quantity} шт."
        )

    def __add__(self, other: "Product") -> float:
        """Возвращает общую стоимость двух товаров на складе."""
        return (
            self.price * self.quantity
            + other.price * other.quantity
        )

    @property
    def price(self) -> float:
        """Геттер для получения цены."""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для установки цены с проверками."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        # Подтверждение при понижении цены
        if new_price < self.__price:
            confirm = input(
                "Вы уверены, что хотите понизить цену? (y/n): "
            )
            if confirm.lower() != "y":
                return

        self.__price = new_price

    @classmethod
    def new_product(
        cls,
        product_data: Dict[str, Any],
        existing_products: List["Product"] = None,
    ) -> "Product":
        """Класс-метод для создания товара из словаря."""

        # Проверка на дубликаты
        if existing_products:
            for prod in existing_products:
                if prod.name == product_data["name"]:
                    prod.quantity += product_data["quantity"]

                    if product_data["price"] > prod.price:
                        prod.price = product_data["price"]

                    return prod

        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )


class Category:
    """Класс для описания категории товаров."""

    category_count = 0
    product_count = 0

    def __init__(
        self, name: str, description: str, products: List[Product]
    ):
        self.name = name
        self.description = description
        self.__products = products  # Приватный атрибут

        Category.category_count += 1
        Category.product_count += len(products)

    def __str__(self) -> str:
        """Возвращает строковое представление категории."""
        total_quantity = 0

        for product in self.__products:
            total_quantity += product.quantity

        return (
            f"{self.name}, количество продуктов: "
            f"{total_quantity} шт."
        )

    def add_product(self, product: Product) -> None:
        """Добавляет продукт в категорию."""
        self.__products.append(product)
        Category.product_count += 1

    def get_products(self) -> List[Product]:
        """Возвращает копию списка товаров категории."""
        return self.__products.copy()

    @property
    def products(self) -> str:
        """Геттер, возвращающий строку со списком товаров."""
        result = ""

        for product in self.__products:
            result += f"{product}\n"

        return result


class CategoryIterator:
    """Итератор для перебора товаров категории."""

    def __init__(self, category: Category) -> None:
        """Получает список товаров и устанавливает начальную позицию."""
        self.products = category.get_products()
        self.index = 0

    def __iter__(self) -> "CategoryIterator":
        """Возвращает объект итератора."""
        return self

    def __next__(self) -> Product:
        """Возвращает следующий товар категории."""
        if self.index >= len(self.products):
            raise StopIteration

        product = self.products[self.index]
        self.index += 1

        return product


def load_categories_from_json(filepath: str) -> List[Category]:
    """Загружает категории и товары из JSON-файла."""
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

    categories = []

    for cat_data in data:
        products = []

        for prod_data in cat_data["products"]:
            product = Product.new_product(prod_data)
            products.append(product)

        category = Category(
            name=cat_data["name"],
            description=cat_data["description"],
            products=products,
        )

        categories.append(category)

    return categories
