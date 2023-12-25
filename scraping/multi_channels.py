from googleapiclient.discovery import build
import pandas as pd
from tabulate import tabulate
import seaborn as sns
import requests 

api_key='AIzaSyBFgk8_mYSU7TR6967YDWcP3josi5Kyh6w'
channel_ids=['UCnz-ZXXER4jOvuED5trXfEA',
             'UCLLw7jmFsvfIVaUFsLs8mlQ',
             'UCiT9RITQ9PW6BhXK0y2jaeg',
             'UC7cs8q-gJRLGwj4A8OmCmXg',
             'UC2UXDak6o7rBm23k3Vv5dww']


youtube=build('youtube', 'v3', developerKey=api_key)
# Function to get channel statistics

def get_channel_stats(youtube, channel_ids):
    all_data=[]
    request=youtube.channels().list(
        part='snippet, contentDetails, statistics',
        id=','.join(channel_ids))
    
    response=request.execute()
    for i in range(len(response['items'])):
        data=dict(Channel_name= response['items'][i]['snippet']['title'],
                  Subscribers=response['items'][i]['statistics']['subscriberCount'],
                  Views=response['items'][i]['statistics']['viewCount'],
                  Total_videos=response['items'][i]['statistics']['videoCount'],
                  playlist_id=response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
        all_data.append(data)
    return all_data

channel_statistics=get_channel_stats(youtube, channel_ids)
channel_data=pd.DataFrame(channel_statistics)
# print(channel_data)
# print(channel_statistics)
# channel_data['Subscribers']=pd.to_numeric(channel_data['Subscribers'])
# channel_data['Views']=pd.to_numeric(channel_data['Views'])
# channel_data['Total_videos']=pd.to_numeric(channel_data['Total_videos'])
print(channel_data)
# sns.set(rc={'figure.figsize':(10,8)})
# ax=sns.barplot(x='Channel_name', y='Subscribers', data=channel_data)
# показывает в виде графика у кого больше всего подписчиков
# # print(ax)

# playlist_id=channel_data.loc[channel_data['Channel_name']]
#  function ti get video ids

def get_video_ids(youtube, playlist_id):
    request=youtube.playlistItems().list(
        part='contentDetails',
        playlist_id=playlist_id,
        maxResults=50)
    
    response=request.execute()
    return response

print()