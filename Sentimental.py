import praw
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
    label = scores.argmax()
    sentiment = 'Positive' if label == 2 else 'Neutral' if label == 1 else 'Negative'

    return sentiment

def filter_posts():
    posts = reddit.subreddit('wallstreetbets').new(time_filter='month',limit=100)
    filtered_posts = []
    with open('senti_data2.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        try:
            for post in posts:
                title = post.title.lower()
                print (title)
                writer.writerow([post.id, post.title, post.selftext, post.author, post.score, post.created_utc])
                sentiment = get_sentiment(title)

#             if sentiment != 'Positive':
#                 continue

#             if 'analysis' in title or 'fundamentals' in title  or 'stock' in title:
                for word in title.split():
                     if word.startswith('$'):
                        print(word)
                        stock_symbol = word[1:]
                        filtered_posts.append((post, stock_symbol))
                        writer.writerow([post.id, post.title, post.selftext, post.author, post.score, post.created_utc])
                        break
        except:
            print("skipped_review")

    return filtered_posts

filtered_posts = filter_posts()
print("hello")
print (len(filtered_posts))

for post, stock_symbol in filtered_posts:
    print(post)
