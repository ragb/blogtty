#!/usr/bin/python
#
#Copyright (c) 2009 - Rui Batista <rui.batista@ist.utl.pt>
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

""" blogtty: a command line blogging tool """

from blogapi import BlogServer
import sys, os
from optparse import OptionParser
from ConfigParser import SafeConfigParser as ConfigParser

__version__ = "0.1.0"
__author__ = "Rui Batista <rui.batista@ist.utl.pt>"

def get_cli_parser(user, defaultconfigfile):
    """ Creates a command line parser for this application """
    parser = OptionParser(usage="%prog [options] [url]", version=__version__)
    
    #SUPPORTED OPTIONS:
    # -v, --verbose: outputs information
    parser.add_option("-v", "--verbose", action="store_true", help="Outputs status information about performed actions")
    #-c, --config: configuration file to use, defualt is ~/.wpcli if exists
    parser.add_option("-c", "--config", metavar="configfile", type="string", default=defaultconfigfile, help="Configuration file to use, default is %s if exitsts" % defaultconfigfile)
    #-f, --file: file name to read contents from
    parser.add_option("-f", "--file", type="string", dest="file", help="File name to read from, if not provided defaults to standarnd intpu")
    #-b, --blog, name of blog to use from config file, default is "default"
    parser.add_option("-b", "--blog", type="string", default="default", help="Blog name to use from configuration file, default is %default")
    #-t, --title to define new post title
    parser.add_option("-T", "--title", type="string", help="Set post title")
    #-C, --categories: coma separated list of categories to post
    parser.add_option("-C", "--categories", type="string", help="Coma separated list of categories do use")
    #-K, --keywords: coma separated list of tags to use
    parser.add_option("-K", "--keywords", type="string", help="Coma separated list of tags do use")
    #-D, --date, publication date of the post
    parser.add_option("-D", "--datetime", type="string", help="Post publication date time, default is current date and time")
    return parser

def make_blog(configfile, blogname):
    #read configuration file
    config = ConfigParser()
    config.read(configfile)
    url = config.get(blogname, 'url')
    id = config.getint(blogname, 'id')
    user = config.get(blogname, 'user')
    password = config.get(blogname, 'password')
    return BlogServer(url, id, user, password)

def main():
    user = os.getenv("$USER")
    home = os.getenv("HOME")
    defaultconfigfile = os.path.join(home, ".blogtty")
    parser = get_cli_parser(user, defaultconfigfile)
    options, args = parser.parse_args()
    blog = make_blog(options.config, options.blog)
    
    #read file contents
    if options.file:
        f = open(options.file, "r")
        contents = f.read()
        f.close()
    else:
        contents = sys.stdin.read()
    
    if options.categories:
        categories = options.categories.split(',')
    else:
        categories = []
    if options.keywords:
        keywords = options.keywords.split(',')
    else:
        keywords = []
    postid = blog.new_post(contents, title=options.title, categories=categories, keywords=keywords)
    if postid and options.verbose:
        print "Post Created"


if __name__ == '__main__':
    main()
