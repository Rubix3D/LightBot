import praw
import time
import os
from PIL import Image
import urllib

def authenticate():
    print("Authenticating...")
    r = praw.Reddit('LightBot', user_agent = "LightBot By Rubix")
    print("Authenticated as {}".format(r.user.me()))
    return r
 
def main():
    r = authenticate()
    comments_replied_to = get_saved_comments()
    while True:
        run_bot(r, comments_replied_to)
        time.sleep(120)
        
def get_saved_comments():
    if not os.path.isfile("comments.txt"):
        comments_replied_to = []
    else:
        with open("comments.txt", "r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
        return comments_replied_to

def run_bot(r, comments_replied_to):
    
    print("Grabbing Subreddit...")
    
    for post in r.subreddit('foundthelightmodeuser').new(limit=25):
        if str(post.url).endswith('.jpg'):
            try:
                response = urllib.request.urlopen(post.url)
            except:
                break
            img = response.read()
            with open(str(post.id)+'.jpg','wb') as f:
                f.write(img)
        
    
    im = Image.open(img)
    
    pixels = im.getdata()
    
    white_thresh = 230
    nwhite = 0
    
    for pixel in pixels:
        if pixel < white_thresh:
            nwhite += 1
            
    n = len(pixels)
    
    if (nwhite / float(n)) > 0.5:
        print("Found white image...")
        for submission in r.subreddit('foundthelightmodeuser').new(limit=25):
            if submission.id not in comments_replied_to:
                submission.reply("This photo is too white. SHUN THIS LIGHT MODE USER!")


if __name__ == '__main__':
    while True:
        try:
            main()
        except BaseException:
            time.sleep(5)