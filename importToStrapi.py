import os
import requests
import json

# CONFIG

videoFolder = "public/videos/"

# END CONFIG

urlGraphQL = ""
accessToken = ""


def booleanToString(bool):
    return "true" if bool else "false"


def query(query, variables={}, operationName=None):

    data = {
        "query": query,
        "variables": variables,
    }

    if operationName:
        data["operationName"] = operationName

    command = []
    command += ["curl --request POST -s"]
    command += ["--url " + urlGraphQL]
    command += ["--header 'Authorization: Bearer " + accessToken + "'"]
    command += ["--header 'Content-Type: application/json'"]
    command += ["--data '" + json.dumps(data) + "'"]

    command = " ".join(command)
    # print(command)
    ret = os.popen(command)
    return ret.read()


with open(".env.local", "r") as configFile:
    for line in configFile.readlines():
        if line.startswith("URL_GRAPHQL="):
            urlGraphQL = line[len("URL_GRAPHQL="):-1]
        elif line.startswith("ACCESS_TOKEN="):
            accessToken = line[len("ACCESS_TOKEN="):-1]
data = {}

previousUid = ""
for file in sorted(os.listdir(videoFolder)):
    uid = file.split(".")[0]
    extension = file.split(".")[1:]
    if uid != previousUid:
        previousUid = uid
        data[uid] = {
            "thumbnail": False,
            "video": False,
            "info": False,
            "live_chat": False,
            "gone": False,
            "title": "",
            "description": "",
            "published_date": {
                "year": 1970,
                "month": 0,
                "day": 0
            },
            "channel": {
                "uid": "",
                "title": "",
                "subscribers": ""
            },
            "categories": [],
            "views": 0,
            "likes": 0,
            "width": 0,
            "height": 0,
            "duration": 0,
            "audio_languages": [],
            "subs_languages": [],
            "source": "YouTube"
        }
    if len(extension) == 0:
        print("Unexpected file", file)
    elif len(extension) == 1:
        if extension[0] == "webp":
            data[uid]["thumbnail"] = True
        elif extension[0] == "mp4":
            data[uid]["video"] = True
        else:
            print("Unexpected file", file)
    elif len(extension) == 2:
        if extension[0] == "info" and extension[1] == "json":
            data[uid]["info"] = True
        elif extension[0] == "live_chat" and extension[1] == "json":
            data[uid]["live_chat"] = True
        elif extension[1] == "vtt":
            data[uid]["subs_languages"] += [extension[0]]
        else:
            print("Unexpected file", file)


for uid in data:
    print(uid)

    archive = data[uid]
    if not archive["thumbnail"]:
        print("Missing thumbnail for", uid)
    if not archive["video"]:
        print("Missing video for", uid)
    if not archive["info"]:
        print("Missing info for", uid)

    with open(videoFolder + uid + ".info.json", "r") as jsonFile:
        info = json.loads(jsonFile.read())
        archive["title"] = info["title"].replace("'", "’")
        archive["description"] = info["description"].replace("'", "’")
        archive["views"] = info["view_count"]
        archive["likes"] = info["like_count"] if "like_count" in info else 0
        archive["width"] = info["width"]
        archive["height"] = info["height"]
        archive["duration"] = info["duration"]
        archive["published_date"]["year"] = int(info["upload_date"][:4])
        archive["published_date"]["month"] = int(info["upload_date"][4:6])
        archive["published_date"]["day"] = int(info["upload_date"][6:8])
        archive["channel"]["uid"] = info["channel_id"]
        archive["channel"]["title"] = info["channel"]
        archive["channel"]["subscribers"] = info["channel_follower_count"] if "channel_follower_count" in info else 0

    # Create the Channel

    createVideoChannel = '''
        mutation {
            createVideoChannel(
                data: { 
                    uid: "''' + archive["channel"]["uid"] + '''"
                    title: "''' + archive["channel"]["title"] + '''"
                    subscribers: ''' + str(archive["channel"]["subscribers"]) + '''
                }
            ) {
                data {
                    id
                }
            }
        }
    '''

    query(createVideoChannel, {}, "")

    # Retrieve Channel ID
    getVideoChannel = '''
        query getVideoChannel($uid: String) {
            videoChannels(filters: { uid: { eq: $uid } }) {
                data {
                    id
                }
            }
        }
    '''

    res = query(getVideoChannel, {
        "uid": archive["channel"]["uid"]}, "getVideoChannel")
    res = json.loads(res)
    channelId = res["data"]["videoChannels"]["data"][0]["id"]

    # Create Video
    createVideo = \
        '''
mutation {
createVideo(data: {
uid: "''' + uid + '''"
title: ''' + json.dumps(archive["title"]) + '''
published_date: {
year: ''' + str(archive["published_date"]["year"]) + '''
month: ''' + str(archive["published_date"]["month"]) + '''
day: ''' + str(archive["published_date"]["day"]) + '''
}
channel: ''' + channelId + '''
views: ''' + str(archive["views"]) + '''
likes: ''' + str(archive["likes"]) + '''
width: ''' + str(archive["width"]) + '''
height: ''' + str(archive["height"]) + '''
duration: ''' + str(archive["duration"]) + '''
source: ''' + archive["source"] + '''
gone:  ''' + booleanToString(archive["gone"]) + '''
live_chat: ''' + booleanToString(archive["live_chat"]) + '''
description: ''' + json.dumps(archive["description"]) + '''
}) {
data {
id
}
}
}'''
    # print(createVideo)

    res = query(createVideo)
    if ("This attribute must be unique" not in res):
        print(uid, res)


    # exit()
