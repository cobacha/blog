from google.appengine.ext import ndb
import string
import logging

class Post(ndb.Model):	
 	title = ndb.StringProperty(required=True)
 	content = ndb.StringProperty(required=True, indexed=False)  
 	date = ndb.DateTimeProperty(auto_now_add=True) 	

def SavePost(key, title, content):
	logging.info("#############"+key)
	if key is None or key=="":
		post = Post()
		post.title=title
		post.content=content	
		post.put()
	else:		
		post_key = ndb.Key(Post, string.atol(key))
		post=post_key.get()
		post.title=title
		post.content=content
		post.put()

def Delete(key):
	post_key = ndb.Key(Post, string.atol(key))
	post_key.delete()

def Get(key):	
	post_key = ndb.Key(Post, string.atol(key))
	post=post_key.get()
	return post
	
def List():
	posts=Post.query().order(-Post.date)
	return posts


