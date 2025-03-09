from config import SHIPMENT_PRICES
from shipment import Shipment


class ShipmentCalculator:
    def __init__(self, discount_strategies=None):
        self.discount_strategies = discount_strategies or []

    def calculate_shipment_price_and_discount(self, shipment: Shipment) -> tuple[int, int] | tuple[None, None]:
        if shipment.size not in SHIPMENT_PRICES or shipment.provider not in SHIPMENT_PRICES[shipment.size]:
            return None, None

        price = SHIPMENT_PRICES[shipment.size][shipment.provider]
        discount = 0

        for strategy in self.discount_strategies:
            price, discount = strategy.apply_discount_rule(price, discount, shipment)
        return price, discount


def process_line(line: str, calculator: ShipmentCalculator):
    parts = line.strip().split()
    if len(parts) != 3:
        print(line.strip() + " Ignored")
        return

    date, size, provider = parts
    shipment = Shipment(size, provider, date)
    price, discount = calculator.calculate_shipment_price_and_discount(shipment)
    if price is None or discount is None:
        print(line.strip() + " Ignored")
        return

    discount_str = "-" if not discount else f"{discount / 100:.2f}"
    print(f"{date} {size} {provider} {price / 100:.2f} {discount_str}")
