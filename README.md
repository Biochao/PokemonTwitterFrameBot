# PokemonFrameBot
Every Pokemon Frame in Order Twitter Bot
https://twitter.com/PKMNFrames

Parts modified from spacebruce's Monogatari bot

Disclamer: I'm not a python developer I don't know what I'm doing... Most of this was created with the help of ChatGPT... If you think you can make this bot better feel free to make a pull request.

Features include:
  
  • Option to read a subtitle file and add the correct caption to the tweet
  To use srt files for captions frames need to be named in milliseconds by ffmpeg
  
  • Option for Discord error reporting and end of episode messages
  
  • Option to not connect to Twitter for testing
  
  • groups of posts with variable delay
  
  • progress file to resume incase of errors or interuptions


How to use:
Insert your Twitter API credentials

Insert your Discord webhook if you want status reports

Set the frame_dir, this is the folder that contains the episode folders. 
The bot will use the season number and episode number you set provided your episode folders are named like this: "s1e1sub" This can be changed by editing the sub_frames variable.


If you want to have subtitles in the post set the folder where your srt files are with source_dir and the episode_name variable being the srt filename without the extension for the episode.

Execute the Python file

Answer the startup options questions

Done!
