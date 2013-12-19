import praw, time, ConfigParser, pprint
from optparse import OptionParser

USERAGENT = "Reddit Feedback Thread Cleaner | a bot by /u/BizCaus"

# Config
parser = OptionParser()
parser.add_option("-c", "--config", dest="conf_path", type="string", help="config file path")
(options, args) = parser.parse_args()

config = ConfigParser.RawConfigParser()
config.readfp(open(options.conf_path))
USERNAME = config.get("feedbackcleaner", "username")
PASSWORD = config.get("feedbackcleaner", "password")
TIME_THRESHOLD = int(config.get("feedbackcleaner", "timethreshold")) # this is in seconds
NOTIFICATION_SUBJECT = config.get("feedbackcleaner", "notificationsubject")
NOTIFICATION_MESSAGE = config.get("feedbackcleaner", "notificationmessage").decode('string_escape')

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

# Notify the user by comment that their post has been removed with
# the reason why it was removed.
def notifyUser(comment,thread):
    # Prepare message by replacing specific keywords
    subject = NOTIFICATION_SUBJECT.replace("#{thread_name}",thread.title)
    message = NOTIFICATION_MESSAGE.replace("#{user}",comment.author.name).replace("#{comment}",comment.permalink).replace("#{thread}",thread.url)
    # Send the message
    r.send_message(comment.author.name,subject,message)

# Check to see if user has replied to any other comments in the same thread
def hasGivenFeedback(username, thread):
    for root_comment in getAllComments(thread):
        # Check all comments one level past the root level
        for leaf in getAllComments(root_comment):
            if leaf.author != None and leaf.author.name == username:
                return True
    return False

# Determine whether or not the user of the comment is useless and if so, delete the comment
def cleanComment(comment,thread):
    if comment.banned_by == None:
        if time.time() - comment.created_utc > TIME_THRESHOLD:
            if not hasGivenFeedback(comment.author.name, thread):
                print "removed " + comment.author.name + "'s comment in " + thread.title
                notifyUser(comment,thread)
                comment.remove()
            else:
                print "did not remove " + comment.author.name + "'s comment in " + thread.title
    else:
        if hasGivenFeedback(comment.author.name, thread):
            print "approved " + comment.author.name + "'s comment in " + thread.title
            comment.approve()

# Filter threads to only include the feedback threads
def cleanThreads(threads):
    for thread in threads:
        thread_title = thread.title
        if thread_title.startswith('Feedback Thread'):
            print("cleaning " + thread_title + "...")
            # Clean all the root comments
            for comment in getAllComments(thread):
                if not comment.author == None:
                    cleanComment(comment,thread)
            return # only clean the latest feedback thread

# Main bot loop
running = True
while running:
    print "=================================="
    print "running cleaning pass on " + time.asctime(time.localtime(time.time())) + "..."
    # bot = r.get_redditor(USERNAME)
    # threads = bot.get_submitted()
    threads = [r.get_submission("http://www.reddit.com/r/edmseduction/comments/1mgqsu/feedback_thread_september_16/")]
    cleanThreads(threads)
    print "cleaning pass completed"
    time.sleep(TIME_THRESHOLD / 10)
