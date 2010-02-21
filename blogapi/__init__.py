# blogtty
# Copyright (c) 2009 - Rui Batista <rui.batista@ist.utl.pt>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


import xmlrpclib

class BlogServer(object):

    def __init__(self, url, id, user, password):
        self.url = url
        self.id = id
        self.user = user
        self.password = password
        self.server = xmlrpclib.ServerProxy(url)

    def get_categories(self):
        raise NotImplementedError

    def new_post(self, content, title=None, categories=[], keywords=[], date=None, publish=True):
        struct = {"description": xmlrpclib.Binary(content)}

        if title: struct['title'] = title
        if categories: struct['categories'] = categories
        if keywords: struct['mt_keywords'] = keywords
        #if we have a date use it, if not don't supply one, it will default to now
        if date: struct['pubDate'] = xmlrpclib.DateTime(date)
        
        #now post it to server
        id = int(self.server.metaWeblog.newPost(self.id, self.user, self.password, struct, publish))
        published = self.server.metaWeblog.getPost(id, self.user, self.password)
        return published


class Post(object):
    """ Class to represent blog post objects """
    
    def __init__(self, content, title=None, categories=[], keywords=[], datetime=None, publish=True,
    link=None, perma=None, id=None,
    allow_comments=True, allow_pings=True, author=None, password=None):
        self.content = content
        self.title = title
        self.categories = categories
        self.keywords = keywords
        self.datetime = datetime
        self.publish = publish
        self.link = link
        self.perma = perma
        self.id = id
        self.allow_comments = allow_comments
        self.allow_pings = allow_pings
        self.author = author
        self.password = password

