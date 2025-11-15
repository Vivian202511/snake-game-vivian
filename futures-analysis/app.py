"""
期货数据分析Web应用
使用Flask创建交互式界面
"""

from flask import Flask, render_template, jsonify
import sys
import os

# 添加src目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_collector import FuturesDataCollector
from technical_indicators import TechnicalIndicators
import pandas as pd

app = Flask(__name__)
collector = FuturesDataCollector()


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/futures-data')
def get_futures_data():
    """获取期货数据API"""
    try:
        df = collector.fetch_apple_futures()

        # 转换为JSON格式
        data = df.to_dict('records')

        return jsonify({
            'success': True,
            'data': data,
            'update_time': df['更新时间'].iloc[0] if len(df) > 0 else ''
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/api/technical-analysis')
def get_technical_analysis():
    """获取技术分析API"""
    try:
        df = collector.fetch_apple_futures()

        # 进行技术分析
        analysis = TechnicalIndicators.analyze_trend(df)

        return jsonify({
            'success': True,
            'analysis': analysis
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/api/main-contract')
def get_main_contract():
    """获取主力合约详情"""
    try:
        df = collector.fetch_apple_futures()

        # 筛选主力合约
        main = df[df['合约代码'] == 'APM']

        if len(main) > 0:
            data = main.iloc[0].to_dict()
            return jsonify({
                'success': True,
                'data': data
            })
        else:
            return jsonify({
                'success': False,
                'error': '未找到主力合约'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


if __name__ == '__main__':
    print("="*80)
    print("期货数据分析系统启动中...")
    print("请在浏览器中访问: http://127.0.0.1:5000")
    print("="*80)
    app.run(debug=True, host='0.0.0.0', port=5000)
