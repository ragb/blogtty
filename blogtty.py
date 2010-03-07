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
import sys
import os, os.path
from optparse import OptionParser
from ConfigParser import SafeConfigParser as ConfigParser
import datetime
import webbrowser

__version__ = "0.1.1"
__author__ = "Rui Batista <rui.batista@ist.utl.pt>"
__licence__ = "GPL"

def get_configfiles_list():
    list = []
    # Try first in home config dir acording to xdg
    from xdg.BaseDirectory import xdg_config_home
    list.append(os.path.join(xdg_config_home, "blogtty/blogtty.conf"))
    #try finding a blogtty.conf ffile in current directory
    list.append("blogtty.conf")
    #TODO: more locations to search
    return list

def get_cli_parser():
    """ Creates a command line parser for this application """
    parser = OptionParser(usage="%prog [options]", version=__version__)
    
    #SUPPORTED OPTIONS:
    # -v, --verbose: outputs information
    parser.add_option("-v", "--verbose", action="store_true", help="Outputs status information about performed actions")
    #-c, --config: configuration file to use, defualt is ~/.wpcli if exists
    parser.add_option("-c", "--config", metavar="configfile", type="string", 
    help="Configuration file to use, if not provided the program will try to find a .blogtty file in your home or a blogtty.conf file in current directory")
    #-f, --file: file name to read contents from
    parser.add_option("-f", "--file", type="string", dest="file", help="File name to read from, if not provided defaults to standarnd input")
    #-b, --blog, name of blog to use from config file, default is "default"
    parser.add_option("-b", "--blog", type="string", default="default", help="Blog name to use from configuration file, default is %default")
    #-t, --title to define new post title
    parser.add_option("-T", "--title", type="string", help="Set post title")
    #-D, --draft: don't publish post
    parser.add_option("-D", "--draft", dest="publish", action="store_false", default="True",
    help="Post as draft")
    #-C, --categories: coma separated list of categories to post
    parser.add_option("-C", "--categories", type="string", help="Coma separated list of categories do use")
    #-K, --keywords: coma separated list of tags to use
    parser.add_option("-K", "--keywords", type="string", help="Coma separated list of tags do use")
    #-D, --date, publication date of the post
    parser.add_option("--datetime", type="string", help="Post publication date time, use current local format. Default is current date and time")
    #--datetimeformat: format to use when parsing dates" and times
    parser.add_option("--datetimeformate", type="string", default="%Y-%m-%d %H:%M", dest="datetimeformat",
    help="Specifies the format to parse the string supplied with --datetime, default is %default", metavar="format")
    # --markup: defines the markup to use to render post (default ist none)
    parser.add_option("--markup", type="string")
    #-o, --open: open created post in web browser
    parser.add_option("-o", "--open", dest="open", action="store_true", default="False",
    help="Open created post in web browser")
    return parser

def make_blog(configfiles, blogname):
    #read configuration file
    config = ConfigParser()
    config.read(configfiles)
    url = config.get(blogname, 'url')
    id = config.getint(blogname, 'id')
    user = config.get(blogname, 'user')
    try:
        password = config.get(blogname, 'password')
    except:
        from getpass import getpass
        password = getpass("Enter blog password")
    return BlogServer(url, id, user, password)

def main():
    
    parser = get_cli_parser()
    options, args = parser.parse_args()
    configfiles = get_configfiles_list()
    if options.config:
        configfiles.preprend(options.config)
    blog = make_blog(configfiles, options.blog)
    
    #read file contents
    try:
        if options.file:
            f = open(options.file, "r")
            contents = f.read()
            f.close()
        else:
            contents = sys.stdin.read()
    except Exception,e:
        print e
        exit(-1)
    if options.categories:
        categories = options.categories.split(',')
    else:
        categories = []
    if options.keywords:
        keywords = options.keywords.split(',')
    else:
        keywords = []
    time = None
    if options.datetime:
        time = datetime.datetime.strptime(options.datetime, options.datetimeformat)
    if options.markup:
        from blogapi.markup import render_markup
        contents = render_markup(contents, options.markup)
    try:
            post = blog.new_post(contents, title=options.title, categories=categories, keywords=keywords, date=time, publish=options.publish)
    except Exception, e:
        print e
        exit(-1)
    if options.verbose:
        print "Post Created. Link on %s" % post['link']
    if options.open:
        webbrowser.open_new(post['link'])

def onSIGINT(sig, stackFrame):
    print "Caught interrupt signal, exiting"
    sys.exit(-1)

if __name__ == '__main__':
    # Catch SIGINT
    import signal
    signal.signal(signal.SIGINT, onSIGINT)
    
    main()
