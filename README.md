This program calculates shipments discount and price based on input data.

## 1. Running the Discount Calculator locally:
python main.py

## 2. (Optional) Run calculator tests
python -m unittest test_calculator


# About program
The program is developed with a focus on writing clean and maintainable code, following the PEP8 standard for Python code formatting. It utilizes the Strategy design pattern to implement discount rules, ensuring separation of concerns and easy addition or removal of rules. This architectural choice is demonstrated in the program's tests, where different rules can be isolated or combined easily.

# About modules
### main.py
This is the entry point of the application. The module is responsible for:
- Reading the input data (e.g., shipment information) from a file or other sources.
- Initializing the ShipmentCalculator and applying the discount rules.
- Displaying or outputting the final calculated prices and discounts for each shipment.

### calculator.py
This module contains the core logic of the discount calculation.

### discount_rules.py
This module contains all the discount rules implemented in the program. Each rule class extends the DiscountRule abstract class and implements its unique discount rule. The implementation follows the Strategy Design Pattern, which allows different discount strategies to be defined as separate classes. This pattern enables the ShipmentCalculator to dynamically choose and apply various discount strategies interchangeably, based on the requirements of the shipment.

The Strategy Design Pattern decouples the discount logic from the main code, allowing for flexibility in applying different discount rules without modifying the context (ShipmentCalculator). Each discount strategy class can implement its own logic for calculating the discount, making it easy to add or modify discount rules in the future.

### shipment.py
This module encapsulates the Shipment class, which represents a shipment's characteristics (size, provider, and date).

### config.py
Module is used for defining configuration settings that might be used across the application.

### test_calculator.py
This module contains unit tests for the discount calculator.


# Final Notes:
- Modularity: Each module is designed to handle specific responsibilities, ensuring the codebase is modular, easy to understand, and maintain.
- Extensibility: The use of the Strategy pattern allows for easy extension of the discount rules without modifying the existing codebase, adhering to the Open/Closed Principle.

# Task:
Each item, depending on its size gets an appropriate package size assigned to it:
S - Small, a popular option to ship jewelry
M - Medium - clothes and similar items
L - Large - mostly shoes
Shipping price depends on package size and a provider:

| Provider | Package Size | Price |
|---|---|---|
|LP| S| 1.50 €|
|LP| M |4.90 €|
|LP| L |6.90 €|
|MR| S |2 €|
|MR| M |3 €|
|MR| L |4 €|


First, you have to implement such rules:
- All S shipments should always match the lowest S package price among the providers.
- The third L shipment via LP should be free, but only once a calendar month.
- Accumulated discounts cannot exceed 10 € in a calendar month. If there are not enough funds to fully cover a discount this calendar month, it should be covered partially.

Your design should be flexible enough to allow adding new rules and modifying existing ones easily.

Member's transactions are listed in a file 'input.txt', each line containing: date (without hours, in ISO format), package size code, and carrier code, separated with whitespace:

2015-02-01 S MR\
2015-02-02 S MR\
2015-02-03 L LP

Your program should output transactions and append reduced shipment price and a shipment discount (or '-' if there is none). The program should append 'Ignored' word if the line format is wrong or carrier/sizes are unrecognized.

2015-02-01 S MR 1.50 0.50\
2015-02-02 S MR 1.50 0.50\
2015-02-03 L LP 6.90 -

# Requirements
- Using additional libraries is prohibited. That constraint is not applied for unit tests and build.
- There should be an easy way to start the solution and tests.
- A short documentation of design decisions and assumptions can be provided in the code itself.
- Make sure your input data is loaded from a file (default name 'input.txt' is assumed)
- Make sure your solution outputs data to the screen (STDOUT) in a format described below
- Your design should be flexible enough to allow adding new rules and modifying existing ones easily
