import os
import tweepy
from anthropic import Anthropic

client_ai = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

API_KEY = os.environ.get("X_API_KEY")
API_SECRET = os.environ.get("X_API_SECRET")
ACCESS_TOKEN = os.environ.get("X_ACCESS_TOKEN")
ACCESS_SECRET = os.environ.get("X_ACCESS_SECRET")

response = client_ai.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=200,
    messages=[
        {
            "role": "user",
     "content": """
あなたは「毎日育児」というXアカウントの投稿を作ります。

このアカウントの目的は、妊娠前〜3歳頃までの子育てで
「これで合っているのか？」と不安になる親に対して、
論文・研究知見・公的情報をベースに
“考える視点”や“安心材料”を提供することです。

重要な考え方：
・子育てに絶対的な正解は少ない
・状況によって答えは変わる
・複数の可能性があることを整理する
・不安を煽らない
・親を否定しない
・「こういう見方もある」という形で伝える

投稿ルール：
・テーマは妊娠前〜3歳までの子育て
・研究知見や公的情報をベースにする
・断定しすぎない
・140文字以内
・箇条書き禁止
・1投稿だけ出力
・人が呟いている自然な文章
・最後に必ず #毎日育児 をつける
・絵文字は1つまで

文章の型：
①よくある悩みや状況
②考えられる理由や視点
③少し安心できる締め

例：
「生後8ヶ月なのに夜中に何度も起きる…。
この時期は睡眠退行や分離不安が重なることも多いと言われています。
月齢だけで判断できないことも多いので、焦らなくて大丈夫という研究知見もあります🌙
#毎日育児」

投稿本文のみ出力してください。
"""
        }
    ]
)

tweet_text = response.content[0].text.strip()

client_x = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

client_x.create_tweet(text=tweet_text)

print("投稿成功")
print(tweet_text)