from zipline.api import symbol, order_target, record

def initialize(context):
    context.i = 0
    context.asset = symbol('AAPL')


def handle_data(context, data):
    # Skip first 300 days to get full windows
    context.i += 1
    if context.i < 300:
        return

    # Compute averages
    sma = data.history(context.asset, 'price', bar_count=20, frequency="1d").mean()
    lma = data.history(context.asset, 'price', bar_count=50, frequency="1d").mean()

    current_price = data.current(context.asset, 'price')
    stop_price = (1 - 0.02)*current_price
    # Trading logic
    if sma > lma:
        order(context.asset, 100, style=StopOrder(stop_price))
    elif sma < lma:
        order_target(context.asset, 0)

    # Save values for later inspection
    record(
        AAPL=current_price,
        short_mavg=sma,
        long_mavg=lma
    )
