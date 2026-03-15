import tweepy

API_KEY = "4HQZhWfddm8aEMHOQh9prS7jZ"
API_SECRET = "DsSHIeeVdHryC7xzQPxSKhwIoM9yuuZgFDiA9M7NWJoPVVSiFy"
ACCESS_TOKEN = "1927635897555865600-pw4ccYjDWL7QBGhrGeIl3LScT89FyV"
ACCESS_SECRET = "pL6EfQXXAhbHL5gI0SwWeTnhy4JqVZoV7m2P1FjDsnob3"

client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

client.create_tweet(text="AI自動投稿テストです")
print("投稿成功")
