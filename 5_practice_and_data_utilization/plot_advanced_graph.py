import matplotlib

matplotlib.use('Agg') # 描画の Backend として Desktop 環境が不要な Agg を使う
import matplotlib.pyplot as plt

# plot()の第３引数に系列の Style を表す文字列を指定できる。
# 'b'は青色、'x'はバツ印の Marker, '-'は Maker を実線で繋ぐことを意味する。
# Keyword 引数 label で指定した系列の名前は、凡例で使用される。
plt.plot([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], 'bx-', label='Linear function')
# Style の'r'は赤色、'o'は丸印の Marker, '--'は点線を意味する。
plt.plot([1, 2, 3, 4, 5], [1, 4, 8, 16, 25], 'ro--', label='Quadratic function')

plt.xlabel('X Value') # xlabel()関数でＸ軸の Label を指定する。
plt.ylabel('Y Value') # ylabel()関数でＹ軸の Label を指定する。
plt.title('Sample of matplotlib') # title()関数で Graph の Title を指定する。

plt.legend(loc='best') # legend()関数で凡例を表示する。loc='best'は最適な位置に表示することを意味する。
plt.xlim(0, 6) # Ｘ軸の範囲を 0~6 とする。ylim()関数で同様にＹ軸の範囲を指定できる。
plt.savefig('advanced_graph.png', dpi=300) # Graph を画像 File に保存する。
