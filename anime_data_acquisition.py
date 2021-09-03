import csv
from os import readlink
import requests
import time
from bs4 import BeautifulSoup
from soupsieve import select
import itertools

# メールアドレスとパスワードの指定
EMAIL = "ja224kg@gmail.com"
PASS = "hogehoge"

# セッションを開始
session = requests.session()

# ログイン
login_info = {
    "data[User][email]":EMAIL,
    "data[User][original_password]":PASS,
    "data[_Token][fields]":"f205e9d7236d8c6e3af9bfbc05b1d475a0196848%3A",
}
time.sleep(2)

# action
url_login = "https://www.anikore.jp/users/login/"
res = session.post(url_login, data=login_info)
res.raise_for_status() # エラーならここで例外を発生させる
time.sleep(2)



# 空の配列作成
anime_as = []

#各アニメリンクが埋め込まれているaタグ取得しanime_as配列に追加、266ページ分繰り返す
page = 1
for a in range(266):
  url = ('https://www.anikore.jp/pop_ranking/page:{}'.format(page))
  r = session.get(url)
  soup = BeautifulSoup(r.text, 'lxml')
  anime_as.append(soup.select(".l-searchPageRanking_unit h2 a"))
  page += 1

# 空の配列作成
anime_hrefs = []
anime_urls = []

# 取得したaタグに埋め込まれているhref要素を取得しanime_hrefsに追加(二次元配列→一次元化)
for anime_a in list(itertools.chain.from_iterable(anime_as)):
  anime_hrefs.append(anime_a.get("href"))

# アニメ詳細ページURL作成のベースとなるURL
base_url = "https://www.anikore.jp/"

# 取得したhref内のURLを取得しanime_urlsに追加
for anime_href in anime_hrefs:
  anime_url1 = (base_url + anime_href)
  anime_urls.append([anime_url1])

# csvファイルを新規作成、anime_urlsに追加したURLをcsvファイルに書き込む
f = open("anikore_urls.csv", "w")
csvf = csv.writer(f)
for anime_url in anime_urls:
  csvf.writerow(anime_url)
f.close

# 評価項目をcsv_datas配列に追加
csv_datas = [['ランキング', 'タイトル', '総合得点(点)', '評価件数(件)', 'お気に入り人数(人)', '評価', '物語', '作画', '声優', '音楽', 'キャラ', 'ジャンル', '放送時期', '制作会社', '声優陣', '主題歌']]

# csvファイルを新規作成、csv_datas配列についかした評価項目をcsvファイルに書き込む
f = open("anime_data.csv", "w")
csvf = csv.writer(f)
csvf.writerow(anime_url)
f.close

# アニメ評価等のデータ取得、csvファイルに書き込む
# 何故か途中で落ちる
# 前回の続きから処理を行うためrank変数に前回処理が止まったところのアニメ順位を代入
rank = 746
f = open("anime_data.csv", "a")
with open('anikore_urls.csv') as csv_file:
  for word in csv_file:
    anime_page = session.get(word)
    soup = BeautifulSoup(anime_page.text, 'lxml')
    time.sleep(5)
    print(word)
    # 要素内にデータがあるか確認
    if soup.select_one("body"):
      # 要素内にデータがあるか確認しデータをtitleに代入
      # true アニメタイトル, false 空
      if soup.select_one(".l-animeDetailHeader .l-wrapper h1"): 
        title = soup.select_one(".l-animeDetailHeader .l-wrapper h1").text.strip().replace('「', '').replace('」', '')
      elif soup.select_one(".l-animeDetailHeader .l-wrapper h1") == None:
        time.sleep(10)
        title = soup.select_one(".l-animeDetailHeader .l-wrapper h1").text.strip().replace('「', '').replace('」', '')
      else:
        ""

      # 要素内にデータがあるか確認しデータをpointに代入
      # true 総合得点, false 空
      if soup.select_one(".l-animeDetailHeader_pointSummary_unit-point dd strong"): 
        point = soup.select_one(".l-animeDetailHeader_pointSummary_unit-point dd strong").text 
      elif soup.select_one(".l-animeDetailHeader_pointSummary_unit-point dd strong") == None:
        time.sleep(10)
        point = soup.select_one(".l-animeDetailHeader_pointSummary_unit-point dd strong").text 
      else:
        ""
      
      # 要素内にデータがあるか確認しデータをimpに代入
      # true 評価件数, false 空
      if soup.select_one(".l-animeDetailHeader_pointSummary_unit-review dd strong"): 
        imp = soup.select_one(".l-animeDetailHeader_pointSummary_unit-review dd strong").text 
      elif soup.select_one(".l-animeDetailHeader_pointSummary_unit-review dd strong") == None:
        time.sleep(10)
        imp = soup.select_one(".l-animeDetailHeader_pointSummary_unit-review dd strong").text 
      else:
        ""

      # 要素内にデータがあるか確認しデータをfavoriteに代入
      # true お気に入り数, false 空
      if soup.select_one(".l-animeDetailHeader_pointSummary_unit-shelf dd strong"): 
        favorite = soup.select_one(".l-animeDetailHeader_pointSummary_unit-shelf dd strong").text 
      elif soup.select_one(".l-animeDetailHeader_pointSummary_unit-shelf dd strong") == None:
        time.sleep(10)
        favorite = soup.select_one(".l-animeDetailHeader_pointSummary_unit-shelf dd strong").text 
      else:
        ""

      # 要素内にデータがあるか確認しデータをreview_scoreに代入
      # true 評価, false 空
      if soup.select_one(".l-animeDetailHeader_pointAndButtonBlock_starBlock strong"): 
        review_score = soup.select_one(".l-animeDetailHeader_pointAndButtonBlock_starBlock strong").text 
      elif soup.select_one(".l-animeDetailHeader_pointAndButtonBlock_starBlock strong") == None:
        time.sleep(10)
        review_score = soup.select_one(".l-animeDetailHeader_pointAndButtonBlock_starBlock strong").text 
      else:
        ""

      # 要素内にデータがあるか確認しデータをcvに代入
      # true 声優, false 空
      if soup.select_one(".l-animeDetailStaffInfo_box"): 
        cv = soup.select_one(".l-animeDetailStaffInfo_box p").text
      else:
        cv = ""

      # 要素内にデータがあるか確認しデータを代入
      # false 空
      if soup.select("dd"):
        # 評価
        scores = soup.select("dd")
        if len(scores) > 4:
          # 物語
          story_score = scores[4].text.strip()
          if len(scores) > 5:
            # 作画
            drawing_score = scores[5].text.strip()
            if len(scores) > 6:
              # 声優
              cv_score = scores[6].text.strip()
              if len(scores) > 7:
                # 音楽
                music_score = scores[7].text.strip()
                if len(scores) > 8:
                  # キャラクター
                  character_score = scores[8].text.strip()
                  if len(scores) > 9:
                    # ジャンル
                    genre = scores[9].text.strip()
                    if len(scores) > 10:
                      # 放送時期
                      date = scores[10].text.strip()
                      if len(scores) > 11:
                        # 制作会社
                        comp = scores[11].text.strip()
                      else:
                        comp = scores = ""
                    else:
                      ""
                  else:
                    ""
                else:
                  ""
              else:
                ""
            else:
              ""
          else:
            ""
        else:
          ""
      else:
        ""

      print(rank)
      # csvファイルを作成、代入した各種評価項目を入書き込み
      csvf = csv.writer(f)
      csvf.writerow([rank, title, point, imp, favorite, review_score, story_score, drawing_score, cv_score, music_score, character_score, genre, date, comp, cv])
      rank += 1





