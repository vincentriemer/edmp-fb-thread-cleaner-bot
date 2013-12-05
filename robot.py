# The MIT License (MIT)

# Copyright (c) 2013 Vincent Riemer

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import praw, time, ConfigParser
from optparse import OptionParser

USERAGENT = "Edmproduction Feedback Thread Cleaner | a bot by /u/BizCaus"

# Config
parser = OptionParser()
parser.add_option("-c", "--config", dest="conf_path", type="string", help="config file path")
(options, args) = parser.parse_args()

config = ConfigParser.RawConfigParser()
config.readfp(open(options.conf_path))
USERNAME = config.get("feedbackcleaner", "username")
PASSWORD = config.get("feedbackcleaner", "password")
SUBREDDIT = config.get("feedbackcleaner", "subreddit")

r = praw.Reddit(USERAGENT)
r.login(USERNAME,PASSWORD)

# Gets all the comments (including the comments contained within a MoreComments object)
def getAllComments(input):
	comment_list = []
	if isinstance(input, praw.objects.Comment):
		for c in input.replies:
			if isinstance(c, praw.objects.MoreComments):
				comment_list.extend(getAllComments(c))
			else:
				comment_list.append(c)
	else:
		for c in input.comments:
			if isinstance(c, praw.objects.MoreComments):
				comment_list.extend(getAllComments(c))
			else:
				comment_list.append(c)
	return comment_list

# Check to see if user has replied to any other comments in the same thread
def hasGivenFeedback(username, thread):
	for root_comment in getAllComments(thread):
		# Check all comments one level past the root level
		for leaf in getAllComments(root_comment):
			if leaf.author.user_name == username:
				return True
	return False

# Determine whether or not the user of the comment is useless and if so, delete the comment
def cleanComment(comment,thread):	
	if time.time() - comment.created_utc > 3600: # 3600 seconds = 1 hour
		if not hasGivenFeedback(comment, thread):			
			print "removed " + comment.author.name + "'s comment in " + thread.title
			comment.remove()
		else:
			print "did not remove " + comment.author.name + "'s comment in " + thread.title

# Filter threads to only include the feedback threads
def cleanThreads(threads):
	for thread in threads:
		thread_title = thread.title			
		if thread_title.startswith('Feedback Thread'):
			print("cleaning " + thread_title + "..."),
			for comment in getAllComments(thread):
				cleanComment(comment,thread)
			print("done!")

# Main bot loop
running = True
while running:
	print "=================================="
	print "running cleaning pass on " + time.asctime(time.localtime(time.time())) + "..."
	subreddit = r.get_subreddit(SUBREDDIT)
	threads = subreddit.get_new()
	cleanThreads(threads)
	print "cleaning pass completed"
	time.sleep(3600)
