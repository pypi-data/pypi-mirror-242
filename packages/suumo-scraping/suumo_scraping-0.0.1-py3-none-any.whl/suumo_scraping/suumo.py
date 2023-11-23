import re
import time
import requests
from bs4 import BeautifulSoup

def check_if_new_arrival(class_names):
    """
    新着かどうかを判定する
    """

    if 'cassetteitem_other-checkbox--newarrival' in class_names:
        return True
    else:
        return False

def collect_rental_data_on_the_page(base_url, page_num):
    """
    ベースURLとページ番号でURLを組み立てて、そのページの賃貸情報データを取得する

    Parameters
    ----------
    base_url : str
        データを取得するSUUMOのベースURL
    page_num : str
        ページ番号
    
    Returns
    -------
    property_item_data_on_the_page : list
        そのページの物件情報を格納したデータ
    """

    # そのページのデータを格納するリストの作成
    property_item_data_on_the_page = []

    # HTMLのパース開始
    html = requests.get(f'{base_url}&page={page_num}')
    soup = BeautifulSoup(html.content, 'html.parser')

    # 物件のリストを取得
    property_items = soup.select('.cassetteitem')

    # 各物件の処理
    for property_item in property_items:
        property_image_url = property_item.select_one('.cassetteitem_object-item img').get('rel') # 物件のタイトル画像
        property_type = property_item.select_one('.ui-pct').text # 「賃貸マンション」などの物件タイプ
        property_title = property_item.select_one('.cassetteitem_content-title').text # 物件名
        address = property_item.select_one('.cassetteitem_detail-col1').text # 住所
        access = property_item.select_one('.cassetteitem_detail-col2').text # アクセス
        years = property_item.select('.cassetteitem_detail-col3 > div')[0].text # 築年数
        stories = property_item.select('.cassetteitem_detail-col3 > div')[1].text # 階数

        # その他の情報（各部屋についての情報）が書かれた表を取得
        other_tables = property_item.select('.js-cassette_link')

        # 各部屋の処理
        for other_table in other_tables:
            tds = other_table.select('td')
            new_arrival = check_if_new_arrival(tds[0]['class']) # 新着
            images = tds[1].select_one('div')['data-imgs'] # 画像
            floor = tds[2].text.strip() # 階
            rent = tds[3].select('li')[0].text # 賃料
            management_fee = tds[3].select('li')[1].text # 管理費
            deposit = tds[4].select('li')[0].text # 敷金
            gratuity = tds[4].select('li')[1].text # 礼金
            arrangement = tds[5].select('li')[0].text # 間取り
            exclusive_area = tds[5].select('li')[1].text # 専有面積

            # こだわり条件
            special_conditions = []
            for special_condition_list in tds[6].select('li'):
                special_conditions.append(special_condition_list.text)

            detail_url = tds[8].select_one('a').get('href') # 詳細リンク

            # その部屋についてのデータ（物件に共通のデータを含む）を追加
            property_item_data_on_the_page.append([property_image_url,
                                    property_type,
                                    property_title,
                                    address,
                                    access,
                                    years,
                                    stories,
                                    new_arrival,
                                    images,
                                    floor,
                                    rent,
                                    management_fee,
                                    deposit,
                                    gratuity,
                                    arrangement,
                                    exclusive_area,
                                    special_conditions,
                                    detail_url])

    # そのページのデータを返す
    return property_item_data_on_the_page


def collect_rental_data(url):
    """
    賃貸情報データを取得して二次元配列の結果を返す

    Parameters
    ----------
    url : str
        データを取得するSUUMOのURL
    
    Returns
    -------
    property_item_data : list
        物件情報を格納したデータ
    """
    # 結果として返すデータを格納するリストの作成
    property_item_data = []

    # 引数として与えられたURLにページ番号クエリがある場合はそれを削除してベースURLを設定
    base_url = re.sub('&page=\d+', '', url)

    # 見出し列の準備
    columns = ["物件のタイトル画像",
            "物件タイプ",
            "物件名",
            "住所",
            "アクセス",
            "築年数",
            "階数",
            "新着",
            "画像",
            "階",
            "賃料",
            "管理費",
            "敷金",
            "礼金",
            "間取り",
            "専有面積",
            "こだわり条件",
            "詳細リンク"]

    # 結果として返すリストの1行目に見出し列を追加
    property_item_data.append(columns)

    # ベースURLのHTMLパース開始
    html = requests.get(base_url)
    soup = BeautifulSoup(html.content, 'html.parser')

    # 最終ページ番号の取得
    pagination = soup.select_one('ol.pagination-parts')
    last_page_num = pagination.select('li')[-1].text
    
    # 1ページから最終ページまでループ
    for page_num in range(1, int(last_page_num) + 1):
        # どのページを取得しているかを表示
        print(f'{page_num}/{last_page_num}ページを取得しています。')

        # サーバーに負荷をかけすぎないように2秒待機
        time.sleep(2)

        # そのページのデータを取得
        property_item_data_on_the_page = collect_rental_data_on_the_page(base_url, page_num)

        # そのページのデータを全体のデータと結合
        property_item_data.extend(property_item_data_on_the_page)


    # 終了通知 
    print('取得を終了しました。')

    # 全体の結果を返す
    return property_item_data


