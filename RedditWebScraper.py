import praw
import csv

# Initialize the Reddit API client with your credentials
reddit = praw.Reddit(client_id='KICIFYgxs-erb7yziA8BCQ',
                     client_secret='AfDR8EPehsK8YCyj5pshTLhm23cjeQ',
                     user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
                     username='TransitionFar6363',
                     password='Divyanshu@123')

# Define the subreddits to scrape
subreddits = ['wallstreetbets','stocks' ]

# Define the fields to extract from each post
fields = ['subreddit', 'id', 'title', 'body', 'author', 'score', 'created_utc']

# Create a CSV writer to write the data to a file
with open('reddit_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(fields)

    # Loop through each subreddit
    for subreddit_name in subreddits:
        sub = reddit.subreddit(subreddit_name)
        try:
            # Loop through the top 500 posts of the month in the subreddit
            for post in sub.top(time_filter='month',limit=500):
                # Write the post data to the CSV file
                writer.writerow([subreddit_name, post.id, post.title, post.selftext, post.author, post.score, post.created_utc])
        except:
            print("skipped_review")
print(reddit.user.me())
print(reddit.auth.limits)
