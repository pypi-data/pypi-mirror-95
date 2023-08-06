# Trading212 API
**Unofficial** API for Trading212 broker. 
### CFD are not suppoerted yet. Investing only.
### Support this project
<a href="https://www.buymeacoffee.com/hellambro" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" height="50" ></a>

### Disclaimer
#### Nor me or Trading212 are responsible for the use of this API, first make sure that everything works well through the use of a **DEMO** account, then switch to **REAL** mode.
### Prerequisites
chromedriver in your PATH,
##### Download the latest stable release of chromedriver from https://chromedriver.chromium.org/, extract and move it to /usr/local/bin

### Install
````
pip install pytrading212
````
### Usage

Refer here: [example.py](https://github.com/HellAmbro/Trading212API/blob/master/example.py)
````
from pytrading212.order import TimeValidity, StopLimitOrder, StopOrder, LimitOrder

from pytrading212 import Trading212, Mode, MarketOrder
from pytrading212.trading212 import Period

trading212 = Trading212('your_email', 'password', mode=Mode.DEMO)

market_order = trading212.execute_order(MarketOrder(instrument_code="AMZN_US_EQ", quantity=2))

limit_order = trading212.execute_order(
    LimitOrder(instrument_code="AMZN_US_EQ", quantity=2, limit_price=3000, time_validity=TimeValidity.DAY))

stop_order = trading212.execute_order(
    StopOrder(instrument_code="AMZN_US_EQ", quantity=2, stop_price=4000, time_validity=TimeValidity.GOOD_TILL_CANCEL))

stop_limit = trading212.execute_order(
    StopLimitOrder(instrument_code="AMZN_US_EQ", quantity=2, limit_price=3000, stop_price=4000,
                   time_validity=TimeValidity.GOOD_TILL_CANCEL))

sell_value_order = trading212.execute_value_order(ValueOrder('AMZN_US_EQ', value=-100))

sell_stop_limit = trading212.execute_order(
    StopLimitOrder(instrument_code="AMZN_US_EQ", quantity=2, limit_price=3000, stop_price=4000,
                   time_validity=TimeValidity.GOOD_TILL_CANCEL))

funds = trading212.get_funds()
orders = trading212.get_orders()

portfolio = trading212.get_portfolio_composition()
performance = trading212.get_portfolio_performance(Period.LAST_DAY)

# finish your session
trading.finish()
````

### Portfolio
````
portfolio = trading212.get_portfolio_composition()
````
````
[
  {
    'logo_url': 'https://trading212equities.s3.eu-central-1.amazonaws.com/BABA_US_EQ.png',
    'instrument_code': 'BABA_US_EQ',
    'value': '€9.28',
    'quantity': '0.0479677 shares',
    'total_return': '€0.28 (3.11%)'
  },
  {
    'logo_url': 'https://trading212equities.s3.eu-central-1.amazonaws.com/AMZN_US_EQ.png',
    'instrument_code': 'AMZN_US_EQ',
    'value': '€15,625.60',
    'quantity': '6.00353784 shares',
    'total_return': '€75.57 (0.49%)'
  },
]
````
### Performance
````
trading212.get_portfolio_performance(Period.LAST_DAY)
````
````
{
  'snapshots': [
    {
      'investment': 16438.3,
      'ppl': -159.81,
      'result': -17.92,
      'pieCash': 0.05,
      'time': '2021-01-13T11:00:00Z'
    },
    {
      'investment': 16438.3,
      'ppl': -158.06,
      'result': -17.92,
      'pieCash': 0.05,
      'time': '2021-01-13T11:15:00Z'
    },
    -- snip --
````
### How can I get instrument code?
Lookup in companies.json, key "ticker"

