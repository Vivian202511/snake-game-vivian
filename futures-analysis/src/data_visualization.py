"""
数据可视化模块
使用matplotlib和plotly创建各种图表
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.font_manager import FontProperties
import pandas as pd
import numpy as np
from datetime import datetime
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class DataVisualizer:
    """数据可视化工具类"""

    def __init__(self, output_dir='../output'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def plot_price_comparison(self, df, save=True):
        """
        绘制价格对比图

        Args:
            df: 期货数据DataFrame
            save: 是否保存图片
        """
        fig, ax = plt.subplots(figsize=(14, 8))

        # 提取主要合约
        main_contracts = df[df['合约代码'].str.contains('APM|AP6')]

        if len(main_contracts) == 0:
            print("没有找到主要合约数据")
            return

        # 绘制柱状图
        x = range(len(main_contracts))
        colors = ['#4CAF50' if val > 0 else '#f44336' for val in main_contracts['涨跌幅']]

        bars = ax.bar(x, main_contracts['最新价'], color=colors, alpha=0.7, edgecolor='black')

        # 在柱子上方显示涨跌幅
        for i, (idx, row) in enumerate(main_contracts.iterrows()):
            height = row['最新价']
            change = row['涨跌幅']
            label = f"{change:+.2f}%"
            ax.text(i, height, label, ha='center', va='bottom', fontsize=10, fontweight='bold')

        # 设置标签
        ax.set_xlabel('合约代码', fontsize=12, fontweight='bold')
        ax.set_ylabel('最新价 (元/吨)', fontsize=12, fontweight='bold')
        ax.set_title('苹果期货合约价格对比', fontsize=16, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(main_contracts['合约名称'], rotation=45, ha='right')

        # 添加网格
        ax.grid(True, alpha=0.3, linestyle='--')

        plt.tight_layout()

        if save:
            filepath = os.path.join(self.output_dir, 'price_comparison.png')
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"图表已保存: {filepath}")

        plt.show()
        return fig

    def plot_volume_analysis(self, df, save=True):
        """
        绘制成交量分析图

        Args:
            df: 期货数据DataFrame
            save: 是否保存图片
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

        main_contracts = df[df['合约代码'].str.contains('APM|AP6')].head(6)

        if len(main_contracts) == 0:
            print("没有找到主要合约数据")
            return

        # 图1: 成交量
        x = range(len(main_contracts))
        bars1 = ax1.bar(x, main_contracts['成交量'], color='#2196F3', alpha=0.7, edgecolor='black')

        ax1.set_xlabel('合约代码', fontsize=12, fontweight='bold')
        ax1.set_ylabel('成交量 (手)', fontsize=12, fontweight='bold')
        ax1.set_title('苹果期货成交量分析', fontsize=14, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(main_contracts['合约名称'], rotation=45, ha='right')
        ax1.grid(True, alpha=0.3, linestyle='--')

        # 添加数值标签
        for i, (idx, row) in enumerate(main_contracts.iterrows()):
            volume = row['成交量']
            label = f"{volume:,.0f}"
            ax1.text(i, volume, label, ha='center', va='bottom', fontsize=9)

        # 图2: 持仓量
        bars2 = ax2.bar(x, main_contracts['持仓量'], color='#FF9800', alpha=0.7, edgecolor='black')

        ax2.set_xlabel('合约代码', fontsize=12, fontweight='bold')
        ax2.set_ylabel('持仓量 (手)', fontsize=12, fontweight='bold')
        ax2.set_title('苹果期货持仓量分析', fontsize=14, fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels(main_contracts['合约名称'], rotation=45, ha='right')
        ax2.grid(True, alpha=0.3, linestyle='--')

        # 添加数值标签
        for i, (idx, row) in enumerate(main_contracts.iterrows()):
            oi = row['持仓量']
            label = f"{oi:,.0f}"
            ax2.text(i, oi, label, ha='center', va='bottom', fontsize=9)

        plt.tight_layout()

        if save:
            filepath = os.path.join(self.output_dir, 'volume_analysis.png')
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"图表已保存: {filepath}")

        plt.show()
        return fig

    def plot_price_range(self, df, save=True):
        """
        绘制价格区间图（最高、最低、最新价）

        Args:
            df: 期货数据DataFrame
            save: 是否保存图片
        """
        fig, ax = plt.subplots(figsize=(14, 8))

        main_contracts = df[df['合约代码'].str.contains('APM|AP6')].head(6)

        if len(main_contracts) == 0:
            print("没有找到主要合约数据")
            return

        x = range(len(main_contracts))
        width = 0.25

        # 绘制最高、最低、最新价
        bars1 = ax.bar([i - width for i in x], main_contracts['最高'], width,
                       label='最高价', color='#4CAF50', alpha=0.7)
        bars2 = ax.bar(x, main_contracts['最新价'], width,
                       label='最新价', color='#2196F3', alpha=0.7)
        bars3 = ax.bar([i + width for i in x], main_contracts['最低'], width,
                       label='最低价', color='#f44336', alpha=0.7)

        ax.set_xlabel('合约代码', fontsize=12, fontweight='bold')
        ax.set_ylabel('价格 (元/吨)', fontsize=12, fontweight='bold')
        ax.set_title('苹果期货价格区间分析', fontsize=16, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(main_contracts['合约名称'], rotation=45, ha='right')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3, linestyle='--')

        plt.tight_layout()

        if save:
            filepath = os.path.join(self.output_dir, 'price_range.png')
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"图表已保存: {filepath}")

        plt.show()
        return fig

    def plot_market_heatmap(self, df, save=True):
        """
        绘制市场热力图（涨跌幅）

        Args:
            df: 期货数据DataFrame
            save: 是否保存图片
        """
        fig, ax = plt.subplots(figsize=(12, 6))

        main_contracts = df.head(8)

        if len(main_contracts) == 0:
            print("没有找到数据")
            return

        # 创建颜色映射
        changes = main_contracts['涨跌幅'].values.reshape(1, -1)

        # 使用红绿配色
        im = ax.imshow(changes, cmap='RdYlGn', aspect='auto', vmin=-3, vmax=3)

        # 设置刻度
        ax.set_xticks(range(len(main_contracts)))
        ax.set_xticklabels(main_contracts['合约名称'], rotation=45, ha='right')
        ax.set_yticks([])

        # 添加颜色条
        cbar = plt.colorbar(im, ax=ax, orientation='horizontal', pad=0.1)
        cbar.set_label('涨跌幅 (%)', fontsize=11)

        # 在每个单元格中显示数值
        for i, (idx, row) in enumerate(main_contracts.iterrows()):
            text = ax.text(i, 0, f"{row['涨跌幅']:.2f}%\n{row['最新价']:.0f}",
                          ha="center", va="center", color="black", fontsize=10, fontweight='bold')

        ax.set_title('苹果期货市场涨跌热力图', fontsize=16, fontweight='bold', pad=20)

        plt.tight_layout()

        if save:
            filepath = os.path.join(self.output_dir, 'market_heatmap.png')
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"图表已保存: {filepath}")

        plt.show()
        return fig

    def plot_comprehensive_dashboard(self, df, save=True):
        """
        绘制综合仪表板

        Args:
            df: 期货数据DataFrame
            save: 是否保存图片
        """
        fig = plt.figure(figsize=(18, 12))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

        main_contracts = df[df['合约代码'].str.contains('APM|AP6')].head(6)

        if len(main_contracts) == 0:
            print("没有找到主要合约数据")
            return

        # 1. 价格对比
        ax1 = fig.add_subplot(gs[0, 0])
        x = range(len(main_contracts))
        colors = ['#4CAF50' if val > 0 else '#f44336' for val in main_contracts['涨跌幅']]
        ax1.bar(x, main_contracts['最新价'], color=colors, alpha=0.7)
        ax1.set_title('价格对比', fontsize=12, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(main_contracts['合约名称'], rotation=45, ha='right', fontsize=8)
        ax1.grid(True, alpha=0.3)

        # 2. 涨跌幅分布
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.barh(range(len(main_contracts)), main_contracts['涨跌幅'], color=colors, alpha=0.7)
        ax2.set_title('涨跌幅分布 (%)', fontsize=12, fontweight='bold')
        ax2.set_yticks(range(len(main_contracts)))
        ax2.set_yticklabels(main_contracts['合约名称'], fontsize=8)
        ax2.grid(True, alpha=0.3)

        # 3. 成交量
        ax3 = fig.add_subplot(gs[1, 0])
        ax3.bar(x, main_contracts['成交量'], color='#2196F3', alpha=0.7)
        ax3.set_title('成交量分析', fontsize=12, fontweight='bold')
        ax3.set_xticks(x)
        ax3.set_xticklabels(main_contracts['合约名称'], rotation=45, ha='right', fontsize=8)
        ax3.grid(True, alpha=0.3)

        # 4. 持仓量
        ax4 = fig.add_subplot(gs[1, 1])
        ax4.bar(x, main_contracts['持仓量'], color='#FF9800', alpha=0.7)
        ax4.set_title('持仓量分析', fontsize=12, fontweight='bold')
        ax4.set_xticks(x)
        ax4.set_xticklabels(main_contracts['合约名称'], rotation=45, ha='right', fontsize=8)
        ax4.grid(True, alpha=0.3)

        # 5. 价格区间
        ax5 = fig.add_subplot(gs[2, 0])
        ax5.plot(x, main_contracts['最高'], 'ro-', label='最高', linewidth=2, markersize=8)
        ax5.plot(x, main_contracts['最新价'], 'bo-', label='最新', linewidth=2, markersize=8)
        ax5.plot(x, main_contracts['最低'], 'go-', label='最低', linewidth=2, markersize=8)
        ax5.fill_between(x, main_contracts['最低'], main_contracts['最高'], alpha=0.2)
        ax5.set_title('价格区间', fontsize=12, fontweight='bold')
        ax5.set_xticks(x)
        ax5.set_xticklabels(main_contracts['合约名称'], rotation=45, ha='right', fontsize=8)
        ax5.legend()
        ax5.grid(True, alpha=0.3)

        # 6. 数据表格
        ax6 = fig.add_subplot(gs[2, 1])
        ax6.axis('off')

        # 创建表格数据
        table_data = []
        for idx, row in main_contracts.head(5).iterrows():
            table_data.append([
                row['合约名称'],
                f"{row['最新价']:.0f}",
                f"{row['涨跌幅']:+.2f}%",
                f"{row['成交量']/10000:.1f}万"
            ])

        table = ax6.table(cellText=table_data,
                         colLabels=['合约', '价格', '涨跌幅', '成交量'],
                         cellLoc='center',
                         loc='center',
                         bbox=[0, 0, 1, 1])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)

        # 设置表格样式
        for i in range(len(table_data) + 1):
            for j in range(4):
                cell = table[(i, j)]
                if i == 0:
                    cell.set_facecolor('#4CAF50')
                    cell.set_text_props(weight='bold', color='white')
                else:
                    cell.set_facecolor('#f0f0f0' if i % 2 == 0 else 'white')

        fig.suptitle('苹果期货市场综合分析仪表板', fontsize=18, fontweight='bold', y=0.98)

        if save:
            filepath = os.path.join(self.output_dir, 'comprehensive_dashboard.png')
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"综合仪表板已保存: {filepath}")

        plt.show()
        return fig


# 测试代码
if __name__ == '__main__':
    # 导入数据采集模块
    import sys
    sys.path.append('../src')
    from data_collector import FuturesDataCollector

    # 获取数据
    collector = FuturesDataCollector()
    df = collector.fetch_apple_futures()

    # 创建可视化
    visualizer = DataVisualizer()

    print("正在生成图表...")
    print("\n1. 生成综合仪表板...")
    visualizer.plot_comprehensive_dashboard(df)

    print("\n2. 生成价格对比图...")
    visualizer.plot_price_comparison(df)

    print("\n3. 生成成交量分析图...")
    visualizer.plot_volume_analysis(df)

    print("\n所有图表生成完成！")
