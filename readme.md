# EDMP Feedback Thread Cleaner Bot

### Description

Forever has the constructive "Feedback Thread" alluded most creative communites on the internet; degrating into pits where desperate creatives dump their work and leave before assesing anyone else's work. Some communites established rules on **needing** to give feedback to someone else before they could post their own work, but this asked a lot of the admins and spammers still slipped through the cracks.

That's where this bot comes in. Created for the subreddit I moderate, [r/edmproduction](http://www.reddit.com/r/edmproduction), this script aims to automatically delete comments on the weekly posted feedback threads which have not given someone else in the thread feedback in a pre-determined amount of time (lets assume 1 hour). While right now this script has been made primarily for the edmproduction subreddit, I hope to generalize the code enough to make it easy for any creative subreddit which has "feedback threads" to use this bot on their threads.

### Installation & Usage

Just clone the github repository to get the script's source:

	$ git clone https://github.com/vincentriemer/edmp-fb-thread-cleaner-bot.git

The script requires the [PRAW](https://praw.readthedocs.org/en/latest/) package and has been tested on Python 2.7.5.

Before running you must make sure you also create a configuration file named config.cfg. The configuration file must follow the following structure:

	[feedbackcleaner]
	username = myAwesomeRedditBotUsername
	password = myAwesomeRedditBotPassword
	timethreshold = myPostRemovalTimeThreshold
    notificationsubject = Your comment has been removed from #{thread_name}
    notificationmessage = Hello #{user},\n\nYour following comment has been automatically removed:\n\n#{comment}\n\nThis is because you have not given feedback to any other users in the thread within 1 hour of posting your material for feedback. If you wish to have your comment restored, please give feedback to another user's material on the same thread and I will restore your comment as soon as possible.

Launch the script using the following command in the terminal:

	$ python robot.py -c config.cfg
