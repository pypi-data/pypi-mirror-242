# suumo_scraping

[【SUUMO】不動産売買・住宅購入・賃貸情報ならリクルートの不動産ポータルサイト](https://suumo.jp/)のデータをスクレイピングにより取得します。

**Warning**

SUUMOの[ご利用規約](https://cdn.p.recruit.co.jp/terms/suu-t-1003/index.html)をよく読んでからご利用ください。不正の目的をもって利用する行為や商業目的で利用する行為(株式会社リクルートが認める場合を除く）は禁止されているので注意してください。

## 使い方

### インストール

```
pip install suumo_scraping
```

### データ取得

[【SUUMO】不動産売買・住宅購入・賃貸情報ならリクルートの不動産ポータルサイト](https://suumo.jp/)の賃貸物件でデータを取得したい条件で検索し、そのURLをcollect_rental_data関数に渡せば、物件情報を格納したデータをリストで取得できます。

例）
```
import suumo_scraping

url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=060&bs=040&ra=026&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&ek=242012011&rn=2420'
results = suumo_scraping.collect_rental_data(url)
```

データの加工やCSVへの出力などは、pandasを利用するのが便利です。

例）
```
import pandas as pd
import suumo_scraping

url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=060&bs=040&ra=026&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&ek=242012011&rn=2420'
results = suumo_scraping.collect_rental_data(url)

# 結果をpandasのデータフレームに変換し、CSVに出力
columns = results.pop(0)
df = pd.DataFrame(results, columns=columns)
df.to_csv('suumo_output.csv')
```


## 著者

浅野直樹

## ライセンス

GNU Affero General Public License v3.0