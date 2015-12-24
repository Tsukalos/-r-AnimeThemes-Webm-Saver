#/r/AnimeThemes Anime Webm Saver
#
#Created by Pedrowski
#Version: 0.4.0
#Contact: /u/Pedrowski
#
# This is under the GNU GPL V3 so use it
# and modify it however you want
#
#
#

# Imports
import praw
import sys
import urllib.request
import urllib.error
import time
import os
import os.path
import logging


#LOGGING CONFIGURATION
# create logger
loggerDownload = logging.getLogger('[Donwload Log]')
loggerDownload.setLevel(logging.DEBUG)
loggerError = logging.getLogger('[Error Log]')
loggerError.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
# create filehandlers
fhd = logging.FileHandler('downloadlog.log')
fhe = logging.FileHandler('errorlog.log')
# set formatters
fhd.setFormatter(formatter)
fhe.setFormatter(formatter)
# set logging levels
fhd.setLevel(logging.DEBUG)
fhe.setLevel(logging.DEBUG)
# add handlers
loggerDownload.addHandler(fhd)
loggerError.addHandler(fhe)


#Header for urllib
USERHEAD = "Script for automatic download of webms, made by /u/Pedrowski"
#Default location
FILEDIR = "files"


# Download progress view
def downloadhook(count, blockSize, totalSize):
    percent = int(count*blockSize*100/totalSize)
    sys.stdout.write("Download progress:   %d%%   \r" % (percent) )
    sys.stdout.flush()
	

if not os.path.exists(FILEDIR):
    #creates the 'files' folder
    print("Creating '"+FILEDIR+"' folder...")
    os.makedirs(FILEDIR)
    print("... Done")
	
#defines location to save file
downloadlocation = FILEDIR+"/"



r = praw.Reddit('AnimeThemeSaver')

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
        if postnumber > 800:
            print("The value is too high, please input a value lower than 100 submissions")
        else:
            break
    except:
        print("There was a error in the value, please input a valid number!")
		
		
subreddit = r.get_subreddit('animethemes')


while True:
	print("Getting submission information") 
	print("(may take time depending of new submissions number)...")

	for submission in subreddit.get_new(limit=postnumber):
		fileurl = submission.url
		postdomain = submission.domain
		originaltitle = submission.title
		id = submission.id
		title = bytes(originaltitle.replace('"','').replace(':','').replace('?','').replace('/','').replace("'","").replace("*","").encode('ascii','ignore'))
		filetitle = title.decode('unicode_escape')
		try:
			url = urllib.request.Request(fileurl, headers = {'User-Agent': USERHEAD})
			url = urllib.request.urlopen(url)
		except (urllib.error.URLError, urllib.error.HTTPError) as err:
			print("///////////////////////////////////////")
			print("[There was a error with requesting the file from the url:] ")
			print(fileurl)
			print(filetitle)
			print("[Error message:]" , err.reason, err.code)
			loggerError.error("Error in requesting %s from url %s",filetitle,fileurl)
			loggerError.error("%s %s",err.reason, err.code)
			loggerError.error(err.headers)
			print("[Error details in errorlog.log]")
			continue
		
		
		print("")
		print("")
		print("")
		print("[DOWNLOADING FROM:] " + fileurl )
		print("[FILE TITLE:] " + filetitle)
		print("[LOCATION:] " + downloadlocation)
		
		
		fileloc = downloadlocation + filetitle + ".webm"
		
		
		
		if os.path.isfile(fileloc) == False and postdomain != 'self.AnimeThemes':
			with open(fileloc, "wb") as f:
				f.write(url.read())
			#Old ulrretrieve method	
			#urllib.request.urlretrieve(fileurl,fileloc, reporthook=downloadhook)
			loggerDownload.info('Submission id: %s | Original name: %s | File name: %s | Url: %s',id,originaltitle,filetitle,fileurl)
			print("[DOWNLOAD COMPLETE.]")
		else:
			print("[File already present or file is not a video, jumping to next...]")
			time.sleep(2)
			
			
		print("///////////////////////////////////////")
		
	print("")
	
	print("[> > > > No more new submissions, entering rest...]")
	
	for x in range(0,waittime):
		timeleft = ((waittime*60)-(60*x))/60
		sys.stdout.write("["+str(int(timeleft)) + " mintues remaining to next check...  ]\r")
		sys.stdout.flush()
		time.sleep(60)

