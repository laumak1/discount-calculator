import unittest
from config import MONTHLY_DISCOUNT_LIMIT
from shipment import Shipment
from calculator import ShipmentCalculator
from discount_rules import (
    MonthlyDiscountLimit,
    SmallShipmentDiscount,
    ThirdLargeLPShipmentDiscount,
)


class TestShipmentCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = ShipmentCalculator()

        self.SHIPMENT_PRICES = {
            "S": {"LP": 150, "MR": 200},
            "M": {"LP": 490, "MR": 300},
            "L": {"LP": 690, "MR": 400},
        }

    def test_all_rules(self):
        self.calculator.discount_strategies = [
            SmallShipmentDiscount(),
            ThirdLargeLPShipmentDiscount(),
            MonthlyDiscountLimit(),
        ]
        test_cases = [
            ("2015-02-10", "S", "MR", 150, 50),
            ("2015-02-10", "S", "MR", 150, 50),
            ("2015-02-11", "L", "LP", 690, 0),
            ("2015-02-11", "L", "LP", 690, 0),
            ("2015-02-11", "L", "LP", 0, 690),
            ("2015-02-12", "M", "MR", 300, 0),
            ("2015-02-13", "M", "LP", 490, 0),
            ("2015-02-15", "S", "MR", 150, 50),
            ("2015-02-17", "L", "LP", 690, 0),
            ("2015-02-17", "S", "MR", 150, 50),
        ]
        for date, size, provider, expected_price, expected_discount in test_cases:
            price, discount = self.calculator.calculate_shipment_price_and_discount(Shipment(size, provider, date))
            self.assertEqual(price, int(expected_price))
            self.assertEqual(discount, expected_discount)

    def test_calculate_shipment_price_and_discount_valid_data(self):
        self.calculator.discount_strategies = [
            SmallShipmentDiscount(),
            ThirdLargeLPShipmentDiscount(),
            MonthlyDiscountLimit(),
        ]
        shipment = Shipment("S", "LP", "2024-03-17")
        price, discount = self.calculator.calculate_shipment_price_and_discount(shipment)
        self.assertIsNotNone(price)
        self.assertIsNotNone(discount)

    def test_calculate_shipment_price_and_discount_invalid_data(self):
        self.calculator.discount_strategies = [
            SmallShipmentDiscount(),
            ThirdLargeLPShipmentDiscount(),
            MonthlyDiscountLimit(),
        ]
        invalid_shipment = Shipment("XL", "UPS", "2024-03-17")
        price, discount = self.calculator.calculate_shipment_price_and_discount(invalid_shipment)
        self.assertIsNone(price)
        self.assertIsNone(discount)

    def test_small_shipment_discount(self):
        self.calculator.discount_strategies = [SmallShipmentDiscount()]
        shipment = Shipment("S", "LP", "2024-03-01")
        price, discount = self.calculator.calculate_shipment_price_and_discount(shipment)
        self.assertEqual(price, self.SHIPMENT_PRICES["S"]["LP"])
        self.assertEqual(discount, 0)

        shipment = Shipment("S", "MR", "2024-03-01")
        price, discount = self.calculator.calculate_shipment_price_and_discount(shipment)
        self.assertEqual(price, self.SHIPMENT_PRICES["S"]["MR"] - discount)
        self.assertEqual(discount, 50)

    def test_third_large_lp_shipment_discount(self):
        self.calculator.discount_strategies = [
            ThirdLargeLPShipmentDiscount(),
            MonthlyDiscountLimit(),
        ]
        for _ in range(2):
            shipment = Shipment("L", "LP", "2024-03-01")
            price, discount = self.calculator.calculate_shipment_price_and_discount(shipment)
            self.assertEqual(price, self.SHIPMENT_PRICES["L"]["LP"])
            self.assertEqual(discount, 0)

        # After 3 large LP shipments, the discount should not be applied
        shipment = Shipment("L", "LP", "2024-03-01")
        price, discount = self.calculator.calculate_shipment_price_and_discount(shipment)
        self.assertEqual(price, 0)
        self.assertEqual(discount, self.SHIPMENT_PRICES["L"]["LP"])

    def test_monthly_discount_limit(self):
        self.calculator.discount_strategies = [
            SmallShipmentDiscount(),
            MonthlyDiscountLimit(),
        ]
        # Add up shipments to reach the discount limit
        total_discount = 0
        for _ in range(20):
            shipment = Shipment("S", "MR", "2024-03-01")
            price, discount = self.calculator.calculate_shipment_price_and_discount(shipment)
            total_discount += discount
        self.assertEqual(total_discount, MONTHLY_DISCOUNT_LIMIT)

        # Beyond the discount limit, no more discounts should be applied
        shipment = Shipment("S", "MR", "2024-03-01")
        price, discount = self.calculator.calculate_shipment_price_and_discount(shipment)
        self.assertEqual(price, self.SHIPMENT_PRICES["S"]["MR"])
        self.assertEqual(discount, 0)


if __name__ == "__main__":
    unittest.main()
