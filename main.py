import praw
import os
import datetime

# pipenv will automatically load these from .env
username = os.environ.get('REDDIT_USERNAME')
password = os.environ.get('REDDIT_PASSWORD')
client_id = os.environ.get('API_CLIENT')
client_secret = os.environ.get('API_SECRET')

reddit = praw.Reddit(
    username=username,
    password=password,
    client_id=client_id,
    client_secret=client_secret,
    user_agent="darwin:net.blyt.weeklyqa:v1.0 (by /u/weekly_qa_bot)",
)

n_weekly = 0;
expiration_date= 0;
for submission in reddit.subreddit("linguistics").search(query='flair:Weekly feature', syntax='plain', sort='new', time_filter='month'):
    submission.comment_sort = "new" # have to set this before fetching
    submission.comment_limit = 13
    if "Q&A" in submission.title:
        n_weekly += 1
        if n_weekly == 1:
            # skip the first (current) Q&A, but save the creation date
            expiration_date = submission.created_utc
        else:
            submission.comments.replace_more(limit=0)
            # find all top level comments with no replies that were posted after a new Q&A thread
            i = 0
            for comment in submission.comments:
                if comment.created_utc < expiration_date:
                    break
                if len(comment.replies) == 0 and comment.author != None:
                    i += 1
                    if i == 1:
                        print(submission.title)
                    print(str(i) + " https://www.reddit.com" + comment.permalink)
                    print(comment.body)
                    comment.reply("Hello,\n\nYou posted in an old (previous week's) Q&A thread. If you want to post in the current week's Q&A thread, you can find that at the top of r/linguistics (make sure you sort by 'hot').")
                    print("---")
            expiration_date = submission.created_utc
print(datetime.datetime.now())
