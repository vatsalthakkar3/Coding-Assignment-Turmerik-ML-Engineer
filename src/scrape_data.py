import os
from dotenv import load_dotenv
import praw
import sqlite3
import time
import argparse

load_dotenv()

# Reddit API credentials
client_id = os.getenv("REDDIT_CLIENT_ID", default="")
client_secret = os.getenv("REDDIT_SECRET_KEY", default="")
user_agent = os.getenv("USER_AGENT", default="")


# Initialize Reddit API
reddit = praw.Reddit(
    client_id=client_id, client_secret=client_secret, user_agent=user_agent
)


# Function to get subreddits related to a topic
def get_subreddits(topic, search_depth="shallow"):
    """
    The function `get_subreddits` retrieves subreddit names related to a given topic based on the
    specified search depth.
    
    :param topic: The `topic` parameter in the `get_subreddits` function represents the topic or keyword
    that you want to search for in Reddit subreddits. This function will return a list of subreddit
    names related to the specified topic
    :param search_depth: The `search_depth` parameter in the `get_subreddits` function determines how
    deeply the function should search for subreddits related to the given topic, defaults to shallow
    (optional)
    
    :return: The function `get_subreddits` returns a list of subreddit names related to the given topic
    based on the specified search depth ("shallow" or "deep").
    """
    subreddit_list = []
    if search_depth == "shallow":
        for submission in reddit.subreddits.search_by_name(topic, exact=False):
            subreddit_list.append(submission.display_name)
    elif search_depth == "deep":
        for submission in reddit.subreddits.search(topic):
            subreddit_list.append(submission.display_name)
    return subreddit_list


# Function to scrape posts and comments from a subreddit
    
def scrape_subreddit(subreddit_name, db_conn, limit=10, requests_per_second=1000):
    """
    The function `scrape_subreddit` scrapes posts and comments from a specified subreddit and stores
    them in a database while implementing rate limiting.
    
    :param subreddit_name: Subreddit name is the name of the subreddit you want to scrape posts and
    comments from. For example, if you want to scrape posts from the "python" subreddit, you would
    provide "python" as the subreddit_name parameter
    
    :param db_conn: The `db_conn` parameter in the `scrape_subreddit` function is the database
    connection object that allows the function to interact with the database where the scraped data will
    be stored. It is used to execute SQL queries to create tables and insert data into the tables
    
    :param limit: The `limit` parameter in the `scrape_subreddit` function specifies the maximum number
    of posts to scrape from the subreddit. It determines how many posts will be fetched and processed
    during each run of the scraping function, defaults to 10 (optional)
    
    :param requests_per_second: The `requests_per_second` parameter in the `scrape_subreddit` function
    represents the number of requests you want to make per second to the Reddit API. This parameter is
    used to control the rate at which you are sending requests to the API in order to avoid hitting any
    rate limits imposed by Reddit, defaults to 1000 (optional)
    """
    subreddit = reddit.subreddit(subreddit_name)

    # Create tables if they don't exist
    db_conn.execute(
        """CREATE TABLE IF NOT EXISTS posts
                (post_id TEXT PRIMARY KEY,
                title TEXT,
                author TEXT,
                content TEXT)"""
    )

    db_conn.execute(
        """CREATE TABLE IF NOT EXISTS comments
                (comment_id TEXT PRIMARY KEY,
                post_id TEXT,
                comment_author TEXT,
                comment_body TEXT,
                reply_to_comment_id TEXT,
                FOREIGN KEY (post_id) REFERENCES posts(post_id))"""
    )

    for post in subreddit.hot(limit=limit):
        post_data = (
            post.id,
            post.title,
            post.author.name if post.author else "Unknown",
            post.selftext,
        )
        db_conn.execute("INSERT OR IGNORE INTO posts VALUES (?, ?, ?, ?)", post_data)

        # Get comments and replies
        post.comments.replace_more(limit=None)
        for comment in post.comments.list():
            comment_data = (
                comment.id,
                post.id,
                comment.author.name if comment.author else "Unknown",
                comment.body,
                comment.parent_id.split("_")[-1],
            )
            db_conn.execute(
                "INSERT OR IGNORE INTO comments VALUES (?, ?, ?, ?, ?)", comment_data
            )

        db_conn.commit()
        # Calculate delay for rate limiting
        delay = 1 / requests_per_second
        time.sleep(delay)


# Main function
def main():
    """
    The main function scrapes Reddit data based on user-defined parameters and stores it in a SQLite
    database.
    """
    
    parser = argparse.ArgumentParser(description="Scrape Reddit data")
    parser.add_argument(
        "--topic", type=str, default="clinical trial", help="Topic to search for"
    )
    parser.add_argument(
        "--limit", type=int, default=2, help="Number of posts to scrape per subreddit"
    )
    parser.add_argument(
        "--depth",
        type=str,
        choices=["shallow", "deep"],
        default="shallow",
        help="Search depth for subreddits",
    )
    args = parser.parse_args()

    subreddits = get_subreddits(args.topic, args.depth)

    # Create SQLite database
    conn = sqlite3.connect("reddit_data.db")

    for subreddit in subreddits:
        print(f"Scraping subreddit: {subreddit}")
        scrape_subreddit(subreddit, conn, args.limit)

    conn.close()
    print("Data scraping and storage complete.")


if __name__ == "__main__":
    main()
