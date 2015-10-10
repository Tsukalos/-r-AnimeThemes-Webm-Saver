#/r/AnimeThemes Anime Webm Saver
#
#Created by Pedrowski
#Version: 0.0.2
#Contact: /u/Pedrowski
#
# This is under the GNU GPL V3 so use it
# and modify it however you want
#
#
#
import praw
import sys
import urllib.request
import time
import os
import os.path
import logging


logging.basicConfig(filename='log.log', level=logging.DEBUG)
logging.debug('Log start')
logging.debug('/////////')

def downloadhook(count, blockSize, totalSize):
    percent = int(count*blockSize*100/totalSize)
    sys.stdout.write("Download progress: %d%%   \r" % (percent) )
    sys.stdout.flush()

if not os.path.exists("files"):
    #creates the 'files' folder
    print("Creating 'files' folder...")
    os.makedirs("files")
    print("... Done")
#defines location to save file
downloadlocation = "files/"
r = praw.Reddit('WebmAnimeSaver')
print("Hello, welcome to the /r/AnimeThemes submission downloader, ")
print("please enter the interval time (minutes) between the searches: ")
#^
while True:
    try:
        waittime = int(input())
        break
    except:
        print("There was a error in the value, please input a valid number!")
print("Enter the number of new submissions,")
print("the program should check each time (MAX 100): ")
#^
while True:
    try:
        postnumber = int(input())
        if postnumber > 100:
            print("The value is too high, please input a value lower than 100 submissions")
        else:
            break
    except:
        print("There was a error in the value, please input a valid number!")
subreddit = r.get_subreddit('animethemes')
while True:
    print("Getting submission information (may take time depending of new submissions number)...")
    for submission in subreddit.get_new(limit=postnumber):
        fileurl = submission.url
        postdomain = submission.domain
        filetitle = submission.title.replace('"', '').replace(':', '').replace('?', '').replace('/','').replace("'","")
        print("")
        print("")
        print("")
        print("DOWNLOADING FROM: [" + fileurl + "]")
        print("FILE TITLE: [" + filetitle + "]")
        print("LOCATION: [" + downloadlocation + "]")
        fileloc = downloadlocation + filetitle + ".webm"
        if os.path.isfile(fileloc) == False and postdomain != 'self.AnimeThemes':
            urllib.request.urlretrieve(fileurl,fileloc, reporthook=downloadhook)
            logging.info(fileurl)
            logging.info(fileloc)
            logging.info('')
            print("DOWNLOAD COMPLETE.")
        else:
            print("File already present, jumping to next...")
            time.sleep(2)
        print("///////////////////////////////////////")
    print("")
    print("> > > > No more new submissions, entering rest...")
    for x in range(0,waittime):
        timeleft = ((waittime*60)-(60*x))/60
        print(str(int(timeleft)) + " mintues remaining to next check...") 
        time.sleep(60)

