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
        
        #now post it to server
        return bool(self.server.metaWeblog.newPost(self.id, self.user, self.password, struct, publish))


