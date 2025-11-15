"""
技术指标计算模块
计算常用的期货技术分析指标
"""

import pandas as pd
import numpy as np


class TechnicalIndicators:
    """技术指标计算器"""

    @staticmethod
    def calculate_ma(prices, period=5):
        """
        计算移动平均线 (Moving Average)

        Args:
            prices: 价格序列
            period: 周期

        Returns:
            pandas.Series: MA值
        """
        return prices.rolling(window=period).mean()

    @staticmethod
    def calculate_ema(prices, period=12):
        """
        计算指数移动平均线 (Exponential Moving Average)

        Args:
            prices: 价格序列
            period: 周期

        Returns:
            pandas.Series: EMA值
        """
        return prices.ewm(span=period, adjust=False).mean()

    @staticmethod
    def calculate_rsi(prices, period=14):
        """
        计算相对强弱指标 (Relative Strength Index)

        Args:
            prices: 价格序列
            period: 周期

        Returns:
            pandas.Series: RSI值 (0-100)
        """
        # 计算价格变动
        delta = prices.diff()

        # 分离上涨和下跌
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        # 计算RS和RSI
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    @staticmethod
    def calculate_macd(prices, fast=12, slow=26, signal=9):
        """
        计算MACD指标 (Moving Average Convergence Divergence)

        Args:
            prices: 价格序列
            fast: 快线周期
            slow: 慢线周期
            signal: 信号线周期

        Returns:
            dict: 包含MACD线、信号线、柱状图的字典
        """
        # 计算快速和慢速EMA
        ema_fast = prices.ewm(span=fast, adjust=False).mean()
        ema_slow = prices.ewm(span=slow, adjust=False).mean()

        # MACD线 = 快速EMA - 慢速EMA
        macd_line = ema_fast - ema_slow

        # 信号线 = MACD的EMA
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()

        # 柱状图 = MACD - 信号线
        histogram = macd_line - signal_line

        return {
            'MACD': macd_line,
            'Signal': signal_line,
            'Histogram': histogram
        }

    @staticmethod
    def calculate_bollinger_bands(prices, period=20, std_dev=2):
        """
        计算布林带 (Bollinger Bands)

        Args:
            prices: 价格序列
            period: 周期
            std_dev: 标准差倍数

        Returns:
            dict: 包含上轨、中轨、下轨的字典
        """
        # 中轨 = 移动平均线
        middle_band = prices.rolling(window=period).mean()

        # 标准差
        std = prices.rolling(window=period).std()

        # 上轨和下轨
        upper_band = middle_band + (std * std_dev)
        lower_band = middle_band - (std * std_dev)

        return {
            'Upper': upper_band,
            'Middle': middle_band,
            'Lower': lower_band
        }

    @staticmethod
    def calculate_kdj(high, low, close, period=9, k_period=3, d_period=3):
        """
        计算KDJ指标 (随机指标)

        Args:
            high: 最高价序列
            low: 最低价序列
            close: 收盘价序列
            period: RSV周期
            k_period: K值平滑周期
            d_period: D值平滑周期

        Returns:
            dict: 包含K、D、J值的字典
        """
        # 计算RSV (未成熟随机值)
        lowest_low = low.rolling(window=period).min()
        highest_high = high.rolling(window=period).max()

        rsv = ((close - lowest_low) / (highest_high - lowest_low)) * 100

        # 计算K值 (RSV的移动平均)
        k = rsv.ewm(com=k_period-1, adjust=False).mean()

        # 计算D值 (K值的移动平均)
        d = k.ewm(com=d_period-1, adjust=False).mean()

        # 计算J值
        j = 3 * k - 2 * d

        return {
            'K': k,
            'D': d,
            'J': j
        }

    @staticmethod
    def calculate_atr(high, low, close, period=14):
        """
        计算平均真实波幅 (Average True Range)

        Args:
            high: 最高价序列
            low: 最低价序列
            close: 收盘价序列
            period: 周期

        Returns:
            pandas.Series: ATR值
        """
        # 计算真实波幅
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())

        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

        # 计算ATR
        atr = tr.rolling(window=period).mean()

        return atr

    @staticmethod
    def calculate_obv(close, volume):
        """
        计算能量潮指标 (On Balance Volume)

        Args:
            close: 收盘价序列
            volume: 成交量序列

        Returns:
            pandas.Series: OBV值
        """
        obv = pd.Series(index=close.index, dtype=float)
        obv.iloc[0] = volume.iloc[0]

        for i in range(1, len(close)):
            if close.iloc[i] > close.iloc[i-1]:
                obv.iloc[i] = obv.iloc[i-1] + volume.iloc[i]
            elif close.iloc[i] < close.iloc[i-1]:
                obv.iloc[i] = obv.iloc[i-1] - volume.iloc[i]
            else:
                obv.iloc[i] = obv.iloc[i-1]

        return obv

    @staticmethod
    def analyze_trend(df):
        """
        综合趋势分析

        Args:
            df: 包含价格数据的DataFrame

        Returns:
            dict: 趋势分析结果
        """
        if '最新价' not in df.columns:
            return {'error': '数据格式错误，缺少最新价列'}

        prices = df['最新价']

        # 计算各种指标
        ma5 = TechnicalIndicators.calculate_ma(prices, 5)
        ma10 = TechnicalIndicators.calculate_ma(prices, 10)
        ma20 = TechnicalIndicators.calculate_ma(prices, 20)
        rsi = TechnicalIndicators.calculate_rsi(prices)
        macd_data = TechnicalIndicators.calculate_macd(prices)

        # 趋势判断
        trend = '中性'
        if len(ma5) > 0 and len(ma10) > 0:
            latest_ma5 = ma5.iloc[-1]
            latest_ma10 = ma10.iloc[-1]
            latest_price = prices.iloc[-1]

            if latest_ma5 > latest_ma10 and latest_price > latest_ma5:
                trend = '上涨'
            elif latest_ma5 < latest_ma10 and latest_price < latest_ma5:
                trend = '下跌'

        # RSI超买超卖判断
        rsi_signal = '中性'
        if len(rsi) > 0:
            latest_rsi = rsi.iloc[-1]
            if not np.isnan(latest_rsi):
                if latest_rsi > 70:
                    rsi_signal = '超买'
                elif latest_rsi < 30:
                    rsi_signal = '超卖'

        # MACD金叉死叉判断
        macd_signal = '中性'
        if len(macd_data['MACD']) > 1:
            current_macd = macd_data['MACD'].iloc[-1]
            current_signal = macd_data['Signal'].iloc[-1]
            prev_macd = macd_data['MACD'].iloc[-2]
            prev_signal = macd_data['Signal'].iloc[-2]

            if not (np.isnan(current_macd) or np.isnan(current_signal)):
                if prev_macd <= prev_signal and current_macd > current_signal:
                    macd_signal = '金叉(看涨)'
                elif prev_macd >= prev_signal and current_macd < current_signal:
                    macd_signal = '死叉(看跌)'

        return {
            '整体趋势': trend,
            'RSI信号': rsi_signal,
            'MACD信号': macd_signal,
            '最新价': prices.iloc[-1] if len(prices) > 0 else 0,
            'MA5': ma5.iloc[-1] if len(ma5) > 0 and not np.isnan(ma5.iloc[-1]) else None,
            'MA10': ma10.iloc[-1] if len(ma10) > 0 and not np.isnan(ma10.iloc[-1]) else None,
            'MA20': ma20.iloc[-1] if len(ma20) > 0 and not np.isnan(ma20.iloc[-1]) else None,
            'RSI': rsi.iloc[-1] if len(rsi) > 0 and not np.isnan(rsi.iloc[-1]) else None,
        }


# 测试代码
if __name__ == '__main__':
    # 创建测试数据
    test_data = {
        '最新价': [9570, 9495, 9446, 9400, 9485, 9450, 9480, 9520, 9550, 9570]
    }
    df = pd.DataFrame(test_data)

    print("技术指标计算示例")
    print("="*80)

    # 计算各种指标
    prices = df['最新价']

    print("\n1. 移动平均线 (MA5):")
    ma5 = TechnicalIndicators.calculate_ma(prices, 5)
    print(ma5)

    print("\n2. RSI指标:")
    rsi = TechnicalIndicators.calculate_rsi(prices)
    print(rsi)

    print("\n3. MACD指标:")
    macd = TechnicalIndicators.calculate_macd(prices)
    print(f"MACD: {macd['MACD'].iloc[-1]:.2f}")
    print(f"Signal: {macd['Signal'].iloc[-1]:.2f}")

    print("\n4. 综合趋势分析:")
    analysis = TechnicalIndicators.analyze_trend(df)
    for key, value in analysis.items():
        print(f"{key}: {value}")

    print("\n"+"="*80)
