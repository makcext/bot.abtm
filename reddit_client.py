import asyncpraw
from config import CLIENT_ID, CLIENT_SECRET, USER_AGENT, COUNT_OF_POSTS_TO_DOWNLOAD

async def download_new_posts(last_timestamp):
    reddit_client = asyncpraw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
    )

    # subreddit_instance = await reddit_client.subreddit("pics")
    subreddit_instance = await reddit_client.subreddit("greece")

    new_posts = subreddit_instance.new(limit=COUNT_OF_POSTS_TO_DOWNLOAD)

    downloaded_posts = []
    updated_last_timestamp = last_timestamp

    async for post in new_posts:
        post_timestamp = post.created_utc
        if post_timestamp > last_timestamp:
            downloaded_posts.append(post)
            updated_last_timestamp = max(updated_last_timestamp, post_timestamp)

    await reddit_client.close()
   
    downloaded_posts.reverse()
    # print(downloaded_posts)
    return downloaded_posts, updated_last_timestamp