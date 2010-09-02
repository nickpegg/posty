#!/usr/bin/python

'''
Posty
Written by Nick Pegg
http://github.com/nickpegg/posty/

Very simple static blog generator.
Takes in markdown files, spits out a website.
Invoked via command line with a few commands.
'''

# Various settings
PER_PAGE = 10        # How many posts should there be per page?

# Locations of various files that Posty needs
TEMPLATE_PATH = '_templates/'
POSTS_PATH = '_posts/'
PAGES_PATH = '_pages/'
MEDIA_PATH = '_media/'

OUTPUT_PATH = 'output/'

# Only edit stuff below here if you're feeling adventurous :)

import os
import sys
import shutil
import datetime
import re
from operator import itemgetter

import sqlite3
import markdown2
import yaml
from jinja2 import Environment, FileSystemLoader


# Create a jinja environment
jenv = Environment(loader=FileSystemLoader(TEMPLATE_PATH), cache_size=0)


## Utility functions ###
def render_markdown(value):
    ''' Simple jinja filter to render markdown text '''
    return markdown2.markdown(value)
jenv.filters['markdown'] = render_markdown

def file_write(filename, html):
    try:
        file = open(filename, 'w')
        file.write(html)
    except Exception as e:
        print("Unable to write file: " + str(e))
        
def read_header(file):
    contents = file.read()
    try:
        matches = re.match('(^---\n+(?:.*\n)+)---\n((.*\n?)+)', contents, re.MULTILINE).groups()
        
        header = matches[0]
        for m in matches[1:]:
            body += m
    catch:
        print("The header in " + file + " is screwey. Fix it.")
        quit(-1)
        
    item = yaml.load(header)
    item['body'] = body
    
    return item
    

### Main functions ###
def render():
    """ Render the posts and pages into a bunch of HTML files """
    
    if os.path.isdir(OUTPUT_PATH):
        try:
            shutil.rmtree(OUTPUT_PATH)
        except Exception as e:
            print("Unable to delete and recreate output folder. Please delete it by hand and try again.")
            print("Error: " + unicode(e))
            quit(-1)
    os.mkdir(OUTPUT_PATH)
    
    # Gather up the posts
    posts = list()
    
    if os.path.isdir('_posts'):
    	for file in os.listdir('_posts'):
    	    post = read_header(open('_posts/' + file))
    	    
    		# Might as well validate while we're here
    		if post['body'] == data[0]:
    			print("Error: " + file + " has no post body. Skipping.")
    			continue
    		if post.get('title') is None:
    			print("Error: " + file + " has no title. Skipping.")
    			continue
    		if post.get('date') is None:
    			print("Error: " + file + " has no date. Skipping.")	
    			continue
    			
    		# Everything must have gone fine, so let's add the post.	
    		posts.append(post)
    
    # Gather up the pages
    pages = list()
    
    if os.path.isdir('_pages'):
    	for file in os.listdir('_pages'):
    		page = read_header(open('_pages/' + file))
    		
    		# Let's validate this guy
    		if page['body'] == data[0]:
    			print("Error: " + file + " has no page body. Skipping.")
    			continue
    		if page.get('title') is None:
    			print("Warning: " + file + " has no title. You may want one depending on your template.")
			if page.get('url') is None:
				print("Warning: " + file + " doesn't specify a URL. Using the page filename...")
				page['url'] = file.replace('.yaml', '.html').replace('.yml', '.html')
				
			# Everything went better than expected.
			pages.append(post)
	
	# Let's sort these pages out so they show up right
	# First in alpha order, then by parent/child
	# Children with a non-existant parent get orphaned. Poor bastards.
	sorted_pages = sorted(pages, key=itemgetter('title'))

	pages = list()
	for page in sorted_pages:
		if page.get('parent') is None:
			pages.append(page)

			for possible_child in sorted_pages:
				parent = possible_child.get('parent')
				if parent is not None and parent == page['title']:
					pages.append(page)
			
	

    
    # Render the posts as individual pages
    template = jenv.get_template('post.html')
    for post in posts:
    	date = datetime.strptime(post['date'], "%Y-%m-%d")
        post['url'] = "/" + str(date.year) + "/" + str(date.month) + "/" + str(post['id']) + ".html"
        
        html = template.render(post=post, pages=sorted_pages)
        file_write("output" + post['url'])

    # Render the posts as grouped pages
    outdir = 'output/'
    template = jenv.get_template('posts.html')
    for start in range(0, len(posts), PER_PAGE):
        prev_page = "posts" + unicode(start - PER_PAGE) + ".html"
        next_page = "posts" + unicode(start + PER_PAGE) + ".html"

        if start == 0:
            prev_page = None

        if len(posts) - start <= PER_PAGE:
            next_page = None
        
        html = template.render(posts=posts[start:(start+PER_PAGE-1)],
            pages=sorted_pages, prev_page=prev_page, next_page= next_page)
        
        if start == 0:
            file_write(outdir + "index.html", html)
        else:
            file_write(outdir + "posts" + unicode(start) + ".html", html)

    # Render the pages
    template = jenv.get_template('page.html')
    for page in pages:
        html = template.render(page=page, pages=sorted_pages)
        file_write(outdir + page['url'], html)
        
    # Finally, copy all static content over
    shutil.copytree('_media', 'output/media/')

    print("\nDone rendering! Check out output/index.html\n")

if __name__ == "__main__":
    render()
    quit(0)
