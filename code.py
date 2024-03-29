# -*- coding: utf-8 -*-
import webapp2
import jinja2
import os
import logging
import json
import ConfigParser
import Post
import re
import HTMLParser
from BaseHandler import BaseHandler

blogconfig = ConfigParser.SafeConfigParser({'email': 'cabocha@163.com', 'password': '123456'})
blogconfig.read('blog.cfg')

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)    

def stripTags(html):
    html = html.strip()
    html = html.strip("\n")
    result=[]
    parse=HTMLParser.HTMLParser()
    parse.handle_data=result.append
    parse.feed(html)
    parse.close()
    return "".join(result)

class Index(webapp2.RequestHandler):
    def get(self):        
        posts=Post.List()        
        ps=[]
        for post in posts:                                    
            p={}
            p["content"]=stripTags(post.content)
            p["title"]=post.title
            p["key"]=post.key.id()
            ps.append(p)
        template = JINJA_ENVIRONMENT.get_template('template/index.html')
        self.response.write(template.render({"posts":ps}))

class View(webapp2.RequestHandler):
    def get(self):  
        key=self.request.get("id")
        post=Post.Get(key)        
        template = JINJA_ENVIRONMENT.get_template('template/post.html')
        self.response.write(template.render({"post":post}))            

class Login(BaseHandler):
    def get(self):        
        template = JINJA_ENVIRONMENT.get_template('template/login.html')
        self.response.write(template.render())
    def post(self):        
        email=self.request.get('email')
        password=self.request.get('password')            
        if blogconfig.get('admin', 'email')==email and blogconfig.get('admin', 'password')==password:            
            self.session['admin'] = 'logged'
            self.redirect('/admin')
        else:
            self.response.write("ERROR")

class Admin(BaseHandler):
    def get(self):       
        if (self.session.get('admin', '')!='logged'):
            self.redirect('/login')
        posts=Post.List()
        template = JINJA_ENVIRONMENT.get_template('template/admin.html')
        self.response.write(template.render({"posts":posts}))     

class Edit(BaseHandler):
    def get(self):        
        if (self.session.get('admin', '')!='logged'):
            self.redirect('/login')
        p=None
        key=self.request.get("id")        
        if key!=None and key!="":
            p=Post.Get(key)
        template = JINJA_ENVIRONMENT.get_template('template/edit.html')
        self.response.write(template.render({"post":p}))     

class Save(BaseHandler):
    def post(self):       
        if (self.session.get('admin', '')!='logged'):
            self.redirect('/login')
        key=self.request.get("key")
        title=self.request.get("title")
        content=self.request.get("content")
        logging.info("#####################\n"+content)
        Post.SavePost(key,title,content)
        self.response.write("SUCCESS")

class Delete(BaseHandler):
    def get(self):        
        if (self.session.get('admin', '')!='logged'):
            self.redirect('/login')
        key=self.request.get("id")
        Post.Delete(key)
        self.redirect('/admin')      


config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'cabocha',
}


application = webapp2.WSGIApplication([
    ('/', Index),        
    ('/view', View),     
    ('/login', Login),    
    ('/admin', Admin),      
    ('/edit', Edit),
    ('/save', Save),
    ('/del', Delete),
], config=config, debug=True)
