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
        struct = {"description": content}
        
        if title: struct['title'] = title
        if categories: struct['categories'] = categories
        if keywords: struct['mt_keywords'] = keywords
        #if we have a date use it, if not don't supply one, it will default to now
        if date: struct['pubDate'] = xmlrpclib.DateTime(date)
        
        #now post it to server
        return bool(self.server.metaWeblog.newPost(self.id, self.user, self.password, struct, publish))


