# EDMP Feedback Thread Cleaner Bot

### Description

Forever has the constructive "Feedback Thread" alluded most creative communites on the internet; degrating into pits where desperate creatives dump their work and leave before assesing anyone else's work. Some communites established rules on **needing** to give feedback to someone else before they could post their own work, but this asked a lot of the admins and spammers still slipped through the cracks.

That's where this bot comes in. Created for the subreddit I moderate, [r/edmproduction](http://www.reddit.com/r/edmproduction), this script aims to automatically delete comments on the weekly posted feedback threads which have not given someone else in the thread feedback in a pre-determined amount of time (lets assume 1 hour). While right now this script has been made primarily for the edmproduction subreddit, I hope to generalize the code enough to make it easy for any creative subreddit which has "feedback threads" to use this bot on their threads.

### Installation & Usage

Just clone the github repository using the following command:

	$ git clone https://github.com/vincentriemer/edmp-fb-thread-cleaner-bot.git

The script requires the [PRAW](https://praw.readthedocs.org/en/latest/) package and has been tested on Python 2.7.5.

Before running you must make sure you also create a configuration file named config.cfg. The configuration file must follow the following structure:

	[feedbackcleaner]
	username = myAwesomeRedditBotUsername
	password = myAwesomeRedditBotPassword
	timethreshold = myPostRemovalTimeThreshold

Launch the script using the following command in the terminal:

	$ python robot.py -c config.cfg

As of the time of writing this documentation, the line of code that actually bans the comments from reddit has been commented out...

	# comment.remove() # UNCOMMENT TO ENABLE COMMENT REMOVALS

...and just prints the results to the terminal. When you are confident enough that you've properly configured the script, uncomment the code.