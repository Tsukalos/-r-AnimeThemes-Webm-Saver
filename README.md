# redditATS (AnimeThemesSaver)
Automated webm downloader whichs download anime openings and endings from /r/AnimeThemes

## Features

####  Search
Find the OP & ED of the series you are looking for. If the link is down, it will try to look for mirrors in the comments.

####   New posts
Regular searching for new submissons in the subreddit, useful for servers or people who want to keep all the files.

<hr>

If you have any suggestions or want to help in some way, feel free to contact me: <b><a href="https://www.reddit.com/user/Pedrowski/">/u/Pedrowski</a></b>

**Note** : Japanese characters (all unicode non-ascii) are removed from string, although I don't find this procedure right...

As for now you need to have <b><a href="https://praw.readthedocs.org/en/stable/">praw</a></b> (tested with version 3.3.0) in your python library. 

If some domain don't allow you to download the files, please let me know.

This has only been tested on version 3.5.1 of python.

If the japanese character aren't showing properly in the logs, set your system locale to japanese, or simply use 
a better text editor ( like [Notepad++](https://notepad-plus-plus.org/) ).


There will probably many things still to be implemented, so I count with everyone to state errors and what is left.


## To-do list

* Check if the url contains a webm (video) file.

* Better logging.

## Installing Praw
Praw is easily installed using [pip](https://pypi.python.org/pypi/pip)

> `pip install praw`

For more details please visit the Praw website.

### Useful links

* [Python](https://www.python.org/)

* [Using pip on windows](http://stackoverflow.com/questions/4750806/how-to-install-pip-on-windows)
