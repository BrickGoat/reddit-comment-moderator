# reddit-comment-moderator
- An Attempt at predicting whether a reddit commit will be deleted by moderators in a particular subreddit.

## Web Scraping
1. Download BeatifulSoup, Pandas, and Selenium  
2. Run `Python3 scrapeReddit.py`  
3. Enter subreddit name and the number of posts to scrape data from.  

## Data Folder
- Comment & user data from the top 40 posts from the past month in the PoliticalDiscussion, askScience, kanye, and socialism subreddits.

## Model notebook
- Data is cleaned within the file
- A model for each subreddit was obtained by searching through TfidfVectorizer & RidgeClassifier parameters.
  - Confusion matrices show no significant predictions of deleted comments. More deleted comment data will be collected to see if prediction improves. 
