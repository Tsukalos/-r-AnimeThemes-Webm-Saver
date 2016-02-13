#/r/AnimeThemes Anime Webm Saver
#
#Created by Pedrowski
#Version: 1.0a
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
import re


#LOGGING CONFIGURATION
# create logger
loggerDownload = logging.getLogger('[Donwload Log]')
loggerDownload.setLevel(logging.DEBUG)
loggerError = logging.getLogger('[Error Log]')
loggerError.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
# create filehandlers
fhd = logging.FileHandler('downloadlog.log', encoding='utf-8')
fhe = logging.FileHandler('errorlog.log', encoding='utf-8')
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
##Default location
#Download directory
FILEDIR = "files"
#Downloaded ids
DOWNLOADED = "dtracker"


if not os.path.exists(FILEDIR):
    #creates the 'files' folder
    print("Creating '"+FILEDIR+"' folder...")
    os.makedirs(FILEDIR)
    print("... Done")

#creates the file id
if not os.path.isfile(DOWNLOADED):
	flog = open(DOWNLOADED,"x")
	flog.close()
	
#defines location to save file
downloadlocation = FILEDIR+"/"


### Gets the comments of the post to look for mirrors (many archived posts have mirrors in the comments because the shutdown of a.pomf)
def commentmirror(submission):
	flatcom = praw.helpers.flatten_tree(submission.comments)
	for comment in flatcom:
		p = re.compile('(?P<url>https?://[^\s]+)')
		result = p.search(comment.body).group()
		if result != "None":
			fileurl = result
			return fileurl
			
	return "None"
## Unused function (old legacy urllib method)
def downloadhook(count, blockSize, totalSize):
    percent = int(count*blockSize*100/totalSize)
    sys.stdout.write("Download progress:   %d%%   \r" % (percent) )
    sys.stdout.flush()

## gets the submission and downloads, also logs to file	
def downloadsub(submission):
	errorflag = False
	mirrorflag = False
	result = ""
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
		result = commentmirror(submission)
		if result != "None":
			mirrorflag = True
		else:
			loggerError.error("Error in requesting %s from url %s",filetitle,fileurl)
			loggerError.error("%s %s",err.reason, err.code)
			loggerError.error(err.headers)
			print("[Error details in errorlog.log]")
			errorflag = True
	if mirrorflag:
		try:
			fileurl = result
			url = urllib.request.Request(fileurl, headers = {'User-Agent': USERHEAD})
			url = urllib.request.urlopen(url)
			print("URL FETCHED FROM MIRROR")
			errrorflag = False
		except (urllib.error.URLError, urllib.error.HTTPError) as err:
			print("[Error message (Mirror):]" , err.reason, err.code)
			print("[There was a error with requesting the file from the url: (MIRROR)] ")
			loggerError.error("Error in requesting %s from url (mirror)%s",filetitle,fileurl)
			loggerError.error("%s %s",err.reason, err.code)
			loggerError.error(err.headers)
			print("[Error details in errorlog.log]")
			errorflag = True

	if errorflag:
		return "urlerror"
	
	print("")
	print("")
	print("")
	print("[DOWNLOADING FROM:] " + fileurl )
	print("[FILE TITLE:] " + filetitle)
	print("[LOCATION:] " + downloadlocation)
	
	#checks if submission is a text post
	if postdomain == 'self.AnimeThemes':
		print("File is not a video, jumping to next...]")
		time.sleep(2)
		errorflag = True
	
	if errorflag:
		return "notvideo"
	
	flag = False
	fa = open(DOWNLOADED,"r")
	for line in fa:
		if str(line) == (id+"\n"):
			print("[File already present, jumping to next...]")
			flag = True
			break
	fa.close();
	if flag == True:
		return "filepresent"
	
	
	fileloc = downloadlocation + filetitle + ".webm"
		
	with open(fileloc, mode="wb") as f:
		f.write(url.read())
	f.close();
	fid = open(DOWNLOADED,"a")
	fid.write(id+"\n");
	fid.close();
	#Old ulrretrieve method	
	#urllib.request.urlretrieve(fileurl,fileloc, reporthook=downloadhook)
	loggerDownload.info('Submission id: %s | Original name: %s | File name: %s | Url: %s',id,originaltitle,filetitle,fileurl)
	print("[DOWNLOAD COMPLETE.]")
	print("///////////////////////////////////////")

## search function
def search(r):
	print("Please type the name of the series you want to look for")
	anititle = str(input())
	print("")
	print("")
	print("Are you looking for a 'op' or 'ed'? (type 'x' to leave it alone)")
	while True:
		type = str(input())
		if type == "ed" or type == "op" or type == "x":
			if type == "x":
				type = ""
			else:
				type = "title:"+type
			break
		else:
			print("plese input again")
	query = anititle+" "+type
	submissions = r.search(query, subreddit="animethemes",sort="relevance")
	sublist = list()
	k = 0
	for submission in submissions:
		print("["+str(k)+"] 	- - "+bytes(submission.title.encode("ascii","ignore")).decode('unicode_escape'))
		print("")
		k = k+1
		sublist.append(submission)
	
	print("")
	print("Type the number in the brackets of the submission")
	print("you want to get, or type 'x' to do another search")
	while True:
		ra = input()
		try:
			ra = int(ra)
		except:
			search(r)
		try:
			sub = sublist[ra]
			break
		except:
			print("please input a valid submission, type 'x' if")
			print("you want to do another search")
		
	downloadsub(sub)
		
		
#end search

## looks for new submissions in the subreddit
def new(r):
	
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
			downloadsub(submission)
			
		print("")
		
		print("[> > > > No more new submissions, entering rest...]")
		
		for x in range(0,waittime):
			timeleft = ((waittime*60)-(60*x))/60
			sys.stdout.write("["+str(int(timeleft)) + " mintues remaining to next check...  ]\r")
			sys.stdout.flush()
			time.sleep(60)

#end new

#### Main Program
r = praw.Reddit('AnimeThemeSaver')

print("Hello, welcome to the /r/AnimeThemes submission downloader, ")
while True:
	print("Type S to search or type N to look for new submissions")
	res = input()
	res = res.lower()
	if res != "s" and res != "n":
		print("please input again")
	else:
		if res == "s":
			search(r)
		if res == "n":
			new(r)






