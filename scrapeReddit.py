import time
import requests
from bs4 import BeautifulSoup as BSoup
import pandas as pd
from itertools import chain
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""
Scrapes comment data from weekly top N posts in a subreddit
"""

class Scrape:
    def __init__(self, subreddit, numOfPosts):
        self.numOfPosts = int(numOfPosts)
        driver.get(f"https://old.reddit.com/r/{subreddit}/top/?sort=top&t=month")
        self.getComments()
        driver.close()
        

    def getComments(self):
        try:
            commentsArr = []
            i = 0
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "siteTable")))
            nextPage = True
            postLinks = []
            while(nextPage and i < self.numOfPosts):
                time.sleep(1)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "siteTable")))
                self.bs_obj = BSoup(driver.page_source, 'html.parser')
                postDivs = self.bs_obj.find(id='siteTable').find_all("div", class_="link")
                
                for j in range(len(postDivs)):
                    if "promoted" in postDivs[j].attrs["class"]:
                        continue
                    link = postDivs[j].find("a", class_="comments").attrs["href"]
                    postLinks.append(link)
                    i+=1
                
                nextPage = self.nextPage()
                    
            for j in range(len(postLinks)):
                commentsArr.append(self.getPostComments(postLinks[j]))
            df = pd.DataFrame(list(chain.from_iterable(commentsArr)))
            df.to_csv("comments.csv", index=False)
        
        except Exception as e:
            print(e)
            raise e
        
        

    def getPostComments(self, link):
        driver.get(link.replace("re", "un", 1))
        input = driver.find_element(By.ID, "maxComments")
        select = Select(driver.find_element(By.ID,"commentFilter"))
        select.select_by_value("SHOW_ALL")
        input.send_keys("20000")
        input.send_keys(Keys.ENTER)
        driver.get(link.replace("re", "un", 1))
        try:
            while True:
                WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "status-text")))
                time.sleep(2)
        except Exception as e:
         print("loaded")
        
        bs_obj = BSoup(driver.page_source, 'html.parser')
        comments = []
        commentDivs = bs_obj.find_all("div", class_="comment")
        linkTag = link.split("/")[-3]
        for div in commentDivs:
            comment = {}
            classes = div.attrs["class"]
            comment["postTag"] = linkTag
            comment["user"] = div.find("a", class_="author").attrs["href"] if "href" in div.find("a", class_="author").attrs else "nan"
            comment["comment_score"] = div.find("span", class_="comment-score").get_text().split(" ")[0]
            comment["comment_body"] = div.find("div", class_="comment-body").get_text()
            comment["mod_deleted"] = 1 if "removed" in classes else 0
            comment["user_deleted"] = 1 if "deleted" in classes else 0
            comments.append(comment)
        return comments

    def nextPage(self):
        try:
            nextButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "next-button")))
            if "paginate_button_disabled" in nextButton.get_attribute('class'):
                return False
            nextButton.click()
        except Exception as e:
            return False
        return True
    
def getUserInfo():
    info = {}
    df = pd.read_csv('comments.csv')
    max = len(df) - 1
    i = 0
    usersDict = {}
    users = df['user'].apply(lambda x: x.split("/")[-1] if type(x) is not float else None)
    keys = ["verified", "is_gold", "has_verified_email", "link_karma", "total_karma", "created_utc", "comment_karma"]
    for key in keys:
        info[key] = []
    for user in users:
        print(f"{i}/{max}")
        if user is None:
            for key in keys:
                info[key].append(None)
            i = i + 1
            continue
        data = {}
        if user in usersDict:
            data = usersDict[user]
        else:
            time.sleep(.25)
            url = f"https://www.reddit.com/user/{user}/about.json"
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'})
            if r.status_code == 200:
                data = r.json()["data"]
                usersDict[user] = data
            else:
                print(f"Status code: {r.status_code}, {url}")
                for key in keys:
                    info[key].append(None)
                i = i + 1
                continue
        data_keys = list(data.keys())
        for key in keys:
            if key in data_keys:
                val = data[key]
                info[key].append(val)
            else:
                info[key].append(None)
        i = i + 1
    for key in keys:
        df[key] = info[key]
    df.to_csv("comments_full.csv", index=False)



subreddit = input("Name of subreddit: ")
n = input("Number of posts to scrape: ")
driver = webdriver.Chrome()

scrape = Scrape(subreddit, n)

getUserInfo()