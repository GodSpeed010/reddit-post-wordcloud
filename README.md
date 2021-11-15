# reddit-post-wordcloud
A script that makes a word cloud of a Reddit post and its comments

## Description

This script interacts with the Reddit API, getting all the text data from a post, parsing it, and populating the data into a DataFrame. Next, a wordcloud is created, displayed, and saved as a .png image. A wordcloud in the shape of the subreddit's header icon will also do the same if found in the API request.

## Getting Started

### Dependencies

Python libraries: requests, pandas, wordcloud, matplotlib, urllib, Pillow, numpy

### Installing

* Create a Reddit Application to get the authorization required to interact with the Reddit API. You can follow this guide linked [here](https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c).
* Set your **CLIENT_ID**, **SECRET_KEY**, account **username**, and account **password** in the auth() function 

### Executing program

1. Run the script
2. Input the full url of the Reddit post when prompted

Example:
```
Enter reddit post link: https://www.reddit.com/r/Python/comments/qt3x3w/advanced_visual_studio_code_for_python_developers/
```
