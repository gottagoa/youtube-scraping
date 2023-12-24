from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns
import requests 

api_key='AIzaSyDSAUN47KPLLQ93rNwA6iekVYUWdoeMSsY'
channel_id='UCnz-ZXXER4jOvuED5trXfEA'

youtube=build('youtube', 'v3', developerKey=api_key)
# Function to get channel statistics

def get_channel_stats(youtube, channel_id):
    request=youtube.channels().list(
        part='snippet, contentDetails, statistics',
        id=channel_id)
    
    response=request.execute()
    data=dict(Channel_name= response['items'][0]['snippet']['title'],
              Subscribers=response['items'][0]['statistics']['subscriberCount'],
              Views=response['items'][0]['statistics']['viewcount'],
              Total_videos=response['items'][0]['statistics']['videoCount'])

    return data