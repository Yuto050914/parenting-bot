import os
import tweepy
from anthropic import Anthropic
from datetime import datetime

client_ai = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

API_KEY = os.environ.get("X_API_KEY")
API_SECRET = os.environ.get("X_API_SECRET")
ACCESS_TOKEN = os.environ.get("X_ACCESS_TOKEN")
ACCESS_SECRET = os.environ.get("X_ACCESS_SECRET")

HISTORY_FILE = "history.txt"
MAX_HISTORY = 20

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return lines[-MAX_HISTORY:]

def save_history(tweet_text):
    history = load_history()
    history.append(tweet_text)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        for line in history[-MAX_HISTORY:]:
            f.write(line + "\n")

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
history = load_history()

if history:
    history_text = "\n".join([f"・{h}" for h in history])
    history_prompt = f"""
過去に投稿した内容（これらと被らないようにしてください）：
{history_text}
"""
else:
    history_prompt = ""

response = client_ai.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=200,
    temperature=0.9,
    messages=[
        {
            "role": "user",
            "content": f"""
実行日時：{now}

あなたは「毎日育児」というXアカウントの投稿を作ります。

このアカウントの目的は、妊娠前〜3歳頃までの子育てで
「これで合っているのか？」と不安になる親に対して、
論文・研究知見・公的情報をベースに
"考える視点"や"安心材料"を提供することです。

重要な考え方：
・子育てに絶対的な正解は少ない
・状況によって答えは変わる
・複数の可能性があることを整理する
・不安を煽らない
・親を否定しない
・「こういう見方もある」という形で伝える

【テーマ選定】
以下のテーマから毎回異なるものを1つ選んでください。
連続して同じテーマにならないよう、実行日時をもとにランダムに選ぶこと。

テーマリスト：
- 夜泣き・睡眠
- 離乳食・食事
- 言葉の発達・発語
- 人見知り・後追い
- イヤイヤ期
- スマホ・テレビとの付き合い方
- 妊娠中の過ごし方
- 抱っこ・スキンシップ
- 保育園・幼稚園への不安
- きょうだい育児
- 予防接種・健診
- 寝かしつけ
{history_prompt}
投稿ルール：
・選んだテーマに基づいて投稿する
・研究知見や公的情報をベースにする
・断定しすぎない
・140文字以内
・箇条書き禁止
・1投稿だけ出力
・人が呟いている自然な文章
・最後に必ず #毎日育児 をつける
・絵文字は1つまで

文章の型：
①よくある悩みや状況（読んだ人が「わかる…」と感じるリアルな言葉で）
②考えられる理由や視点
③少し安心できる締め（「知っておいて損はない」「意外と見落とされがち」など、思わず保存したくなる言葉で締める）

拡散のヒント（自然に組み込むこと）：
・「あるある」と感じさせる具体的な場面描写を冒頭に入れる
・難しい言葉を使わず、疲れているママ・パパでもスッと読める文体
・読み終わったあと「保存しておこう」と思わせる情報密度

投稿本文のみ出力してください。
"""
        }
    ]
)

tweet_text = response.content[0].text.strip()
tweet_text = tweet_text[:140]

client_x = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

client_x.create_tweet(text=tweet_text)
save_history(tweet_text)

print("投稿成功")
print(tweet_text)
