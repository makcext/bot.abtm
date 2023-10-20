import praw
import telebot
import pickle
import time

channel_id = "-1001715730728"

def download_posts_from_subreddit(last_timestamp):
	reddit = praw.Reddit(
		client_id="YJ85gCYgTVVMtcdsY4jzcw",
		client_secret="hiPHteFqF5Xb9OUQNBsYfda71L-CxQ",
		user_agent="myapp/1.0",
	)

	subreddit = reddit.subreddit("greece")
	# subreddit = reddit.subreddit("bottestabtm")

	posts = subreddit.new(limit=3)

	downloaded_posts = []
	new_last_timestamp = last_timestamp

	for post in posts:
		post_timestamp = post.created_utc
		if post_timestamp > last_timestamp:
			downloaded_posts.append(post)
			new_last_timestamp = max(new_last_timestamp, post_timestamp)

	return downloaded_posts, new_last_timestamp


# Function to filter posts based on their flair
def process_posts(downloaded_posts):
	for post in downloaded_posts:
		if post.link_flair_text == ":zz_question: ερωτήσεις/questions":
			continue  # Skip this post

		# Send the post title and URL to the Telegram channel
		bot.send_message(
			chat_id=channel_id,
			text=f"<a href='{post.url}'>link</a>",
			parse_mode="HTML",
			disable_web_page_preview=False
		)


def save_last_timestamp(last_timestamp):
	with open("last_timestamp.txt", "wb") as file:
		pickle.dump(last_timestamp, file)


def load_last_timestamp():
	try:
		with open("last_timestamp.txt", "rb") as file:
			last_timestamp = pickle.load(file)
	except FileNotFoundError:
		last_timestamp = 0

	return last_timestamp


def main():
	# Load the last timestamp from file
	last_timestamp = load_last_timestamp()

	# Download new posts from the subreddit
	downloaded_posts, new_last_timestamp = download_posts_from_subreddit(last_timestamp)

	# Process the downloaded posts
	process_posts(downloaded_posts)

	# Save the new last timestamp to file
	save_last_timestamp(new_last_timestamp)


if __name__ == "__main__":
	# Initialize the Telegram bot
	bot = telebot.TeleBot("6105348307:AAGK-UaRDXrFdZhYSP_t8gY4aYjbDO5SN6s")

	# Call the main function every minute
	while True:
		main()
		time.sleep(300)		
		print("Sleeping for 300 seconds")

