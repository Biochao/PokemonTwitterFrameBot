import pysrt
from pysrt.srttime import SubRipTime
import tweepy
import discord
from discord import Webhook, RequestsWebhookAdapter, File
import os
import time
import datetime

# Config
frame_dir = r"C:/Users/framebot/bots/pokemonFrames/"
season_num = 1
episode_num = 24
episode_name = "Pokemon-1x24-HaunterVersusKadabra" # Name of subtitle file
tweet_text = r"Pokémon Season 1 Episode 24 - Haunter versus Kadabra"
hashtags = r"#pokemon #s1e24 #anime #anipoke"
# Timing Config
delay = 1 # Seconds inbetween each Tweet
wait_time = 900 # Seconds after a group of Tweets
group = 5 # How many Tweets per group
# Subtitle Config
source_dir = "C:/Users/framebot/bots/sources/Season 01/" #Directory of the subtitle file
sub_type = ".srt" # Format of subtitles
# Use a subtitle file?
subtitled = input('Does this episode have an external subtitle file (y/n)? ')
if subtitled.lower() == 'y':
    subs = pysrt.open(f"{source_dir}{episode_name}{sub_type}") # Full location of the subtitle file
else:
    subs = ""

# Initialize a counter variable to track how many frames of a group have been tweeted
counter = 0
Now = datetime.datetime.now()

# Online mode?
connect_to_twitter = input('Do you want to connect to Twitter (y/n)? ')

# Replace these with your own Twitter API keys
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"


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
webhookid = YOUR_WEBHOOK_ID
token = "YOUR TOKEN"
webhook = Webhook.partial(webhookid, token, adapter=RequestsWebhookAdapter())
  
# The folder where your images are stored (This only need to be changed if folder stucture changes. Currently set up for folders named like this: folder/s1e1/frames)
image_folder = f"{frame_dir}s{season_num}e{episode_num}sub"
print(f"Image folder: {image_folder} loaded")

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
        webhook.send(f"New Twitter Bot started")

# Determine how many frames there are
ListLength = len(os.listdir(image_folder))
print(ListLength, "files found")

# Report how long this episode will run for
TimeLength = (ListLength-index)/(60/wait_time*group)
print(f"Running for {TimeLength} hours")
endtime = Now + datetime.timedelta(hours = TimeLength)
print(f"EndTime: {endtime}")
if connect_to_discord.lower() == 'y':
    webhook.send(f"Running until {endtime}")
    
# Tweet each image in the folder starting from the saved index
for i, file in enumerate(os.listdir(image_folder)):
    # Check if the file is an image
    if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.gif'):
        # Skip files before the saved index
        if i < index:
            continue
        print(index)
        file_path = os.path.join(image_folder, file)
        filename = file
        # Split the extension from the filename
        base_name, file_extension = os.path.splitext(file)
        
        # Create a SubRipTime instance with the time in milliseconds
        timestamp = int(base_name[:8])
        if subtitled.lower() == 'y':
            caption = subs.at(timestamp)
        else:
            caption = ""
            
        Status = f"{tweet_text}\nFrame {index+1}/{ListLength} {hashtags}\n{caption.text if caption else ''}"
        print(Status)
        
        retries = 0
        success = False
        while not success and retries < 10:
            try:
                # Tweet the image
                if connect_to_twitter.lower() == 'y':
                    file = api.media_upload(file_path)
                    api.update_status(Status, media_ids = [file.media_id])
                else:
                    print(f"Processing file {file}")
                success = True
            except:
                print(f'Error while tweeting image {file}')
                retries += 1
                print('Trying again in 10 seconds.')
                if connect_to_discord.lower() == 'y':
                    webhook.send(f"Twitter Bot encountered an error and is trying again")
                time.sleep(10)
        if not success:
            print(f'Failed to tweet image {file} after {retries} attempts')
            if connect_to_discord.lower() == 'y':
                webhook.send(f"Twitter Bot failed to tweet image {file} after {retries} attempts")
            break
        
        # Increment the index
        index += 1
        # Save progress to text file
        with open("progress.txt", "w") as f:
            f.write(str(index))
        
        # Sleep for a specified delay before posting the next frame
        print(f"Waiting for {delay} seconds till the next frame\n")
        time.sleep(delay)
        
        # Increment the counter
        counter += 1

        # If the counter has reached 5, sleep for the specified wait time
        # before resetting the counter and continuing to tweet the next batch of frames
        if counter == group:
            print(f"Group posted waiting for {wait_time} seconds\n")
            time.sleep(wait_time)
            counter = 0
            
# Wait for user input before exiting
if connect_to_discord.lower() == 'y':
    webhook.send(f"Twitter Bot finished episode")
input("End of the video. Press Enter to restart...")
