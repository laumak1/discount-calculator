This program calculates shipments discount and price based on input data.

# Running the Discount Calculator
This program can be executed in two ways: using Docker or locally.

## Using Docker:
### 1. Build Docker image:
docker build -t discount-calculator .
### 2. Run the calculator:
docker run --rm discount-calculator
### 3. (Optional) Run calculator tests
docker run --rm discount-calculator python -m unittest test_calculator

## Locally:
### 1. Run calculator:
python discount_calculator.py
### 2. (Optional) Run calculator tests
python -m unittest test_calculator

# About program
The program is developed with a focus on writing clean and maintainable code, following the PEP8 standard for Python code formatting. It utilizes the Strategy design pattern to implement discount rules, ensuring separation of concerns and easy addition or removal of rules. This architectural choice is demonstrated in the program's tests, where different rules can be isolated or combined easily.

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
