from datetime import datetime
import pandas as pd
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from IPython.display import display


def main():
    df_exchange = pd.read_csv('exchange.csv', encoding='cp932', header=1, names=['date', 'USD', 'rate'], index_col=0,
                              parse_dates=True)
    df_jgbcm = pd.read_csv('jgbcm_all.csv', encoding='cp932', header=1, index_col=0, parse_dates=True,
                           date_parser=parse_japanese_date, na_values=['-'])
    df_jobs = pd.read_excel('effective_job_ratio.xlsx', skiprows=3, skipfooter=3, usecols='A,U:AF', index_col=0)
    df_jobs = df_jobs[1:]
    df_jobs.columns = [c.split('.')[0] for c in df_jobs.columns]
    s_jobs = df_jobs.stack()
    s_jobs.index = [parse_year_and_month(y, m) for y, m in s_jobs.index]

    min_date = datetime(1973, 1, 1)  # Ｘ軸の最小値
    max_date = datetime.now()  # Ｙ軸の最大値

    # １つ目の Subplot（為替 Data）
    plt.subplot(3, 1, 1)  # ３行１列の１番目の Subplot を作成。
    plt.plot(df_exchange.index, df_exchange['USD'], label='Dollar-yen')
    plt.xlim(min_date, max_date)  # Ｘ軸の範囲を設定。
    plt.ylim(50, 250)  # Ｙ軸の範囲を設定
    plt.legend(loc='best')  # 凡例を最適な位置に表示

    # ２つ目の Subplot（国債金利 Data）
    plt.subplot(3, 1, 2)  # ３行1列の2番目の Subplot を作成
    plt.plot(df_jgbcm.index, df_jgbcm['1年'], label='1-year rate')
    plt.plot(df_jgbcm.index, df_jgbcm['5年'], label='5-year rate')
    plt.plot(df_jgbcm.index, df_jgbcm['10年'], label='10-year rate')
    plt.xlim(min_date, max_date)  # Ｘ軸の範囲を設定
    plt.legend(loc='best')  # 凡例を最適な位置に表示

    # ３つ目の Subplot（有効求人倍率 Data）
    plt.subplot(3, 1, 3)  # ３行１列の３番目の Subplot
    plt.plot(s_jobs.index, s_jobs, label='Effective job openings-to-applicants ratio (seasonally adjusted)')
    plt.xlim(min_date, max_date)  # Ｘ軸の範囲を設定
    plt.ylim(0.0, 2.0)  # Ｙ軸の範囲を設定
    plt.axhline(y=1, color='gray')  # y1 の水平線を引く
    plt.legend(loc='best')

    plt.savefig('historical_data.png', dpi=300) # 画像を保存


def parse_japanese_date(s):
    base_years = {'S': 1925, 'H': 1988, 'R': 2018}  # 昭和以降の元号の０年に相当する年を定義しておく。
    era = s[0]  # 元号を表す Alphabet １文字を取得。
    year, month, day = s[1:].split('.')  # ２文字目以降を.（Period)で分割して年月日に分ける。
    year = base_years[era] + int(year)  # 元号の０年に相当する年と数値に変換した年を足して西暦の年を得る。
    return datetime(year, int(month), int(day))  # datetime object を作成する。


def parse_year_and_month(year, month):
    year = int(year[:-1])  # "年"を除去して数値に変換
    month = int(month[:-1])  # "月"を除去して数値に変換
    return datetime(year, month, 1)  # datetime object を作成する。


if __name__ == '__main__':
    main()
