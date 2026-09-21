"""Операции с клиентами без файлового ввода-вывода."""

from utils import generate_id


def find_client(clients: list[dict], client_id: int) -> dict | None:
    """Находит клиента по ID."""
    for client in clients:
        if client['id'] == client_id:
            return client
    return None


def find_clients(clients: list[dict], query: str) -> list[dict]:
    """Ищет по подстроке имени без учета регистра."""
    result = []
    for client in clients:
        if query.strip().lower() in client['name'].lower():
            result.append(client)
    return result


def delete_client(
    clients: list[dict], client_id: int, orders: list[dict],
) -> None:
    """Удаляет клиента, только если у него нет заказов."""
    client = find_client(clients, client_id)
    if client is None:
        raise ValueError('Клиент с таким ID не найден.')
    for order in orders:
        if order['client_id'] == client_id:
            raise ValueError('Сначала удалите заказы этого клиента.')
    clients.remove(client)


def add_client(clients: list[dict], name: str, phone: str) -> dict:
    """Проверяет данные и добавляет нового клиента."""
    name = name.strip()
    phone = phone.strip()
    if not name or not phone:
        raise ValueError('Заполните имя и телефон.')
    client = {
        'id': generate_id(clients),
        'name': name,
        'phone': phone,
    }
    clients.append(client)
    return client
