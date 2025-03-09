from abc import ABC, abstractmethod
from config import LP_LARGE_SHIPMENTS_THRESHOLD, MONTHLY_DISCOUNT_LIMIT, SHIPMENT_PRICES
from shipment import Shipment


class DiscountRule(ABC):
    @abstractmethod
    def apply_discount_rule(self, price: int, discount: int, shipment: Shipment) -> tuple[int, int]:
        pass


class SmallShipmentDiscount(DiscountRule):
    def apply_discount_rule(self, price: int, discount: int, shipment: Shipment) -> tuple[int, int]:
        if shipment.size == "S":
            discount = price - min(SHIPMENT_PRICES["S"].values())
            price -= discount
        return price, discount


class ThirdLargeLPShipmentDiscount(DiscountRule):
    def __init__(self):
        self.lp_large_shipments_count = {}

    def apply_discount_rule(self, price: int, discount: int, shipment: Shipment) -> tuple[int, int]:
        if shipment.size == "L" and shipment.provider == "LP":
            year_month_key = shipment.date.strftime("%Y-%m")
            self.lp_large_shipments_count[year_month_key] = self.lp_large_shipments_count.get(year_month_key, 0) + 1
            if self.lp_large_shipments_count[year_month_key] == LP_LARGE_SHIPMENTS_THRESHOLD:
                return 0, price
        return price, discount


class MonthlyDiscountLimit(DiscountRule):
    def __init__(self):
        self.accumulated_monthly_discount = {}

    def apply_discount_rule(self, price: int, discount: int, shipment: Shipment) -> tuple[int, int]:
        year_month_key = shipment.date.strftime("%Y-%m")
        if self.accumulated_monthly_discount.get(year_month_key, 0) < MONTHLY_DISCOUNT_LIMIT:
            discount_up_to_limit = min(
                discount, MONTHLY_DISCOUNT_LIMIT - self.accumulated_monthly_discount.get(year_month_key, 0)
            )
            self.accumulated_monthly_discount[year_month_key] = (
                self.accumulated_monthly_discount.get(year_month_key, 0) + discount_up_to_limit
            )
            price += discount - discount_up_to_limit
            return price, discount_up_to_limit
        price += discount
        return price, 0
