#!/usr/bin/python3

import sys
from datetime import *
from pprint import *

out_of_project_files = "/home/akbkuku/.youtube/"

sys.path.append("/home/akbkuku/.youtube")
from youtubeanalyticsapi import YTAnalytics
from youtubedataapi import YTData
from apikey import GoogleAPIKey
from videodata import VideoData

def determine_demonetized(videos,threshold):
    bad_videos = [[],[],[]];
    for video in videos:
        video.confidence = video.views / views_for_confidence
        if video.percent < threshold:
            if video.confidence > 1.0:
                bad_videos[0].append(video)
            elif video.confidence > 0.5:
                bad_videos[1].append(video)
            else:
                bad_videos[2].append(video)

    return bad_videos

def print_video(video):
        print("Video \"" + video.title + "\" is at " + str(video.percent*100) + "% (" + str(int(video.monetizedPlaybacks)) + "/" + str(int(video.views)) + ") monetized views") 
        print(youtube_edit_link + video.id) 

m = YTAnalytics.Metrics()

views_for_confidence = 25
days = 2
threshold = 0.1

youtube_edit_link = "https://www.youtube.com/edit?o=U&video_id="

# Setup APIs
api = GoogleAPIKey()
ytd = YTData()
ytd.set_client(api.get_client_id(),api.get_client_secret())

yta = YTAnalytics()
yta.set_client(api.get_client_id(),api.get_client_secret())

# Connect APIs
ytd.connect()
yta.connect()

ytd.set_channel_id(api.channel_id)
yta.set_channel_id(api.channel_id)

videos = ytd.get_video_list()


for video in videos:
    yta.get_metrics(
            date.today()-timedelta(days),
            date.today()-timedelta(1),
            [m.views,m.monetizedPlaybacks],
            video
    )

bad_videos = determine_demonetized(videos,threshold)

if len(bad_videos[0]):
    print("High Confidence of Demonetiztion:")
    for bv in bad_videos[0]:
        print_video(bv)
    print()

if len(bad_videos[1]):
    print("Medium Confidence of Demonetiztion:")
    for bv in bad_videos[1]:
        print_video(bv)
    print()

if len(bad_videos[2]):
    print("Low Confidence of Demonetiztion:")
    for bv in bad_videos[2]:
        print_video(bv)
    print()
