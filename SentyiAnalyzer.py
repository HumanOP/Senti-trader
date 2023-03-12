import praw
import re
import torch
import csv
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax

# Initialize the Reddit API client with your credentials
reddit = praw.Reddit(client_id='KICIFYgxs-erb7yziA8BCQ',
                     client_secret='AfDR8EPehsK8YCyj5pshTLhm23cjeQ',
                     user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
                     username='TransitionFar6363',
                     password='Divyanshu@123')

MODEL =f"cardiffnlp/twitter-xlm-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

def get_sentiment(text):
    encoded_text = tokenizer.encode_plus(
        text,
        max_length=128,
        padding='max_length',
        truncation=True,
        return_attention_mask=True,
        return_tensors='pt'
    )

    output = model(**encoded_text)[0]
    scores = torch.softmax(output, dim=1).detach().numpy()[0]
    sentiment_score = scores[2] - scores[0]  # positive score - negative score
    return sentiment_score

def filter_posts():
    posts = reddit.subreddit('wallstreetbets').new(limit=1000)
    filtered_posts = []
    with open('senti_data2.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        try:
            for post in posts:
                title = post.title.lower()
                writer.writerow([post.id, post.title, post.selftext, post.author, post.score, post.created_utc])
                sentiment_score = get_sentiment(title)

                for word in title.split():
                    if re.match("^[a-zA-Z0-9]", word[1:]):
                        continue
                    if word.startswith('$'):
                        print(word)
                        stock_symbol = word[1:]
                        filtered_posts.append((post, stock_symbol, sentiment_score))
                        writer.writerow([post.id, post.title, post.selftext, post.author, post.score, post.created_utc, stock_symbol, sentiment_score])
                        break
        except:
            print("skipped_review")

    return filtered_posts

def make_trade_decision(sentiment_score):
    if sentiment_score > 0.2:
        return 'Buy'
    elif sentiment_score < -0.2:
        return 'Sell'
    else:
        return 'Hold'

filtered_posts = filter_posts()

for post, stock_symbol, sentiment_score in filtered_posts:
    trade_decision = make_trade_decision(sentiment_score)
    print(f"{stock_symbol}: {trade_decision}")