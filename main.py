from calculator import ShipmentCalculator, process_line
from discount_rules import SmallShipmentDiscount, ThirdLargeLPShipmentDiscount, MonthlyDiscountLimit


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
    discount_calculator = ShipmentCalculator(
        discount_strategies=[
            SmallShipmentDiscount(),
            ThirdLargeLPShipmentDiscount(),
            MonthlyDiscountLimit(),
        ]
    )
    start_program("input.txt", discount_calculator)
