import requests
import threading
from dhooks import Embed, Webhook
import datetime
import json
import tweepy
import random
import time

WebhookList = []

def get_t_name():
    threadname = threading.currentThread().getName()
    #threadname = str(threadname).replace('Thread-', 'Task ')
    return f'| {threadname} | {datetime.datetime.now()} |'

def mentionedUser(user,api):
    try:
        userT = api.get_user(id=user)
        userT = userT._json
    
        embed_n = f'embed_{id}'
        embed_n = Embed()
        embed_n.color = 0xe6938a
    
    
        if userT["protected"] == True:
            emoji = ':lock~1:'
        else:
            emoji = ':unlock~1:'
    
        embed_n.set_title(title=f'**Mentioned User: @{user} | {emoji}**',url=f'https://twitter.com/{user}')
    
        try:
            embed_n.set_image(url=userT["profile_banner_url"])
        except:
            pass
    
        try:
            embed_n.set_thumbnail(url=userT["profile_image_url"])
        except:
            pass
        
        try:
            embed_n.add_field('**User Bio:**',value=userT["description"],inline=True)
        except:
            pass
        
        location = userT["location"]
        if location == "":
            pass
        else:
            try:
                embed_n.add_field('**Location:**',value=location,inline=True)
            except:
                pass
    
        try:
            embed_n.add_field('**Followers:**',value=userT["followers_count"],inline=True)
        except:
            pass

        try:
            latestTweet = userT["status"]
            latestTEXT = latestTweet["text"]
            embed_n.add_field('**Latest Tweet:**',value=latestTEXT,inline=False)
        except:
            pass


        if userT["url"] == None:
            pass
        else:
            try:
                
                embed_n.add_field('**User URL:**',value=userT["url"],inline=False)
            except:
                pass
    
        try:
            for u in userT["entities"]["description"]["urls"]:
                embed_n.add_field('**BIO URL:**',value=f'**[T.CO]({u["url"]}) | {u["url_expanded"]}',inline=True)
        except:
            pass

        embed_n.add_field(name='**Shortcuts:**',value=f'**[PROFILE](https://twitter.com/{user}) | [LIKES](https://twitter.com/{user})**',inline=False)
        embed_n.set_footer(text='Monitor Solutions by @0charlie01')
    
        try:
            for h in WebhookList:
                hook = Webhook(h)
                hook.send(embed=embed_n)
        except:
            pass
    except:
        pass


def sendRegular(id,tweetText,urlList,images,screenNom,userFollowers,userIcon):
    embed_n = f'embed_{id}'
    embed_n = Embed()
    embed_n.color = 0xb1e68a
    try:
        embed_n.set_thumbnail(url=userIcon)
    except:
        pass
    embed_n.set_title(title=f'**New Tweet: @{screenNom}** | Followers: {userFollowers}',url=f'https://twitter.com/{screenNom}/status/{id}')

    
    try:
        embed_n.add_field(name='**Text:**',value=tweetText,inline=False)
    except:
        pass

    try:
        for u in urlList:
            base_u = u.split('<<<|>>>')
            url = f'**[T.CO]({base_u[0]})** - *{base_u[1]}*'
            embed_n.add_field(name='**URLS:**',value=url,inline=False)
    except:
        pass

    try:
        for u in images:
            embed_n.set_image(url=u)
    except:
        pass

    embed_n.add_field(name='**Shortcuts:**',value=f'**[PROFILE](https://twitter.com/{screenNom}) | [LIKES](https://twitter.com/{screenNom})**')
    embed_n.set_footer(text='Monitor Solutions by @0charlie01')

    try:
        for h in WebhookList:
            hook = Webhook(h)
            hook.send(embed=embed_n)
    except:
        pass


def sendQuoted(id,text,urlList,Images,screenName,userFollowers,UserIcon):
    embed_n = f'embed_{id}'
    embed_n = Embed()
    embed_n.color = 0xedc2f2
    try:
        embed_n.set_thumbnail(url=UserIcon)
    except:
        pass
    
    embed_n.set_title(title=f'**Quoted Tweet: @{screenName}** | Followers: {userFollowers}',url=f'https://twitter.com/{screenName}/status/{id}')

    try:
        embed_n.add_field(name='**Text:**',value=text,inline=False)
    except:
        pass

    try:
        for u in urlList:
            base_u = u.split('<<<|>>>')
            url = f'**[T.CO]({base_u[0]})** - *{base_u[1]}*'
            embed_n.add_field(name='**URLS:**',value=url,inline=False)
    except:
        pass

    try:
        for u in Images:
            embed_n.set_image(url=u)
    except:
        pass

    embed_n.add_field(name='**Shortcuts:**',value=f'**[PROFILE](https://twitter.com/{screenName}) | [LIKES](https://twitter.com/{screenName})**')

    embed_n.set_footer(text='Monitor Solutions by @0charlie01')

    try:
        for h in WebhookList:
            hook = Webhook(h)
            hook.send(embed=embed_n)
    except:
        pass




class Monitor:
    def __init__(self):
        self.sentTweets = []
        self.APIlist = []
        print(f"{get_t_name()} Twitter Monitor v2 | by CharlieAIO")
        self.MonitorList = ["soleaio"]

        with open('webhooks.json','r') as webhooksRead:
            webhookData = json.loads(webhooksRead.read())
            for w in webhookData["webhooks"]:
                WebhookList.append(w)
            
        with open('data.json','r') as dataRead:
            data = json.loads(dataRead.read())
            for i in range(2):
                i + 1
                name = f'account{i}'
                print(f"{get_t_name()} Loading API | {name} |")
                auth = tweepy.OAuthHandler(data[name]["consumer_key"], data[name]["consumer_secret"])
                auth.set_access_token(data[name]["access_token"], data[name]["access_secret"])
                #api = tweepy.API(auth)
                self.APIlist.append(tweepy.API(auth))
        
        if len(self.MonitorList) == 1:
            print(f"{get_t_name()} Launching Monitor For {self.MonitorList[0]}")
            for api in self.APIlist:
                threading.Thread(target=self.task, args=(self.MonitorList[0], api)).start()

    
    def task(self, user, api):
        print(f"{get_t_name()} Here ")
        while True:
            try:
                twitter = api.user_timeline(id=user,count=1)
                #print(twitter)
                status = twitter[0]._json
                #print(status)
                if status["id_str"] not in self.sentTweets:
                    if status["retweeted"] == False:
                        print(f"{get_t_name()} Found Tweet ")
                        self.sentTweets.append(status["id_str"])
            
                        #get text from tweet
                        try:
                            tweetText = status["text"]
                        except:
                            tweetText = ' '
        
            
                        #get all urls from tweet
                        try:
                            urlList = []
                            for u in status["entities"]["urls"]:
                                # T.CO URL : FULL URL
                                urlList.append(f'{u["url"]}<<<|>>>{u["expanded_url"]}')
                        except:
                            pass
            
                        #get images from tweet
                        try:
                            images = []
                            for img in status["entities"]["media"]:
                                images.append(img["media_url_https"])
                            
                        except:
                            pass
            
                        #Get tweet sender info
                        try:
                            user = status["user"]
                            screenNom= user["screen_name"]
                            #user_name = user["name"]
                            #userLocation = user["location"]
                            #userBio = user["description"]
                            #userURLS = user["entities"]["url"]["urls"]
                            # T.CO URL : FULL URL
                            #userURL = f'{userURLS[0]["url"]}<<<|>>>{userURLS[0]["expanded_url"]}'
            
                            #userProtected = user["protected"]
                            userFollowers = user["followers_count"]
                            #userBanner = user["profile_banner_url"]
                            userIcon = user["profile_image_url_https"]
            
                        except:
                            pass
        
                        sendRegular(status["id_str"],tweetText,urlList,images,screenNom,userFollowers,userIcon)
                        #Get all mentioned users from tweet
                        try:
                            for u in status["entities"]["user_mentions"]:
                                mentionedUser(u["screen_name"],api)
                        except:
                            pass
        
            
                        #Get quoted tweet data if quoted
                        if status["is_quote_status"] == True:
                            quoted_tweet = status["quoted_status"]
                            q_id = quoted_tweet["id_str"]
            
                            try:
                                QtweetText = quoted_tweet["text"]
                            except:
                                QtweetText = ' '
                
                
                            #get all urls from tweet
                            try:
                                QUOTEDurlList = []
                                for u in quoted_tweet["entities"]["urls"]:
                                    # T.CO URL : FULL URL
                                    QUOTEDurlList.append(f'{u["url"]}<<<|>>>{u["expanded_url"]}')
                            except:
                                pass
                
                            #get images from tweet
                            try:
                                QUOTEDimages = []
                                for img in quoted_tweet["entities"]["media"]:
                                    QUOTEDimages.append(img["media_url_https"])
                                print
                                
                            except:
                                pass
            
                            #Get quoted tweet sender
                            try:
                                user = quoted_tweet["user"]
                                Q_screen_name = user["screen_name"]
                                #Q_user_name = user["name"]
                                #Q_userLocation = user["location"]
                                #Q_userBio = user["description"]
                                #Q_userURLS = user["entities"]["url"]["urls"]
                                # T.CO URL : FULL URL
                                #Q_userURL = f'{Q_userURLS[0]["url"]}:{Q_userURLS[0]["expanded_url"]}'
                
                                #Q_userProtected = user["protected"]
                                Q_userFollowers = user["followers_count"]
                                #Q_userBanner = user["profile_banner_url"]
                                Q_userIcon = user["profile_image_url_https"]
                
                            except:
                                pass
        
                            sendQuoted(q_id,QtweetText,QUOTEDurlList,QUOTEDimages,Q_screen_name,Q_userFollowers,Q_userIcon)
        
                            #Get all mentioned users from tweet
                            try:
                                for u in quoted_tweet["entities"]["user_mentions"]:
                                    mentionedUser(u["screen_name"],api)
                            except:
                                pass

        
                        
                    else:
                        pass
        
                else:
                    time.sleep(0.9)
                    pass
            except:
                print(f"{get_t_name()} Tweepy Error")
                pass

    
            
if __name__ == "__main__":
    Monitor()
