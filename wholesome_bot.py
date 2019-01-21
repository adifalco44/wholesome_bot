import time, tweepy, os, sys, requests
import json

def twitter_api():
    f = open("my_keys.txt","r+")
    lines_ = f.readlines()
    f.close()

    consumer_key=lines_[0].strip('\n')
    consumer_secret=lines_[1].strip('\n')
    access_token=lines_[2].strip('\n')
    access_token_secret=lines_[3].strip('\n')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

def download_image(url):
    file_name = url
    file_name=file_name.replace('/','_')
    file_name=file_name.split(':')[1]
    file_name='memes/{0}'.format(file_name)
    if os.path.exists(file_name)==False:
        request = requests.get(url,stream=True)
        if request.status_code == 200:
            print('Downloading {0}'.format(file_name))
            with open('memes/{0}'.format(file_name),'wb') as image:
                for chunk in request:
                    image.write(chunk)


### REPLY TO TWEET ###
def reply_with_image(url,uuid,at):
    api = twitter_api()
    file_name = url
    file_name=file_name.replace('/','_')
    file_name=file_name.split(':')[1]
    file_name='memes/{0}'.format(file_name)
    ### DOWNLOAD FILE ###
    if os.path.exists(file_name)==False:
        download_image(file_name)

    #api.update_with_media(filename='memes/{0}'.format(file_name),in_reply_to_status_id=uuid,status='@{0}'.format(at))

if __name__ == "__main__":

    api = twitter_api()

    ### GET MEMES AND SIFT THRU THEM FOR UNIQUE CONTENT ###
    user_obj = api.lookup_users(screen_names=['WholesomeMeme'])
    user_id = user_obj[0].id_str
    memes = api.user_timeline(id=user_id,count=100)
    trimmed_memes = []
    for meme in memes:
        if meme.in_reply_to_user_id_str==None and 'media' in meme.entities.keys():
            if meme.entities['media'][0]['media_url'] not in trimmed_memes:
                trimmed_memes.append(meme.entities['media'][0]['media_url'])
    for meme in trimmed_memes:
        download_image(meme)

    all_memes = os.listdir('memes')
    print(all_memes)

    ### SEARCH OVER DESIRED KEYWORDS ###
    query = ['sad','depressed']
    it = 0
    for i in range(0,len(query)-1):
        que = query[i].strip('\n')
        data = api.search(q=que,count=10000)

        ### ITERATE OVER TWEETS ###
        for status in data:
            if 'RT' not in status.text and '@' not in status.text and 'http' not in status.text:
                try:
                    print("{0}\n".format(status.text))
                    reply_status = input("To reply, press Y,\n To skip, press N\n")

                    ### REPLY OR DONT TO TWEETS ###
                    if (True):
                        print(status.id_str)
                        reply_with_image(all_memes[it%(len(all_memes))],status.id_str,status.user.screen_name)
                        print('Reply #{0}'.format(it))
                        it+=1
                    else:
                        print('Skipped tweet\n\n')
                except UnicodeEncodeError:
                    pass
