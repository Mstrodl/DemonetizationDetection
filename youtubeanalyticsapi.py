#!/usr/bin/python3

import types
from pprint import pprint

from googleapi import GoogleAPIBase
from videodata import VideoData


class YTAnalytics(GoogleAPIBase):

    class Metrics:
        estimatedRevenue = "estimatedRevenue" , VideoData.estimatedRevenue
        estimatedMinutesWatched="estimatedMinutesWatched" , VideoData.estimatedMinutesWatched
        monetizedPlaybacks = "monetizedPlaybacks" , VideoData.monetizedPlaybacks
        views = "views" , VideoData.views

    m  = None

    channel_id = None


    def __init__(self):
        self.set_api(
                name = "youtubeAnalytics",
                version = "v1",
        )
        self.add_scope("https://www.googleapis.com/auth/yt-analytics.readonly")
        self.add_scope("https://www.googleapis.com/auth/yt-analytics-monetary.readonly")
        self.m = self.Metrics() 


    def set_channel_id(self,channel_id):
        self.channel_id = channel_id


    def execute_query(self,start,end,metrics,video=None):
        if video.id == None:
            filters = ""
        else:
            filters = "video==" + video.id
        
        
        return self.service.reports().query(
            ids="channel=="+self.channel_id,
            filters=filters,
            metrics=metrics,
            start_date=start.strftime("%Y-%m-%d"),
            end_date=end.strftime("%Y-%m-%d")
            ).execute()

    def get_metrics(self,start,end,metrics,video):
        if end == None:
            end = start
        
        metricString = ""

        for m in metrics:
            metricString += m[0] + ","
        
        metricString = metricString[:-1]

        result = self.execute_query(start,end,metricString,video)

        for row in result.get("rows", []):
            for i , value in enumerate(row):
                types.MethodType(metrics[i][1].fset,video)(value)

        return video

    def get_monetizedPlaybacks(self,start,end=None,video=None):
        if end == None:
            end = start

        result = self.execute_query(start,end,self.m.monetizedPlaybacks[0],video)

        for row in result.get("rows", []):
            for value in row:
                return value

        return -1


    def get_views(self,start,end=None,video=None):
        if end == None:
            end = start

        result = self.execute_query(start,end,self.m.views,video)

        for row in result.get("rows", []):
            for value in row:
                return value

        return -1


    def get_revenue(self,start,end=None,video=None):
        if end == None:
            end = start

        result = self.execute_query(start,end,self.m.estimatedRevenue[0],video)

        for row in result.get("rows", []):
            for value in row:
                return value

        return -1


    def get_watchtime(self,start,end=None):
        if end == None:
            end = start

        result = self.execute_query(start,end,self.m.estimatedMinutesWatched[0])

        for row in result.get("rows", []):
            for value in row:
                return value / 60.0

        return -1

