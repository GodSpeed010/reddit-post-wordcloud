import requests
import pandas as pd
from requests.api import post
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import urllib.request
from PIL import Image
import numpy as np
import re
from urllib.parse import urljoin

ROOT_URL = 'https://oauth.reddit.com/'

#holds all the text data for the Reddit post and its comments
df = pd.DataFrame()

def main():
    headers = auth()

    post_url = input('Enter reddit post link: ')
    
    #get post data from API
    post_data = get_post_data(post_url, headers) 
    print('Retreived post data')
    
    #populate df with post and post's comment tree
    populate_df(post_data)
    print('Populated DataFrame with data')
    
    #generates the wordcloud using the DataFrame
    generate_wordcloud()
    print('Generated wordcloud')
    
    #generate wordcloud using the subreddit's header image
    if (img_mask := get_sub_img(post_url, headers)) is not None:
        generate_wordcloud(mask=img_mask)
        print('Generated word cloud using subreddit header image')

def get_post_data(post_url, headers):
    #get only the needed parts from the given url
    path = re.search(r'/(r/.+)$', post_url).group(1)

    #call the API to get the post data
    res = requests.get( urljoin(ROOT_URL, path) , headers=headers).json()    

    return res

def generate_wordcloud(mask=None):
    text = ''.join([x + ' ' for x in df['text'].values])
    
    if mask is None:
        wc = WordCloud(width=800, height=400)
        wc.generate_from_text(text)

        plt.figure(figsize=(20,10), facecolor='k') # set figure size and make border black
        plt.tight_layout(pad=0)
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        
        plt.savefig('wordcloud.png', format='png', facecolor='k')
    else:
        wc = WordCloud(mask=mask, width=800, height=400).generate_from_text(text)

        image_colors = ImageColorGenerator(mask)
        plt.figure(figsize=[20,10], facecolor='k')
        plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
        plt.axis("off")

        plt.savefig('img_wordcloud.png', format='png', facecolor='k')

def get_sub_img(post_url, headers):
    #get the subreddit name from the url
    subreddit = re.search(r'/(r/\w+/?)', post_url).group(1)
    
    api_endpoint = urljoin(ROOT_URL , urljoin(subreddit, 'about') )
    
    #API call for subreddit data
    res = requests.get(api_endpoint , headers=headers).json()
    
    if res['data']['icon_img'] == '':
        print('No header image found')
        return None
    
    #save the image
    urllib.request.urlretrieve(res['data']['icon_img'], "header_image.png")

    #open the image as a colored img array
    mask = np.array(Image.open("header_image.png").convert('RGB'))
    
    return mask

def populate_df(res):
    global df

    #append the post body to the DataFrame  
    df = df.append({
        'text': res[0]['data']['children'][0]['data']['selftext']
    }, ignore_index=True)

    #append all comments to the DataFrame
    for comment in res[1]['data']['children']:
        append_comments(comment)

def append_comments(reply):
    """Recursively populates the DataFrame with the Reddit post's comments"""

    global df

    #reply json does not have ['body'] sometimes. This prevents an error
    if 'body' not in reply['data']:
        return

    #append the reply to the df
    df = df.append({
        'text' : reply['data']['body']
    }, ignore_index=True)

    #the base case; end of branch
    if reply['data']['replies'] == '':
        return

    #recurse for each child
    for child in reply['data']['replies']['data']['children']:
        append_comments(child)

def auth():
    """Sets up script for interacting with Reddit API
        Returns the headers"""
    CLIENT_ID = 'client_id_here'
    SECRET_KEY = 'secret_key_here'

    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

    data = {
        'grant_type' : 'password',
        'username' : 'your_username_here',
        'password' : 'your_password_here'
    }

    headers = {'User-Agent': 'MyAPI/0.0.1'}

    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)

    TOKEN = res.json()['access_token']

    headers['Authorization'] = f'bearer {TOKEN}'

    return headers

main()