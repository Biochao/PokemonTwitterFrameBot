import tweepy
import discord
from discord import Webhook, RequestsWebhookAdapter, File
import pysrt
from pysrt.srttime import SubRipTime
import os
import time
import datetime

# Directory Config
frame_dir = r"C:/Users/framebot/bots/pokemonFrames/" #This is the folder with all the episode folders
subtitles_dir = "C:/Users/framebot/bots/sources/srt"
# Current episode config
season_num = 1
episode_num = 46
tweet_text = f"Pokémon Season {season_num} Episode {episode_num} - Attack of the Prehistoric Pokémon"
hashtags = f"#pokemon #s{season_num}e{episode_num} #anime #anipoke"
notification = ""
# Timing Config
delay = 5 # Seconds inbetween each Tweet
wait_time = 3600 # Seconds after a batch of Tweets
batch = 2 # How many Tweets per batch
group = 4 # How many images per tweet

# The folder where your images are stored (This only need to be changed if folder stucture changes. Currently set up for folders named like this: folder/s1e1/frames)
current_episode_folder = f"s{season_num}e{episode_num}"
image_folder = os.path.join(frame_dir,current_episode_folder)

# Load captions if there is one
pattern = f"{season_num}x{episode_num}" #naming pattern to look for
extension = ".srt"
for filename in os.listdir(subtitles_dir):
    full_path = os.path.join(subtitles_dir, filename)
    if os.path.isfile(full_path) and full_path.endswith(extension) and pattern in full_path:
        match = True
        break
if match:
    print(f"Subtitle file found {full_path}")
    captioned = True
else:
    print("No episode number match found. Filenames should have an x separating the season number from the episode number.")
if captioned:
    subs = pysrt.open(full_path)
    print(f"Subtitle file loaded")
else:
    subs = ""

# Initialize a counter variable to track how many frames of a batch have been tweeted
counter = 0
Now = datetime.datetime.now()

# Online mode?
connect_to_twitter = input('Do you want to connect to Twitter (y/n)? ')

# Replace these with your own Twitter API keys
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

if connect_to_twitter.lower() == 'y':
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        print("Connected to Twitter!")
    except:
        print("Twitter not OK, try again")
        time.sleep(10)
  
# Error Notifications?
connect_to_discord = input('Do you want to report to Discord (y/n)? ')
  
# Discord Error Reporting
webhookid = 1234567890
token = ""
webhook = Webhook.partial(webhookid, token, adapter=RequestsWebhookAdapter())
  
image_folder = f"{frame_dir}s{season_num}e{episode_num}sub"
# image_folder = f"{frame_dir}testSingle"
print(f"Image folder: {image_folder} loaded")

# Confirmation to start   
print(tweet_text)
input("Press any key to start")

# Load the index from a file (or initialize it to 0 if the file doesn't exist)
index_file = "progress.txt"
if os.path.exists(index_file):
    with open(index_file) as f:
        index = int(f.read())
    print("Progress file found. Resuming.")
    if connect_to_discord.lower() == 'y':
        webhook.send(f"Twitter Bot resuming at frame {index+1}")
else:
    index = 0
    print("No index file found. Starting from the beginning")
    if connect_to_discord.lower() == 'y':
        webhook.send(f"Twitter Bot started {tweet_text}")

# Determine how many frames there are
ListLength = len(os.listdir(image_folder))
print(ListLength, "files found")

# Report how long this episode will run for
# Calculate the time length in seconds
time_length_seconds = (ListLength - index) * wait_time / batch

# Create a timedelta object to represent the time length
time_length = datetime.timedelta(seconds = time_length_seconds)

# Convert the time length to hours
time_length_hours = time_length.total_seconds() / 3600

# Calculate the time to the end of the series
episodes_left = 1234 - (episode_num + 0) # Add previous season episodes to count
series_time_left = round(time_length_hours * episodes_left / 24 / 365, 1)

# Calculate the end time by adding the time length to the current time
endtime = datetime.datetime.now() + time_length
endtime_minute_only = endtime.strftime("%Y-%m-%d %H:%M")

print(f"Running for {time_length_hours} hours")
print(f"EndTime: {endtime}")
if connect_to_discord.lower() == 'y':
    webhook.send(f"Running until {endtime_minute_only}")

if index == 0:    
    if connect_to_twitter.lower() == 'y':
        api.update_status(f"Pokébot starting new episode {tweet_text}\n Estimated running time {time_length_hours} hours. End time: {endtime_minute_only}\n\nThere are {episodes_left} regular episodes left. At the current pace it will take at least {series_time_left} years to finish.")

# Get the list of images in the folder
images = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.gif')]    
# Tweet multiple images per tweet
for i in range(0, len(images), group):
    images_to_tweet = images[i:i+group]
    # Skip files before the saved index
    if i < index:
        continue
    print(index)
    
    # Create a list to store the alt text for each image
    alt_text_to_tweet = []
    for j, image in enumerate(images_to_tweet):
        # Get the base name of the file
        base_name = os.path.basename(image)
        # Create a SubRipTime instance with the time in milliseconds
        timestamp = int(base_name[:8])
        if captioned:
            caption = subs.at(timestamp)
        else:
            caption = ""
        alt_text_to_tweet.append(caption.text)

       
    Status = f"{tweet_text}\nFrames {index+1}-{index+len(images_to_tweet)} of {ListLength} {hashtags}{notification if counter == batch-1 else ''}"
    print(Status)
    
    retries = 0
    success = False
    while not success and retries < 5:
        if len(images_to_tweet) > 0:
            try:
                # Upload the images and get the media ids
                media_ids = []
                media_metadata_list = []
                for image, alt_text in zip(images_to_tweet, alt_text_to_tweet):
                    # Upload media
                    response = api.media_upload(filename=image)
                    print(f"Uploaded {image}")

                    # Append media ID to list
                    media_ids.append(response.media_id)

                    # Create media metadata with alt text
                    media_metadata = api.create_media_metadata(response.media_id, alt_text)

                
                # Tweet the images
                if connect_to_twitter.lower() == 'y':
                    # Post the tweet with up to 4 images and their corresponding alt text
                    tweet = api.update_status(status=Status, media_ids=media_ids)
                else:
                    print(f"Processing files {images_to_tweet}")
                    time.sleep(3)
                success = True
            except tweepy.error.TweepError as error:
                print(f'Error while tweeting images {images_to_tweet}: {error}')
                retries += 1
                print('Trying again in 60 seconds.')
                if connect_to_discord.lower() == 'y':
                    try:
                        webhook.send(f"Twitter Bot encountered an error and is trying again")
                    except:
                        time.sleep(60)
                time.sleep(60)
    if not success:
        print(f'Failed to tweet image {file} after {retries} attempts')
        if connect_to_discord.lower() == 'y':
            webhook.send(f"Twitter Bot failed to tweet image {file} after {retries} attempts")
        # Wait for user input before exiting
        input("Too many errors. Press Enter to restart...")
    
    # Increment the index
    index += group
    # Save progress to text file
    with open("progress.txt", "w") as f:
        f.write(str(index))
    
    # Sleep for a specified delay before posting the next frame
    print(f"Waiting for {delay} seconds till the next frame\n")
    time.sleep(delay)
    
    # Increment the counter
    counter += 1

    # If the counter has reached the batch amount, sleep for the specified wait time
    # before resetting the counter and continuing to tweet the next batch of frames
    if counter == batch:
        print(f"Group posted waiting for {wait_time} seconds\n")
        time.sleep(wait_time)
        counter = 0
        

if connect_to_discord.lower() == 'y':
    webhook.send(f"Twitter Bot finished episode")
os.remove("progress.txt")

# Ending tweet
if connect_to_twitter.lower() == 'y':
    api.update_status(f"To be continued...\n \n This is a fan run page. If you'd like to support me check out my Redbubble for fan-made designs on shirts, stickers and more!\n https://biochao.redbubble.com")

# Wait for user input before exiting
input("End of the video. Press Enter to restart...")
