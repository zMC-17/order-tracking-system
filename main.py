def create_order(client_name: str, product_name: str) -> str:
    """Создаёт описание нового заказа."""
    return f'Клиент {client_name} заказал товар: {product_name}.'


def calculate_order_price(price: float, quantity: int) -> float:
    """Рассчитывает общую стоимость заказа."""
    return price * quantity


def get_order_status(is_ready: bool) -> str:
    """Возвращает текущий статус заказа."""
    if is_ready:
        return 'Заказ готов к выдаче'
    return 'Заказ находится в обработке'


client_name = 'Иван'
product_name = 'Клавиатура'
product_price = 3500
product_quantity = 2
is_order_ready = False

order = create_order(client_name, product_name)
total_price = calculate_order_price(
    product_price,
    product_quantity
)
status = get_order_status(is_order_ready)

print(order)
print(f'Количество товара: {product_quantity}')
print(f'Стоимость заказа: {total_price} руб.')
print(f'Статус: {status}')