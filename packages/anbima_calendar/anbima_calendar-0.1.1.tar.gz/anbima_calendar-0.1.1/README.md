Anbima Calendar 🏦 📆 
=======================
![anbima-calendar](https://github.com/rizidoro/anbima_calendar/assets/13101/4aead264-4ab0-410e-a232-200fec9e7afa)

## Introduction
**Anbima Calendar** is a Python library designed to simplify handling banking holidays specific to Brazil. **ANBIMA (Associação Brasileira das Entidades dos Mercados Financeiro e de Capitais)**, the Brazilian Financial and Capital Markets Association, plays a crucial role in the development of financial markets in Brazil. This library provides a robust set of tools for determining business days, calculating due dates, and identifying holidays based on the official holiday calendar published by ANBIMA.

The holiday data used in **Anbima Calendar** is sourced directly from ANBIMA's official website: https://www.anbima.com.br/feriados/feriados.asp. This ensures that the library stays up-to-date with the most accurate and relevant holiday information, making it an invaluable resource for financial applications, scheduling systems, and any software dealing with date calculations in the Brazilian context.

Whether you're developing a finance-related application, a scheduling tool, or simply need to be aware of Brazilian banking holidays, Anbima Calendar offers a straightforward and efficient solution to navigate through the complexities of holiday scheduling in Brazil's financial markets.


## Features
- Identify Business Days: Quickly determine if a specific date is a business day in Brazil.
- Calculate Due Dates: Accurately calculate due dates taking into account weekends and holidays.
- Discover Holidays: Retrieve information about specific Brazilian holidays.
- Add Business Days: Add a specified number of business days to a given date.

## Installation
Install Anbima Calendar using pip:

```bash
pip install anbima_calendar
```

## Quickstart
Here's a quick example to get you started with Anbima Calendar:

```python
from anbima_calendar import is_business_day, add_business_days, get_holiday

# Check if a date is a business day
print(is_business_day('2023-04-21'))  # False, as it's Tiradentes' Day

# Add business days to a date
new_date = add_business_days(5, '2023-04-18')
print(new_date)  # Returns the date after adding 5 business days

# Retrieve the holiday name
holiday = get_holiday('2023-04-21')
print(holiday)  # Tiradentes
```

### Checking Business Days:
Determine if a given date is a business day in Brazil.

```python
from anbima_calendar import is_business_day

print(is_business_day('2023-12-25'))  # False, Christmas Day is a holiday
```
### Adding Business Days:
Add business days to a date, automatically skipping weekends and holidays.

```python
from anbima_calendar import add_business_days

new_date = add_business_days(10, '2023-12-20')
print(new_date)  # Date 10 business days from December 20, 2023
```

### Identifying Holidays
Find out if a date is a holiday and get its name.

```python
from anbima_calendar import get_holiday

holiday_name = get_holiday('2023-05-01')
print(holiday_name)  # Dia do Trabalho (Labor Day)
```

## Contributing
Contributions to Anbima Calendar are welcome! Whether it's bug reports, feature requests, or code contributions, your input is highly valued. Please refer to our Please refer to our [contributing guidelines](CONTRIBUTING.md) for more information.

## License
Anbima Calendar is licensed under the MIT License. See the LICENSE file for more details.
