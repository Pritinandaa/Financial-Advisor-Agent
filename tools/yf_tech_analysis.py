import yfinance as yf
from crewai.tools import BaseTool
from scipy.signal import find_peaks
import pandas as pd

# Try to import pandas_ta (pandas-ta). If unavailable, fall back to the
# alternative `ta` package (bukosabino/ta), which supports newer Python.
try:
    import pandas_ta as pta
    _ta_backend = "pandas_ta"
except Exception:
    pta = None
    try:
        import ta as ta_alt
        _ta_backend = "ta"
    except Exception:
        ta_alt = None
        _ta_backend = None

class YFinanceTechnicalAnalysisTool(BaseTool):
    """
    A BaseTool implementation for performing advanced technical analysis on a given stock ticker using pandas-ta.
    """

    def __init__(self):
        super().__init__(
            name="yf_tech_analysis",
            description="Perform advanced technical analysis on a given stock ticker."
        )

    def _run(self, ticker: str, period: str = "1y") -> dict:
        """
        Perform the technical analysis.

        Args:
            ticker (str): The stock ticker symbol.
            period (str): The time period for analysis (e.g., "1y" for 1 year).

        Returns:
            dict: Advanced technical analysis results.
        """
        try:
            # Fetch historical data
            stock = yf.Ticker(ticker)
            history = stock.history(period=period)

            # Validate data size
            if history.empty or len(history) < 50:  # Ensure enough rows for rolling calculations
                return {"error": "Insufficient data for technical analysis. At least 50 data points are required."}

            # Calculate indicators using available TA backend
            if _ta_backend == "pandas_ta":
                history['SMA_50'] = pta.sma(history['Close'], length=50)
                history['SMA_200'] = pta.sma(history['Close'], length=200)
                history['RSI'] = pta.rsi(history['Close'], length=14)
                history['MACD'], history['MACD_SIGNAL'], history['MACD_HIST'] = pta.macd(
                    history['Close'], fast=12, slow=26, signal=9
                )
                history['ATR'] = pta.atr(history['High'], history['Low'], history['Close'], length=14)
            elif _ta_backend == "ta":
                history['SMA_50'] = history['Close'].rolling(window=50).mean()
                history['SMA_200'] = history['Close'].rolling(window=200).mean()
                history['RSI'] = ta_alt.momentum.RSIIndicator(history['Close'], window=14).rsi()
                macd = ta_alt.trend.MACD(history['Close'], window_slow=26, window_fast=12, window_sign=9)
                history['MACD'] = macd.macd()
                history['MACD_SIGNAL'] = macd.macd_signal()
                history['MACD_HIST'] = macd.macd_diff()
                history['ATR'] = ta_alt.volatility.AverageTrueRange(history['High'], history['Low'], history['Close'], window=14).average_true_range()
            else:
                return {"error": "Neither 'pandas_ta' nor 'ta' libraries are installed. Please install one: `pip install ta` (recommended) or `pip install pandas-ta`."}

            # Get the current values of indicators
            current_price = history['Close'].iloc[-1]
            sma_50_current = history['SMA_50'].iloc[-1] if not history['SMA_50'].isnull().all() else None
            sma_200_current = history['SMA_200'].iloc[-1] if not history['SMA_200'].isnull().all() else None
            rsi_current = history['RSI'].iloc[-1] if not history['RSI'].isnull().all() else None
            macd_current = history['MACD'].iloc[-1] if not history['MACD'].isnull().all() else None
            atr_current = history['ATR'].iloc[-1] if not history['ATR'].isnull().all() else None

            # Identify potential support and resistance levels
            close_prices = history['Close'].dropna().values
            peaks, _ = find_peaks(close_prices, distance=20)
            troughs, _ = find_peaks(-close_prices, distance=20)
            support_levels = close_prices[troughs][-3:] if len(troughs) >= 3 else close_prices[troughs]
            resistance_levels = close_prices[peaks][-3:] if len(peaks) >= 3 else close_prices[peaks]

            # Identify chart patterns
            patterns = self.identify_chart_patterns(history)

            return {
                "ticker": ticker,
                "current_price": current_price,
                "sma_50": sma_50_current,
                "sma_200": sma_200_current,
                "rsi": rsi_current,
                "macd": macd_current,
                "atr": atr_current,
                "support_levels": support_levels.tolist() if len(support_levels) > 0 else [],
                "resistance_levels": resistance_levels.tolist() if len(resistance_levels) > 0 else [],
                "identified_patterns": patterns,
            }
        except IndexError:
            return {"error": "Index error: Ensure sufficient data for technical analysis."}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}

    def identify_chart_patterns(self, history):
        """
        Identify chart patterns like Head and Shoulders, Double Top, and Double Bottom.

        Args:
            history (pd.DataFrame): The DataFrame containing stock data.

        Returns:
            list: A list of identified patterns.
        """
        patterns = []
        close = history['Close'].values

        if self.is_head_and_shoulders(close):
            patterns.append("Head and Shoulders")
        if self.is_double_top(close):
            patterns.append("Double Top")
        if self.is_double_bottom(close):
            patterns.append("Double Bottom")

        return patterns

    def is_head_and_shoulders(self, close):
        """
        Detect a Head and Shoulders pattern.

        Args:
            close (np.ndarray): The closing prices.

        Returns:
            bool: True if a Head and Shoulders pattern is detected, False otherwise.
        """
        peaks, _ = find_peaks(close, distance=20)
        if len(peaks) >= 3:
            left_shoulder, head, right_shoulder = peaks[-3], peaks[-2], peaks[-1]
            if close[head] > close[left_shoulder] and close[head] > close[right_shoulder]:
                return True
        return False

    def is_double_top(self, close):
        """
        Detect a Double Top pattern.

        Args:
            close (np.ndarray): The closing prices.

        Returns:
            bool: True if a Double Top pattern is detected, False otherwise.
        """
        peaks, _ = find_peaks(close, distance=20)
        if len(peaks) >= 2:
            if abs(close[peaks[-1]] - close[peaks[-2]]) / close[peaks[-2]] < 0.03:
                return True
        return False

    def is_double_bottom(self, close):
        """
        Detect a Double Bottom pattern.

        Args:
            close (np.ndarray): The closing prices.

        Returns:
            bool: True if a Double Bottom pattern is detected, False otherwise.
        """
        troughs, _ = find_peaks(-close, distance=20)
        if len(troughs) >= 2:
            if abs(close[troughs[-1]] - close[troughs[-2]]) / close[troughs[-2]] < 0.03:
                return True
        return False

if __name__ == "__main__":
    tool = YFinanceTechnicalAnalysisTool()
    result = tool.run(ticker="AAPL", period="1y")
    print(result)