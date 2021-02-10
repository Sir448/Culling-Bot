import praw
import time
from datetime import datetime
import json
import os
from os.path import join, dirname
from dotenv import load_dotenv

# time allowed since last posting in seconds
# 864000 seconds is 10 days
lastActive = 864000

mods = ["blackat_chemical"]

now = time.time()
activeUsers = []
activeFlairs = []
culled = []

rootdir = os.path.dirname(os.path.abspath(__file__))

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
password = os.getenv("PASSWORD")
username = os.getenv("USER")

reddit = praw.Reddit(client_id=client_id,client_secret = client_secret, password = password, username = username, user_agent="testscript by u/SirAwesome789")


# Loads previously active users list
try:
    with open('activeUsers.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    data = {"activeUsers": []}


# Creates list of active users based on who has created posts recently
for submission in reddit.subreddit("edefine").new(limit = None):
    if submission.created_utc < now - lastActive:
        break
    elif len(activeUsers) == 0 and submission.author.name not in mods:
        # print(submission.author.name, submission.author_flair_text)
        activeUsers.append(submission.author.name)
        activeFlairs.append(int(submission.author_flair_text))
    elif submission.author.name not in activeUsers and submission.author.name not in mods:
        # print(submission.author.name, submission.author_flair_text)
        for i in range(len(activeFlairs)):
            if activeFlairs[i] > int(submission.author_flair_text):
                activeFlairs.insert(i,int(submission.author_flair_text))
                activeUsers.insert(i,submission.author.name)
                break
        else:
            activeUsers.append(submission.author.name)
            activeFlairs.append(int(submission.author_flair_text))

# Adds to list based on who has commented recently
for comment in reddit.subreddit("edefine").comments(limit = None):
    if comment.created_utc < now - lastActive:
        break
    elif len(activeUsers) == 0 and comment.author.name not in mods:
        # print(comment.author.name, comment.author_flair_text)
        activeUsers.append(comment.author.name)
        activeFlairs.append(int(comment.author_flair_text))
    elif comment.author.name not in activeUsers and comment.author.name not in mods:
        # print(comment.author.name, comment.author_flair_text)
        for i in range(len(activeFlairs)):
            if activeFlairs[i] > int(comment.author_flair_text):
                activeFlairs.insert(i,int(comment.author_flair_text))
                activeUsers.insert(i,comment.author.name)
                break
        else:
            activeUsers.append(comment.author.name)
            activeFlairs.append(int(comment.author_flair_text))


# # Removes the inactive
# # One is for if there is no list of active users from the previous culling, the other is for if there is
# if not os.path.exists("activeUsers.json"):
#     contributors = reddit.subreddit("edefine").contributor()
#     for contributor, i in zip(contributors,range(len(contributors))):
#         if contributor not in activeUsers and contributor not in mods:
#             # reddit.subreddit("edefine").contributor.remove(contributor)
#             culled.append(contributor.name)
# else:
#     for contributor, i in zip(data["activeUsers"],range(len(data["activeUsers"]))):
#         if contributor not in activeUsers and contributor not in mods:
#             # reddit.subreddit("edefine").contributor.remove(contributor)
#             culled.append({"name":contributor,"number":i+1})



# # Sets flairs
# # for i in range(len(activeFlairs)):
#     # reddit.subreddit("edefine").flair.set(activeUsers[i],str(i+1))
#     # print(activeUsers[i], activeFlairs[i],"->",i+1)



# # Creates submissions saying who was culled and who survived
# if os.path.exists("activeUsers.json"):
#     message = str(culled[0]['number'])+": "+culled[0]['name']

#     for user in culled[1:]:
#         message += "\n\n{}: {}".format(user['number'],user['name'])

# else:
#     message = culled[0]
#     for user in culled[1:]:
#         message +="\n\n"+user

# # print(message)
# # reddit.subreddit("edefine").submit("The Culled", selftext = message)

# message = "1: "+activeUsers[0]

# for i in range(1,len(activeUsers)):
#     message += "\n\n{}: {}".format(i+1,activeUsers[i])

# # print(message)
# # reddit.subreddit("edefine").submit("Survivors", selftext = message)


# # Records current active users at time of culling
# # data['activeUsers'] = activeUsers
# # data['mods'] = mods

# # with open('activeUsers.json', 'w') as file:
# #         json.dump(data, file, indent = 4)


# # Creates Active User and Culling Logs
# text = time.ctime(time.time())+"\nMods:"
# for mod in mods:
#     text+=" "+mod
# for i in range(len(activeUsers)):
#     text += "\n{}: {}".format(i+1,activeUsers[i])

# if not os.path.exists("ActiveUsersLogs"):
#     os.mkdir(os.path.join(rootdir,"ActiveUsersLogs"))
#     print("ActiveUsersLogs directory created")

# with open('ActiveUsersLogs/Active Users {}.txt'.format(1+len(os.listdir(os.path.join(rootdir,"ActiveUsersLogs")))),'a') as file:
#     file.write(text)
    


# text = time.ctime(time.time())
# if os.path.exists('activeUsers.json'):
#     for user in culled:
#         text += "\n{}: {}".format(user['number'],user['name'])
# else:
#     for user in culled:
#         text += "\n"+user

# if not os.path.exists("CullingLogs"):
#     os.mkdir(os.path.join(rootdir,"CullingLogs"))
#     print("CullingLogs directory created")

# with open('CullingLogs/Culled {}.txt'.format(1+len(os.listdir(os.path.join(rootdir,"CullingLogs")))),'a') as file:
#     file.write(text)