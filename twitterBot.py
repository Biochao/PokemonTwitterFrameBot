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

import requests
import discord
from discord import Webhook, RequestsWebhookAdapter, File
import tweepy
import time
import sys
import pause
import datetime
import os.path
from glob import glob

print("Pokemon Framebot v2.7")

#login
Online = True #Set to False for offline debug mode
ApiKey = ""
ApiKeySecret = ""
AccessToken = ""
AccessTokenSecret = ""

# Discord Error Reporting
webhookid = 123456890
token = ""
webhook = Webhook.partial(webhookid, token, adapter=RequestsWebhookAdapter())

# config
Caption = r"Pokémon Season 1 Episode 14 - Electric Shock Showdown - " # post caption
hashtags = r"#pokemon #anime #anipoke"
Path = "../pokemonFrames/s1e14sub/*.jpg" # image search path/parameters. uses glob syntax (https://en.wikipedia.org/wiki/Glob_%28programming%29#Syntax). ".*.jpg" for same dir, "./images/*.jpg" for images subdir, etc
Interval = 1   # seconds between individual tweets
groupNum = 4 # number of tweets in a group
groupInterval = 18   # minutes between groups

IconFile = "\icon.jpg"
HeaderFile = "\header.jpg"

# functions

def Panic():
        # api.update_status(ErrorMessage)
        webhook.send("Twitter Bot encountered and error!")
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
        Status = f"{Caption} Frame {index+1} of {ListLength} {hashtags}"
        sens = "cut"
        print(Status)
        if Online:      # Offline mode always works
                try:
                        # api.update_with_media(filename, status=Name)
                        file = api.media_upload(filename)
                        if sens in filename:
                            api.update_status(Status, media_ids = [file.media_id], possibly_sensitive = true)
                        else:
                            api.update_status(Status, media_ids = [file.media_id])
                        return True
                except:
                        webhook.send("Twitter Bot encountered and error and is trying again!")
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
Now = datetime.datetime.now()

# load images
ImageList = GetFiles(Path, True)
ListLength = len(ImageList)
print(ListLength, "files")

# resume state
if not os.path.isfile("state.txt"):
        with open("state.txt","w") as saveFile:
                saveFile.write(ImageList[0])
        print("Starting new state file")
        TimeLength = ListLength/(60/groupInterval*groupNum)
        print(f"Running for {TimeLength} hours")
        endtime = Now + datetime.timedelta(hours = TimeLength)
        print(f"EndTime: {endtime}")
        webhook.send(f"Twitter Bot started {Caption} Running until {endtime}")
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
                TimeLength = ListLength-ImageList[StartIndex]/(60/groupInterval*groupNum)
                print(f"Running for {TimeLength} hours")
                endtime = Now + datetime.timedelta(hours = TimeLength)
                print(f"EndTime: {endtime}")
                webhook.send(f"Twitter Bot started {Caption} Running until {endtime}")

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
                                print(ImageName)
                                sent = SendTweet(Caption, ImageName)
                                if sent:
                                        print("OK!")
                                        group = group+1
                                        print("On to the next image")
                                        try:
                                                with open("state.txt","w") as saveFile:
                                                        if(next < index):
                                                                StartIndex = 0
                                                        ImageName = ImageList[next]
                                                        saveFile.write(ImageName)
                                        except:
                                                webhook.send("Twitter Bot encountered and error!")
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
                                        webhook.send("Twitter Bot - End of the episode!")
                                    print("Waiting until user input")
                                    input("Close the window or press enter to restart...")
print("Sequence End!")
