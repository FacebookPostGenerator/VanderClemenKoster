##################################################################
#   This script accesses the Facebook API and retrieves
#   all posts on a given page.
#   MUST UPDATE ACCESS_TOKEN BEFORE EACH USE
#   Follow directions below
#
#   Author:  Stephen Clemenger
#   Version: 2013-04-26
#
##################################################################

print "FacebookScraper called"

#enable access the internet
import urllib

#regular expressions
import re

#a parsing tool for data like the Graph API data
import json

#to satisfy my curiosity...
from time import clock, time


def cleanupString(string):
    # removes links from text
    string = re.sub(r'^https?:\/\/.*[\r\n]*', '', string, flags=re.MULTILINE)
    return string
#end of onlyascii


#this function returns a dictionary with postIds as keys, and and array of [ post message, like count integer ] as the value
#the passed in pageID is the facebook id deliniation for that page.  example:  me/home
def getPostDict( pageID = "me/home" ):
    
    print "getPostDict() called"
    #  get access_token from https://developers.facebook.com/tools/explorer?method=GET&path=1142421495%3Ffields%3Did%2Cname
    #  and paste it into the access_token variable

    #this is the access_token required by facebook to gain temporary access to the graph API -- MUST BE UPDATED BEFORE EACH USE OF THE PROGRAM
    access_token = "BAACEdEose0cBAJdkBC0ze0odNuuZAN699uTQiGK74PsTcRHT6k9MkIYjnbdtYftNO0sXT9FKUSVvyZCFxEZB2LWhVmRd1GUyAcPayTgxuxKZC1JQh7ZAdZABgmrUMMEixK19DqiPF6yqxE6lKGLTsywGEnfwNfi3l8h9VpQnujK7u71i8IAYqpwaZCTzAYIZCpL5DCWqYdr7bvIJh9gJkwLpN7LT1J9sCd1KTk5gQpddnwZDZD"

    #the number of posts to get from given url
    numberOfNewPostsToGet = 1000
    
    #url that returns the GraphAPI data for the page we are scanning
    urlToImport = "https://graph.facebook.com/" + pageID + "?limit=" + str(numberOfNewPostsToGet) + "&access_token=" + access_token

    #open url, read data, and close connection
    print "opening url: " + urlToImport
    f = urllib.urlopen(urlToImport)
    s = f.read()
    f.close()

    #cleanup input
    s = cleanupString(s)
    
    print s
    
    #check if data is fetched
    if s != '':
        print "Data Fetched!"

    #parse incomming data
    s = s.encode("utf8")
    s = json.loads(s)
    

    print "json evaluation worked"

    #this is the dictionary we will return with case format: { "postId" : [ "postText", #likes ] }
    PostAndLikesDict = {}

    #keep track of ignored posts
    ignoredPosts = 0

    #check to make sure the access key is getting us the data we need.
    try:
        mydata = s['data']
    except:
        print "*** YOU NEED TO GET A NEW ACCESS KEY FOR THE FACEBOOK API ***"
        print "...see documentation..."
        print "program exiting..."
        exit(0)

    print "Adding " + str( len( s['data']) ) + " posts to dataset..."

    #this loop iterates through the posts in the data and stores each one with a "message" and a "likes" key in the dictionary
    # assumption: people like their own post without clicking like.
    #So this adds one to the current "likes count" value and gives unliked posts a value of 1
    for i in s['data']:
        #only get "likes" data if it has likes and a message (otherwise a KeyError occurs)
        try:
            #add post id, message, and likesCount to dictionary  (the key is the post ID)
            PostAndLikesDict[ str(i['id']) ] = [ str(i['message']), int(i['likes']['count'])+1 ]
            print "Added: { " + str(i['id']) + " : " + " [ " + str(i['message']) + " , " + str(int(i['likes']['count'])+1) + " ] "
        except KeyError:
            #if post has no likes, just count it as a post with 1 like (the person who wrote it.
            try:
                PostAndLikesDict[ str(i['id']) ] = [ str(i['message']), 1 ]
                print "Added: { " + str(i['id']) + " : " + " [ " + str(i['message']) + " , 1 ] "
            except KeyError as e:
                #this post has no likes and no message... ignore it.
                ignoredPosts += 1
                print "Ignored a post - Key Error"
                print e
            except Exception as e:
                print "Ignored a post"
                ignoredPosts += 1
                print e
        except Exception as e:
            print "Ignored a post"
            ignoredPosts += 1
            print e

    #print the number of posts ignored.  
    print "Ignored " + str( ignoredPosts ) + " posts."
    #debug lines...
    #print str(ignoredPosts) + " posts were not liked."
    #print str( len( PostAndLikesDict ) ) + " posts added to dataset."

    #return created dictionary
    return PostAndLikesDict
#end of getPostDict()


#retun a simple list of all messages... input is a dictionary like the one created in getPostDict
def getPostDictMessageList( mydict ):
    myMessageList = []
    #iterate through input dict and pull out all messages
    for i in mydict:
        myMessageList.append( myresult[i][0] )
    return myMessageList
#end of getPostDictMessageList



#test getPostDict()

startTime= clock()  #start timer

myresult = getPostDict()

timer = (clock() - startTime)

print myresult


print "getPostDict() Time Elapsed: " + str(timer)

print "---LIST OF MESSAGES---"

#test getPostDictMessageList( mydict ):
print getPostDictMessageList( myresult )


