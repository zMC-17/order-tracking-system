"""Создание, поиск и обработка коллекции заказов."""

from collections.abc import Iterator

from clients import find_client
from utils import generate_id


def add_order(
    orders: list[dict], client_id: int, product_name: str,
    price: float, quantity: int, clients: list[dict],
) -> dict:
    """Создает заказ для существующего клиента после проверки данных."""
    if find_client(clients, client_id) is None:
        raise ValueError('Клиент с таким ID не найден.')
    product_name = product_name.strip()
    if not product_name:
        raise ValueError('Введите название товара.')
    if price <= 0 or quantity <= 0:
        raise ValueError('Цена и количество должны быть больше нуля.')
    order = {
        'id': generate_id(orders), 'client_id': client_id,
        'product_name': product_name,
        'price': price, 'quantity': quantity,
        'is_ready': False,
    }
    orders.append(order)
    return order


def find_order_by_id(orders: list[dict], order_id: int) -> dict | None:
    """Возвращает заказ по ID или None."""
    for order in orders:
        if order['id'] == order_id:
            return order
    return None


def delete_order(orders: list[dict], order_id: int) -> None:
    """Удаляет (отменяет) заказ по ID."""
    order = find_order_by_id(orders, order_id)
    if order is None:
        raise ValueError('Заказ с таким ID не найден.')
    orders.remove(order)


def change_order_status(
    orders: list[dict], order_id: int, is_ready: bool,
) -> None:
    """Устанавливает булев статус готовности заказа."""
    order = find_order_by_id(orders, order_id)
    if order is None:
        raise ValueError('Заказ с таким ID не найден.')
    order['is_ready'] = is_ready


def find_orders_by_client(orders: list[dict], client_id: int) -> list[dict]:
    """Находит все заказы клиента."""
    return [order for order in orders if order['client_id'] == client_id]


def find_orders(orders: list[dict], query: str) -> list[dict]:
    """Ищет заказы по подстроке названия товара без учета регистра."""
    result = []
    for order in orders:
        if query.strip().lower() in order['product_name'].lower():
            result.append(order)
    return result


def filter_orders_by_status(
    orders: list[dict], is_ready: bool,
) -> Iterator[dict]:
    """Генерирует заказы с выбранным статусом."""
    for order in orders:
        if order['is_ready'] == is_ready:
            yield order


def calculate_order_price(price: float, quantity: int) -> float:
    """Рассчитывает стоимость заказа (сценарий ПР1)."""
    return round(price * quantity, 2)


def get_order_status(is_ready: bool) -> str:
    """Возвращает текстовый статус (сценарий ПР1)."""
    if is_ready:
        return 'Заказ готов к выдаче'
    return 'Заказ находится в обработке'


def sort_orders(
    orders: list[dict], key: str = 'total', reverse: bool = False,
) -> list[dict]:
    """Сортирует копию списка по сумме, товару или ID."""
    if key == 'total':
        return sorted(orders, reverse=reverse, key=lambda order:
                      calculate_order_price(order['price'], order['quantity']))
    if key == 'product_name':
        return sorted(orders, reverse=reverse,
                      key=lambda order: order['product_name'].lower())
    if key == 'id':
        return sorted(orders, reverse=reverse, key=lambda order: order['id'])
    raise ValueError('Допустимые ключи: total, product_name, id.')


def get_order_statistics(orders: list[dict]) -> dict:
    """Возвращает количество, статусы, сумму и число клиентов с заказами."""
    ready = 0
    amount = 0
    client_ids = set()
    for order in orders:
        if order['is_ready']:
            ready += 1
        amount += calculate_order_price(order['price'], order['quantity'])
        client_ids.add(order['client_id'])
    return {
        'total': len(orders),
        'ready': ready,
        'processing': len(orders) - ready,
        'clients': len(client_ids),
        'amount': round(amount, 2),
    }
