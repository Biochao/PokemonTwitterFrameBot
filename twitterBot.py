author;
	Original - 𝚜𝚙𝚊𝚌𝚎 ☆ 𝚋𝚛𝚞𝚌𝚎 (@spacebruce)
    Modified - Biochao (@biochao)
    
needed;
	pip install pause
	pip install tweepy
    pip install pytgbot
instructions;
	install python3
	type the needed^ lines
	put twitterbot.py in folder
	put your twitter and telegram tokens in the config area below and change values as desired
	click on twitterbot.py
	???
	profit
license;
	           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
	                   Version 2, December 2004
	Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
	Everyone is permitted to copy and distribute verbatim or modified
	copies of this license document, and changing it is allowed as long
	as the name is changed.
	           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
	  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
	 0. You just DO WHAT THE FUCK YOU WANT TO.
	 http://www.wtfpl.net/about/

import tweepy
import time
import sys
import pause
import datetime
import os.path
from glob import glob
from pytgbot import Bot

print("Pokemon Framebot v2.5")

#login
Online = True #Set to False for offline debug mode
ApiKey = ""
ApiKeySecret = ""
AccessToken = ""
AccessTokenSecret = ""

#Telegram Error Reporting
API_KEY=''  # change this to the token you get from @BotFather
CHAT=''  # can be a @username or a id, change this to your own @username or id for example.
bot = Bot(API_KEY)

# config
Caption = r"Pokemon Season 1 Episode 1 - Pokemon I choose you! - " # post caption
Path = "./pokemonEpisodes/s1e1/*.jpg" # image search path/parameters. uses glob syntax (https://en.wikipedia.org/wiki/Glob_%28programming%29#Syntax). ".*.jpg" for same dir, "./images/*.jpg" for images subdir, etc
Interval = 1   # seconds between individual tweets
groupNum = 3 # number of tweets in a group
groupInterval = 15   # minutes between groups
DelayStart = False

IconFile = "\icon.jpg"
HeaderFile = "\header.jpg"

# functions

def Panic():
        # api.update_status(ErrorMessage)
        bot.send_message(CHAT, "Twitter Bot encountered and error!")
        print(ErrorMessage)
        Errors = 0

def GetFiles(rootPath, verbose):
        foundfiles = glob(rootPath)
        files = []
        for item in foundfiles:
                if (IconFile not in item) and (HeaderFile not in item):
                        files.append(item)
                else:
                        if(verbose):    
                                print("removed ", item)
        return files

def SendTweet(message,filename):
        Name = os.path.splitext(os.path.basename(filename))[0]
        print("post", Name, filename)
        Status = f"{Caption} Frame {index+1} of {ListLength}"
        if Online:      # Offline mode always works
                try:
                        # api.update_with_media(filename, status=Name)
                        file = api.media_upload(filename)
                        api.update_status(Status, media_ids = [file.media_id])
                        return True
                except:
                        print("posting broke somewhere, trying again")
                        for e in sys.exc_info():
                                print(e)
                        return False
        else:
                return True

def ChangeIcon(path):
        print("Icon change ", path)
        if Online:
                File = open(path)
                update_profile_image(path, File)
                File.close()
    
def ChangeHeader(path):
        print("Header change ", path)
        if Online:
                File = open(path)
                update_profile_banner(path, File)
                File.close()
                
# initial state
StartIndex = 0

# load images
ImageList = GetFiles(Path, True)
ListLength = len(ImageList)
print(ListLength, "files")

# resume state
if not os.path.isfile("state.txt"):
        with open("state.txt","w") as saveFile:
                saveFile.write(ImageList[0])
        print("Starting new state file")
else:
        with open("state.txt","r") as saveFile:
                line = saveFile.readlines()
                lastImage = line[0]
                lastImage.replace(r"//",r"/")
        try:
                StartIndex = ImageList.index(lastImage)
        except:
                StartIndex = 0
        print("Resuming at " + ImageList[StartIndex])

# twitter login
if Online:
        auth = tweepy.OAuth1UserHandler(ApiKey, ApiKeySecret, AccessToken, AccessTokenSecret)
        api = tweepy.API(auth)
        try:
                api.verify_credentials()
                print("twitter OK")
        except:
                print("twitter not OK, try again (", sys.exc_info()[0], ")")
                sys.exit()
else:
        print("Offline testing mode")


#post
LastDirectory = ""
index = StartIndex
group = 0
while(index <= ListLength):
        while(index < ListLength):
                next = (index + 1)
                Now = datetime.datetime.now()
                DoPost = True
                ImageName = ""
                while(DoPost):
                        try:
                                ImageName = ImageList[index]

                                print("file ", index, "/", ListLength-1)
                                sent = SendTweet(Caption, ImageName)
                                if sent:
                                        print("OK!")
                                        print(f"{Caption}")
                                        group = group+1
                                        print("On to the next image")
                                        try:
                                                with open("state.txt","w") as saveFile:
                                                        if(next < index):
                                                                StartIndex = 0
                                                        ImageName = ImageList[next]
                                                        saveFile.write(ImageName)
                                        except:
                                                print("Progress not saved to file!! (", sys.exc_info()[0], ")")
                                        DoPost = False  #no need to retry
                                        index = next
                                else:
                                        print("Trying again")
                        except:
                                print("posting broke somewhere, trying again")
                                for e in sys.exc_info():
                                        print(e)

                                
                        if DoPost:      # retry every 5 seconds after error
                                Now += datetime.timedelta(seconds = 5)
                                pause.until(Now)
                        else: #normal posting schedule

                                # Update icon paths
                                try:
                                        Directory = os.path.dirname(ImageName)
                                        # print("dir", Directory)
                                        if (Directory != LastDirectory):
                                                print("Directory changed", Directory)
                                                if os.path.isfile(Directory + IconFile):
                                                        ChangeIcon(Directory + IconFile)
                                                if os.path.isfile(Directory + HeaderFile):
                                                        ChangeHeader(Directory + HeaderFile)
                                except:
                                        print("can't update icons, error?")
                                
                                LastDirectory = Directory
                                
                                NewList = GetFiles(Path, False)        #Reload DB
                                NewLength = len(NewList)
                                if NewLength != ListLength:     #If DB changed
                                        ImageList.clear()       #clear out old (unnecersary?)
                                        ImageList = NewList     #Use new DB
                                        print("Database change detected! Change delta : ", NewLength - ListLength, "(",NewLength,")")
                                        ListLength = NewLength  #Update length
                                        newIndex = ImageList.index(ImageName)  
                                        if next != newIndex:     #If point EARLIER than current post has been edited, reseek
                                                print("Update post index pointer", index, "to", newIndex)
                                                index = newIndex
                                if group<groupNum:
                                    print("Delaying next post for", Interval, "seconds")
                                    time.sleep(Interval) #Delay next post in group
                                if group==groupNum:
                                    minutes = 60
                                    print("Delaying next post for", groupInterval, "minutes \n")
                                    time.sleep(groupInterval*minutes) #Delay next post in group
                                    group = 0
                                if index+1 == ListLength+1:
                                    print("Sequence End!")
                                    if Online:
                                        api.update_status("#ToBeContinued - End of the episode!")
                                        bot.send_message(CHAT, "Twitter Bot - End of the episode!")
                                    print("Waiting until user input")
                                    time.sleep(9999*minutes) #Wait for a long time
print("Sequence End!")
