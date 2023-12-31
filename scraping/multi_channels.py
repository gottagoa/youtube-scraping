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
# print(channel_data)
# sns.set(rc={'figure.figsize':(10,8)})
# ax=sns.barplot(x='Channel_name', y='Subscribers', data=channel_data)
# показывает в виде графика у кого больше всего подписчиков
# # print(ax)

playlist_id=channel_data.loc[channel_data['Channel_name']=='Ken Jee', 'playlist_id'].iloc[0]
#  function ti get video ids

def get_video_ids(youtube, playlist_id):
    request=youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50)
    
    response=request.execute()

    video_ids=[]

    for i in range((len)(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])
    next_page_token=response.get('nextPageToken')
    more_pages=True
        # добавляем новую переменную? чтобы определить, есть ли еще страницы, для определения
        # используется токен страницы
    while more_pages:
        if next_page_token is None:
            more_pages=False
        else:
            # делается дополнительный запрос на получение 
            request=youtube.playlistItems().list(
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token)
            response=request.execute()

            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])
            next_page_token=response.get('nextPageToken')

    return video_ids

video_ids=get_video_ids(youtube, playlist_id)
# print(video_ids)

# function to get video details
def get_video_details(youtube, video_ids):

    all_video_stats=[]
    for i in range(0, len(video_ids), 50):
        # тк при итерации можно использовать только 50 id,
        # то при каждой итерации будут браться по 50 id
        # т.е. при первой итерации i=0 (начинается с 0) и i+50=50
        # при второй итерации i=50, i+50=100 и тд до конца
        request=youtube.videos().list(
                    part='snippet,statistics',
                    id=','.join(video_ids[i:i+50]))
        response=request.execute()
        # делаем второй цикл, чтоб из 50 видео получить информацию о каждом
        for video in response['items']:
            video_stats=dict(Title=video['snippet']['title'],
                            Published_date=video['snippet']['publishedAt'],
                            Views=video['statistics']['viewCount'],
                            Likes=video['statistics']['likeCount'],
                            Dislikes=video['statistics'].get('dislikeCount', 0), # use get if not every video has dislike
                            Comments=video['statistics']['commentCount']
                            )
            all_video_stats.append(video_stats)
    return all_video_stats

video_details=get_video_details(youtube, video_ids)
video_data=pd.DataFrame(video_details)
# модификация данных в читабельный и удобный вид и создание колонн
video_data['Published_date']=pd.to_datetime(video_data['Published_date']).dt.date
video_data['Views']=pd.to_numeric(video_data['Views'])
video_data['Likes']=pd.to_numeric(video_data['Likes'])
video_data['Dislikes']=pd.to_numeric(video_data['Dislikes'])
# video_data['Views']=pd.to_numeric(video_data['Views'])

# identify top-10 viwable videos
top10_videos=video_data.sort_values(by='Views', ascending=False)
ax1=sns.barplot(x='Views', y='Title', data=top10_videos)
# print(top10_videos)

# every month how many videos has reposted
video_data['Month']=pd.to_datetime(video_data['Published_date']).dt.strftime('%b')
videos_per_month=video_data.groupby('Month', as_index=False).size()
# strftime-month date
# print(videos_per_month)

# going to sort by months and index. index will represented by month
sort_order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

videos_per_month.index=pd.CategoricalIndex(videos_per_month['Month'], categories=sort_order, ordered=True)
videos_per_month=videos_per_month.sort_index()
print(videos_per_month)

# finding out on seaborn diagram
ax2=sns.barplot(x='Month', y='size', data=videos_per_month)

# exporting to csv file
video_data.to_csv('Video_Details(KenJee).csv')