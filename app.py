### Turn this into a pipeline/flask app which when called will do the following.
#
### Take inputs from users, account description, no of posts, time interval between the posts and
### post ideas(optional). It will feed those into the functions we will import from the
### caption_generation.py file. Then the caption will be extracted and the image prompt will be fed into
### the image_generation.py functions. Now we will have the image caption pairs.
#
### We will create the job for the time interval for which we need to post each post. We will iterate
### through the image caption pairs and call the job() function from the posting_to_ig.py file with the
### new image caption pair everytime.
#
### The expected result is an instagram image post with proper captions and hashtags posted at the
### predefined interval





import schedule
import time

from posting_to_ig import job

schedule.every(10).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
