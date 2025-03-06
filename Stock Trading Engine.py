import threading
import time
import random


class Order:
    def __init__(self, order_type, ticker, quantity, price):
        self.order_type = order_type  # 'Buy' or 'Sell'
        self.ticker = ticker
        self.quantity = quantity
        self.price = price
        self.timestamp = time.time()


class OrderBook:
    def __init__(self):
        self.buy_orders = []  # List for buy orders
        self.sell_orders = []  # List for sell orders
        self.lock = threading.Lock()

    def add_order(self, order):
        with self.lock:
            if order.order_type == 'Buy':
                self.buy_orders.append(order)
                self.buy_orders.sort(key=lambda x: (-x.price, x.timestamp))  # Sort by highest price, earliest timestamp
            else:
                self.sell_orders.append(order)
                self.sell_orders.sort(key=lambda x: (x.price, x.timestamp))  # Sort by lowest price, earliest timestamp

    def match_orders(self):
        with self.lock:
            while self.buy_orders and self.sell_orders:
                buy_order = self.buy_orders[0]
                sell_order = self.sell_orders[0]

                if buy_order.price >= sell_order.price:  # Matching condition
                    executed_qty = min(buy_order.quantity, sell_order.quantity)
                    print(f"Matched {executed_qty} of {buy_order.ticker} at {sell_order.price}")

                    if buy_order.quantity > executed_qty:
                        buy_order.quantity -= executed_qty
                    else:
                        self.buy_orders.pop(0)

                    if sell_order.quantity > executed_qty:
                        sell_order.quantity -= executed_qty
                    else:
                        self.sell_orders.pop(0)
                else:
                    break  # No more matches possible


def simulate_orders(order_book, num_orders=100):
    tickers = [f"T{i}" for i in range(1024)]
    for _ in range(num_orders):
        order_type = random.choice(['Buy', 'Sell'])
        ticker = random.choice(tickers)
        quantity = random.randint(1, 100)
        price = round(random.uniform(10, 500), 2)
        order = Order(order_type, ticker, quantity, price)
        order_book.add_order(order)

        if random.random() < 0.5:  # Simulate market activity
            order_book.match_orders()


if __name__ == "__main__":
    order_book = OrderBook()
    simulate_orders(order_book, num_orders=200)
