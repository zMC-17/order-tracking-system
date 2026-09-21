"""Пять простых проверок основных функций проекта."""

import pytest

from clients import add_client
from orders import add_order, calculate_order_price, find_orders
from storage import load_records, save_records


def test_add_client():
    clients = []
    add_client(clients, 'Иван', '1234567')
    assert clients == [{'id': 1, 'name': 'Иван', 'phone': '1234567'}]


def test_find_orders():
    orders = [{'product_name': 'Клавиатура'}, {'product_name': 'Мышь'}]
    assert find_orders(orders, 'КЛАВ') == [orders[0]]


def test_calculate_order_price():
    assert calculate_order_price(3500, 2) == 7000


def test_unknown_client():
    orders = []
    with pytest.raises(ValueError):
        add_order(orders, 99, 'Клавиатура', 3500, 2, [])
    assert orders == []


def test_save_and_load(tmp_path):
    filename = tmp_path / 'clients.json'
    clients = [{'id': 1, 'name': 'Иван', 'phone': '1234567'}]
    save_records(filename, clients)
    assert load_records(filename) == clients
