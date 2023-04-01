# PokemonFrameBot
Every Pokemon Frame in Order Twitter Bot
https://twitter.com/PKMNFrames

Parts modified from spacebruce's Monogatari bot

Disclamer: I'm not a python developer I don't know what I'm doing... Most of this was created with the help of ChatGPT... If you think you can make this bot better feel free to make a pull request.

Features include:
  
  • Set the amount of images per tweet so it can better comply with Twitter's new free API limits of 1500 tweets per month.
  
  • Option to read a subtitle file and add the correct caption to the tweet
  To use srt files for ALT text captions, frames need to be named in milliseconds by ffmpeg
  srt file will be found automatically if the filename contains the season and episode number like this: "1x01"
  
  • Option for Discord error reporting and end of episode messages
  
  • Option to not connect to Twitter for testing
  
  • batches of posts with variable delay
  
  • progress file to resume incase of errors or interuptions
  
  • Startup and ending tweets
    I use a startup tweet to say how long an episode will run for and an ending tweet for self promotion
    
  • Optional message in the last tweet of the batch
    The notification variable will append a message to the last tweet of a batch


How to use:
Install, tweepy, discord and pysrt using PIP

Insert your Twitter API credentials

Insert your Discord webhook if you want status reports

Set the frame_dir, this is the folder that contains the episode folders. 
The bot will use the season number and episode number you set provided your episode folders are named like this: "s1e1sub" This can be changed by editing the sub_frames variable.


If you want to have subtitles in the post set the folder where your srt files are, if the filenames are formated like this "1x01" they will be set automatically by the season and episode number variables.

Execute the Python file

Answer the startup options questions

Done!
