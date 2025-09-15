
"""
SPX Bull Put Credit Spread Trading Bot
Based on RSI Strategy with 90% Win Rate

Strategy Rules:
1. Enter when RSI < 35 (after big sell-offs)
2. Sell at-the-money put (50 delta)
3. Buy put 10 points below
4. Use 14 days to expiry
5. Target 50% profit
6. No stop-loss

Platform: Interactive Brokers (recommended) or TD Ameritrade or Alpaca
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta, time
import time as time_module
import logging
from typing import Dict, List, Optional, Tuple
import asyncio

# Technical Analysis Libraries
import talib
import pandas_ta as ta

# Interactive Brokers imports (choose one platform)
try:
    from ib_insync import *
    PLATFORM = "IB"
except ImportError:
    PLATFORM = None

# TD Ameritrade imports (alternative)
try:
    import tda
    from tda import auth, client
    if PLATFORM is None:
        PLATFORM = "TDA"
except ImportError:
    pass

# Alpaca imports (alternative)
try:
    from alpaca.trading.client import TradingClient
    from alpaca.trading.requests import MarketOrderRequest, OptionLegRequest
    from alpaca.trading.enums import OrderSide, TimeInForce, OrderClass
    from alpaca.data.historical import StockHistoricalDataClient
    from alpaca.data.requests import StockBarsRequest
    from alpaca.data.timeframe import TimeFrame
    if PLATFORM is None:
        PLATFORM = "ALPACA"
except ImportError:
    pass

class SPXBullPutBot:
    def __init__(self, platform="IB", paper_trading=True):
        """
        Initialize the SPX Bull Put Credit Spread Trading Bot

        Args:
            platform: "IB", "TDA", or "ALPACA"
            paper_trading: Boolean, True for paper trading
        """
        self.platform = platform
        self.paper_trading = paper_trading
        self.positions = {}
        self.historical_data = pd.DataFrame()

        # Strategy Parameters
        self.rsi_threshold = 35
        self.rsi_period = 14
        self.days_to_expiry = 14
        self.target_delta = 0.5  # 50 delta for short put
        self.spread_width = 10   # 10 points wide
        self.profit_target = 0.5  # 50% profit target
        self.position_size = 1   # Number of contracts per trade

        # Risk Management
        self.max_positions = 5
        self.min_dte = 7  # Minimum days to expiry before closing

        # Logging setup
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Initialize connection based on platform
        self.client = None
        self._initialize_platform()

    def _initialize_platform(self):
        """Initialize connection to chosen trading platform"""
        if self.platform == "IB":
            self._initialize_ib()
        elif self.platform == "TDA":
            self._initialize_tda()
        elif self.platform == "ALPACA":
            self._initialize_alpaca()
        else:
            raise ValueError("Unsupported platform. Choose IB, TDA, or ALPACA")

    def _initialize_ib(self):
        """Initialize Interactive Brokers connection"""
        try:
            self.ib = IB()
            if self.paper_trading:
                self.ib.connect('127.0.0.1', 7497, clientId=1)  # Paper trading port
            else:
                self.ib.connect('127.0.0.1', 7496, clientId=1)  # Live trading port
            self.logger.info("Connected to Interactive Brokers")
        except Exception as e:
            self.logger.error(f"Failed to connect to IB: {e}")

    def _initialize_tda(self):
        """Initialize TD Ameritrade connection"""
        # You'll need to set up API keys and authentication
        # Instructions: https://tda-api.readthedocs.io/en/latest/auth.html
        self.logger.info("TD Ameritrade initialization - Please set up authentication")
        pass

    def _initialize_alpaca(self):
        """Initialize Alpaca connection"""
        # You'll need to set up API keys
        # Get from: https://alpaca.markets/
        try:
            if self.paper_trading:
                self.trading_client = TradingClient(
                    api_key="YOUR_PAPER_API_KEY",
                    secret_key="YOUR_PAPER_SECRET_KEY",
                    paper=True
                )
            else:
                self.trading_client = TradingClient(
                    api_key="YOUR_LIVE_API_KEY", 
                    secret_key="YOUR_LIVE_SECRET_KEY",
                    paper=False
                )
            self.logger.info("Connected to Alpaca")
        except Exception as e:
            self.logger.error(f"Failed to connect to Alpaca: {e}")

    def get_spx_data(self, days=100) -> pd.DataFrame:
        """Get historical SPX price data for RSI calculation"""
        if self.platform == "IB":
            return self._get_spx_data_ib(days)
        elif self.platform == "TDA":
            return self._get_spx_data_tda(days)
        elif self.platform == "ALPACA":
            return self._get_spx_data_alpaca(days)

    def _get_spx_data_ib(self, days) -> pd.DataFrame:
        """Get SPX data from Interactive Brokers"""
        try:
            spx = Index('SPX', 'CBOE', 'USD')
            self.ib.qualifyContracts(spx)

            bars = self.ib.reqHistoricalData(
                spx,
                endDateTime='',
                durationStr=f'{days} D',
                barSizeSetting='1 day',
                whatToShow='TRADES',
                useRTH=True,
                formatDate=1
            )

            df = util.df(bars)
            df.set_index('date', inplace=True)
            return df

        except Exception as e:
            self.logger.error(f"Error getting SPX data from IB: {e}")
            return pd.DataFrame()

    def _get_spx_data_tda(self, days) -> pd.DataFrame:
        """Get SPX data from TD Ameritrade"""
        # Implementation for TD Ameritrade
        self.logger.info("TDA SPX data retrieval - implement with your API keys")
        return pd.DataFrame()

    def _get_spx_data_alpaca(self, days) -> pd.DataFrame:
        """Get SPX data from Alpaca"""
        try:
            data_client = StockHistoricalDataClient(
                api_key="YOUR_DATA_API_KEY",
                secret_key="YOUR_DATA_SECRET_KEY"
            )

            request = StockBarsRequest(
                symbol_or_symbols=["SPY"],  # Use SPY as proxy for SPX
                timeframe=TimeFrame.Day,
                start=datetime.now() - timedelta(days=days)
            )

            bars = data_client.get_stock_bars(request)
            df = bars.df
            return df

        except Exception as e:
            self.logger.error(f"Error getting SPX data from Alpaca: {e}")
            return pd.DataFrame()

    def calculate_rsi(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate RSI indicator"""
        if 'close' not in data.columns:
            data = data.rename(columns={'Close': 'close'})

        # Calculate RSI using pandas_ta
        data['rsi'] = ta.rsi(data['close'], length=self.rsi_period)

        return data

    def should_enter_trade(self) -> bool:
        """Check if conditions are met to enter a new trade"""
        # Get latest SPX data
        data = self.get_spx_data(100)
        if data.empty:
            return False

        # Calculate RSI
        data = self.calculate_rsi(data)

        # Get latest RSI value
        current_rsi = data['rsi'].iloc[-1]

        self.logger.info(f"Current RSI: {current_rsi}")

        # Check entry conditions
        if current_rsi < self.rsi_threshold:
            # Additional checks
            if len(self.positions) < self.max_positions:
                return True
            else:
                self.logger.info("Maximum positions reached")
                return False

        return False

    def get_options_chain(self, symbol="SPX", expiry_days=14):
        """Get options chain for SPX"""
        if self.platform == "IB":
            return self._get_options_chain_ib(symbol, expiry_days)
        elif self.platform == "TDA":
            return self._get_options_chain_tda(symbol, expiry_days)
        elif self.platform == "ALPACA":
            return self._get_options_chain_alpaca(symbol, expiry_days)

    def _get_options_chain_ib(self, symbol, expiry_days):
        """Get options chain from Interactive Brokers"""
        try:
            # Create underlying contract
            if symbol == "SPX":
                underlying = Index('SPX', 'CBOE', 'USD')
            else:
                underlying = Stock(symbol, 'SMART', 'USD')

            self.ib.qualifyContracts(underlying)

            # Get current price
            ticker = self.ib.reqMktData(underlying, '', False, False)
            self.ib.sleep(2)  # Wait for price update
            current_price = ticker.last

            # Calculate target expiry date
            target_date = datetime.now() + timedelta(days=expiry_days)

            # Get option chain
            chains = self.ib.reqSecDefOptParams(
                underlying.symbol, '', underlying.secType, underlying.conId
            )

            if not chains:
                self.logger.error("No option chains found")
                return None

            chain = chains[0]

            # Find closest expiry to target date
            target_expiry = min(chain.expirations, 
                              key=lambda x: abs((datetime.strptime(x, '%Y%m%d') - target_date).days))

            # Get put options around current price
            put_strikes = [s for s in chain.strikes 
                          if current_price - 50 <= s <= current_price + 10]

            options = []
            for strike in put_strikes:
                opt = Option('SPX', target_expiry, strike, 'P', 'SMART')
                options.append(opt)

            # Qualify contracts and get market data
            self.ib.qualifyContracts(*options)

            option_data = []
            for opt in options:
                ticker = self.ib.reqMktData(opt, '', False, False)
                self.ib.sleep(1)

                option_data.append({
                    'contract': opt,
                    'strike': opt.strike,
                    'bid': ticker.bid,
                    'ask': ticker.ask,
                    'last': ticker.last,
                    'expiry': opt.lastTradeDateOrContractMonth
                })

            return option_data

        except Exception as e:
            self.logger.error(f"Error getting options chain from IB: {e}")
            return None

    def find_bull_put_spread(self, options_data, current_price):
        """Find suitable bull put spread based on strategy criteria"""
        if not options_data:
            return None, None

        # Find ATM put (closest to 50 delta / current price)
        short_put = None
        long_put = None

        # Find short put (sell) - closest to ATM
        atm_candidates = [opt for opt in options_data 
                         if abs(opt['strike'] - current_price) <= 20]

        if not atm_candidates:
            return None, None

        # Sort by proximity to current price
        atm_candidates.sort(key=lambda x: abs(x['strike'] - current_price))
        short_put = atm_candidates[0]

        # Find long put (buy) - 10 points below short put
        target_long_strike = short_put['strike'] - self.spread_width
        long_candidates = [opt for opt in options_data 
                          if abs(opt['strike'] - target_long_strike) <= 5]

        if long_candidates:
            long_candidates.sort(key=lambda x: abs(x['strike'] - target_long_strike))
            long_put = long_candidates[0]

        return short_put, long_put

    def calculate_spread_metrics(self, short_put, long_put):
        """Calculate spread risk, reward, and other metrics"""
        if not short_put or not long_put:
            return None

        # Credit received (premium collected)
        short_premium = (short_put['bid'] + short_put['ask']) / 2
        long_premium = (long_put['bid'] + long_put['ask']) / 2
        net_credit = short_premium - long_premium

        # Maximum risk
        strike_diff = short_put['strike'] - long_put['strike']
        max_risk = strike_diff - net_credit

        # Profit target
        profit_target_price = net_credit * (1 - self.profit_target)

        return {
            'net_credit': net_credit,
            'max_risk': max_risk,
            'profit_target': profit_target_price,
            'risk_reward_ratio': net_credit / max_risk if max_risk > 0 else 0,
            'strike_width': strike_diff
        }

    def place_bull_put_spread_order(self, short_put, long_put, quantity=1):
        """Place bull put spread order"""
        if self.platform == "IB":
            return self._place_order_ib(short_put, long_put, quantity)
        elif self.platform == "TDA":
            return self._place_order_tda(short_put, long_put, quantity)
        elif self.platform == "ALPACA":
            return self._place_order_alpaca(short_put, long_put, quantity)

    def _place_order_ib(self, short_put, long_put, quantity):
        """Place order using Interactive Brokers"""
        try:
            # Create combo order for spread
            combo = Contract()
            combo.symbol = 'SPX'
            combo.secType = 'BAG'
            combo.currency = 'USD'
            combo.exchange = 'SMART'

            # Create legs
            leg1 = ComboLeg()
            leg1.conId = short_put['contract'].conId
            leg1.ratio = 1
            leg1.action = 'SELL'
            leg1.exchange = 'SMART'

            leg2 = ComboLeg()
            leg2.conId = long_put['contract'].conId  
            leg2.ratio = 1
            leg2.action = 'BUY'
            leg2.exchange = 'SMART'

            combo.comboLegs = [leg1, leg2]

            # Create order
            order = Order()
            order.action = 'BUY'  # Buy the spread (net credit)
            order.orderType = 'LMT'
            order.totalQuantity = quantity

            # Calculate net credit for limit price
            metrics = self.calculate_spread_metrics(short_put, long_put)
            order.lmtPrice = metrics['net_credit'] * 0.95  # Slightly below mid-price

            # Place order
            trade = self.ib.placeOrder(combo, order)

            self.logger.info(f"Bull put spread order placed: {trade}")
            return trade

        except Exception as e:
            self.logger.error(f"Error placing order with IB: {e}")
            return None

    def _place_order_alpaca(self, short_put, long_put, quantity):
        """Place order using Alpaca"""
        # Implementation for Alpaca multi-leg orders
        self.logger.info("Alpaca order placement - implement with your API")
        return None

    def manage_positions(self):
        """Check and manage existing positions"""
        for position_id, position in self.positions.items():
            # Check if profit target is reached
            current_value = self.get_position_value(position)

            if current_value <= position['profit_target']:
                self.close_position(position_id)
                self.logger.info(f"Closing position {position_id} - profit target reached")

            # Check if close to expiration
            days_to_expiry = (position['expiry'] - datetime.now()).days
            if days_to_expiry <= self.min_dte:
                self.close_position(position_id)
                self.logger.info(f"Closing position {position_id} - approaching expiration")

    def run_strategy(self):
        """Main strategy execution loop"""
        self.logger.info("Starting SPX Bull Put Credit Spread Bot")

        while True:
            try:
                # Check market hours (9:30 AM - 4:00 PM ET)
                current_time = datetime.now().time()
                market_open = time(9, 30)
                market_close = time(16, 0)

                if market_open <= current_time <= market_close:
                    # Manage existing positions
                    self.manage_positions()

                    # Check for new entry signals
                    if self.should_enter_trade():
                        self.logger.info("Entry signal detected!")

                        # Get current SPX price
                        spx_data = self.get_spx_data(1)
                        if not spx_data.empty:
                            current_price = spx_data['close'].iloc[-1]

                            # Get options chain
                            options_data = self.get_options_chain()

                            if options_data:
                                # Find suitable spread
                                short_put, long_put = self.find_bull_put_spread(
                                    options_data, current_price
                                )

                                if short_put and long_put:
                                    # Calculate metrics
                                    metrics = self.calculate_spread_metrics(short_put, long_put)

                                    self.logger.info(f"Spread metrics: {metrics}")

                                    # Place order if metrics are acceptable
                                    if metrics['net_credit'] > 0 and metrics['max_risk'] < 1000:
                                        order = self.place_bull_put_spread_order(
                                            short_put, long_put, self.position_size
                                        )

                                        if order:
                                            # Store position for management
                                            position_id = f"SPX_BPS_{datetime.now().strftime('%Y%m%d_%H%M')}"
                                            self.positions[position_id] = {
                                                'short_put': short_put,
                                                'long_put': long_put,
                                                'order': order,
                                                'entry_time': datetime.now(),
                                                'profit_target': metrics['profit_target'],
                                                'expiry': datetime.strptime(short_put['expiry'], '%Y%m%d')
                                            }

                # Sleep for 1 minute before next check
                time_module.sleep(60)

            except KeyboardInterrupt:
                self.logger.info("Bot stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                time_module.sleep(60)

    def get_position_value(self, position):
        """Get current value of a position"""
        # Implementation to get current position value
        return 0

    def close_position(self, position_id):
        """Close a specific position"""
        # Implementation to close position
        if position_id in self.positions:
            del self.positions[position_id]


# Example usage and setup instructions
def main():
    """Main function to run the trading bot"""

    print("SPX Bull Put Credit Spread Trading Bot")
    print("=====================================")
    print()
    print("Setup Instructions:")
    print("1. Choose your trading platform (IB, TDA, or Alpaca)")
    print("2. Set up API credentials")
    print("3. Install required packages:")
    print("   pip install ib_insync pandas-ta talib pandas numpy")
    print("4. For paper trading, make sure your platform supports it")
    print()

    # Initialize bot (change platform as needed)
    platform = input("Choose platform (IB/TDA/ALPACA): ").upper()
    paper = input("Use paper trading? (y/n): ").lower() == 'y'

    try:
        bot = SPXBullPutBot(platform=platform, paper_trading=paper)

        # Run backtest first (optional)
        print("\nRunning strategy...")
        bot.run_strategy()

    except Exception as e:
        print(f"Error initializing bot: {e}")
        print("Please check your platform setup and API credentials")

if __name__ == "__main__":
    main()
