from abc import ABC, abstractmethod
from datetime import datetime


class Shipment:
    def __init__(self, size, provider, date):
        self.size = size
        self.provider = provider
        self.date = date


# Abstract class for rules to inherit.
class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount_rule(self, price: int, discount: int, shipment: Shipment) -> tuple[int, int]:
        pass


class SmallShipmentDiscount(DiscountStrategy):
    def apply_discount_rule(self, price: int, discount: int, shipment: Shipment) -> tuple[int, int]:
        if shipment.size == "S":
            discount = price - min(ShipmentCalculator.SHIPMENT_PRICES["S"].values())
            price -= discount
        return price, discount


class ThirdLargeLPShipmentDiscount(DiscountStrategy):
    LP_LARGE_SHIPMENTS_THRESHOLD = 3

    def __init__(self):
        self.lp_large_shipments_monthly_count = 0

    def apply_discount_rule(self, price: int, discount: int, shipment: Shipment) -> tuple[int, int]:
        if shipment.size == "L" and shipment.provider == "LP":
            self.lp_large_shipments_monthly_count += 1
            if self.lp_large_shipments_monthly_count == self.LP_LARGE_SHIPMENTS_THRESHOLD:
                return 0, price
        return price, discount

    def reset_large_shipment_counter(self):
        self.lp_large_shipments_monthly_count = 0


class MonthlyDiscountLimit(DiscountStrategy):
    MONTHLY_DISCOUNT_LIMIT = 1000

    def __init__(self):
        self.accumulated_monthly_discount = 0

    def apply_discount_rule(self, price: int, discount: int, shipment: Shipment) -> tuple[int, int]:
        if self.accumulated_monthly_discount < self.MONTHLY_DISCOUNT_LIMIT:
            discount_up_to_limit = min(discount, self.MONTHLY_DISCOUNT_LIMIT - self.accumulated_monthly_discount)
            self.accumulated_monthly_discount += discount_up_to_limit
            price += discount - discount_up_to_limit
            return price, discount_up_to_limit
        price += discount
        return price, 0

    def reset_monthly_counters(self):
        self.accumulated_monthly_discount = 0


class ShipmentCalculator:
    SHIPMENT_PRICES = {
        "S": {"LP": 150, "MR": 200},
        "M": {"LP": 490, "MR": 300},
        "L": {"LP": 690, "MR": 400},
    }

    def __init__(self):
        self.current_month = None
        self.discount_strategies = [
            SmallShipmentDiscount(),
            ThirdLargeLPShipmentDiscount(),
            MonthlyDiscountLimit(),
        ]  # Order of rules matters.

    def check_month(self, date: str) -> None:
        try:
            parsed_date = datetime.strptime(date, "%Y-%m-%d")
            if parsed_date.month != self.current_month:
                self.current_month = parsed_date.month
                for strategy in self.discount_strategies:
                    if isinstance(strategy, MonthlyDiscountLimit):
                        strategy.reset_monthly_counters()
                    elif isinstance(strategy, ThirdLargeLPShipmentDiscount):
                        strategy.reset_large_shipment_counter()
        except ValueError:
            print(f"Error: Incorrect date format for '{date}'. Ignoring the month check.")

    def calculate_shipment_price_and_discount(self, shipment: Shipment) -> tuple[int, int] | tuple[None, None]:
        if shipment.size not in self.SHIPMENT_PRICES or shipment.provider not in self.SHIPMENT_PRICES[shipment.size]:
            return None, None

        self.check_month(shipment.date)
        price = self.SHIPMENT_PRICES[shipment.size][shipment.provider]
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
    price, discount = calculator.calculate_shipment_price_and_discount(Shipment(size, provider, date))
    if price is None or discount is None:
        print(line.strip() + " Ignored")
        return

    discount_str = "-" if not discount else f"{discount / 100:.2f}"
    print(f"{date} {size} {provider} {price / 100:.2f} {discount_str}")


def start_program(input_file: str, calculator: ShipmentCalculator):
    try:
        with open(input_file, "r", encoding="utf-8") as f_in:
            for line in f_in:
                process_line(line, calculator)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as exception:
        print(f"Error: An unexpected error occurred: {exception}")


if __name__ == "__main__":
    discount_calculator = ShipmentCalculator()
    start_program("input.txt", discount_calculator)
