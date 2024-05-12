import json
import os
import sqlite3
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="gpt-3.5-turbo-0125", temperature=0.7, api_key=os.getenv("OPENAI_API_KEY")
)

SYSTEM_PROMPT = """
Take a deep breath and think that you are a helpful model that sends a personalized messages based on the sentiment of the comment aimed at \ 
users who express interest in or could potentially benefit from participating in a clinical trial.\
I will provide you with the following things:
1. Subreddit Post Title
2. Subreddit post content
3. Commenter Name (author of the comment)
4. Comment Body or Content
5. Parameter Indicating weather comment to Post or reply to another Comment.\
    is_reply_to_post = True if you are replying to a post, False if you are replying to a comment.

5. If It will be comment to post then you will create a personalized message based on the sentiment of the comment \
of the Commenter to that post that encourages the author of the comment to consider participating in a clinical trial. 

6. If It will be comment to comment (reply to a comment) then you will create a personalized message based on the sentiment of the User comment, \
comment to which he or she has replied and the post to which the comment was made. that encourages the author of the comment to consider participating in a clinical trial. 
"""


def generate_message(comment, db_conn, is_reply_to_post):
    cursor = db_conn.cursor()
    cursor.execute(f"SELECT * FROM posts WHERE post_id = '{comment[1]}';")
    post = cursor.fetchall()[0]
    if is_reply_to_post:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    SYSTEM_PROMPT,
                ),
                (
                    "human",
                    """Generate the Customize Message for the author of the comment.
                        Subreddit Post Title: {post_title}
                        Subreddit Post Content: {post_content}
                        Commenter Name: {comment_author}
                        Comment Body: {comment_body}
                        Parameter Indicating weather comment to Post or reply to another Comment: {is_reply_to_post}
                 """,
                ),
            ]
        )

        chain = prompt | llm
        response = chain.invoke(
            {
                "post_title": post[1],
                "post_content": post[3],
                "comment_author": comment[2],
                "comment_body": comment[3],
                "is_reply_to_post": is_reply_to_post,
            }
        )
        return response.content
    else:
        cursor.execute(f"SELECT * FROM comments WHERE comment_id = '{comment[4]}';")
        parent_comment = cursor.fetchall()[0]
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    SYSTEM_PROMPT,
                ),
                (
                    "human",
                    """Generate the Customize Message for the author of the comment.
                        Subreddit Post Title: {post_title}
                        Subreddit Post Content: {post_content}
                        Commenter Name: {comment_author}
                        Comment Body: {comment_body}
                        Parameter Indicating weather comment to Post or reply to another Comment: {is_reply_to_post}
                        Parent Comment body: {parent_comment_body}
                        
                 """,
                ),
            ]
        )

        chain = prompt | llm
        response = chain.invoke(
            {
                "post_title": post[1],
                "post_content": post[3],
                "comment_author": comment[2],
                "comment_body": comment[3],
                "is_reply_to_post": is_reply_to_post,
                "parent_comment_body": parent_comment[3],
            }
        )
        return response.content


def main():
    conn = sqlite3.connect("reddit_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM comments")
    comments = cursor.fetchall()

    messages = []
    for comment in comments:
        is_reply_to_post = False
        if comment[1] == comment[4]:  # Check if parent_id is a post ID
            is_reply_to_post = True
        message = generate_message(comment, conn, is_reply_to_post)
        print(message)
        message_data = {
            "author_id": comment[0],
            "comment": comment[2],
            "is_reply_to_post": is_reply_to_post,
            "personalized_message": message,
        }
        messages.append(message_data)

    with open("generated_messages.json", "w") as outfile:
        json.dump(messages, outfile, indent=4)

    conn.close()
    print("JSON file created with generated personalized messages.")


if __name__ == "__main__":
    main()
