#!/usr/bin/python

'''
Posty
Written by Nick Pegg
http://nickpegg.com/

Very simple static blog engine.
Takes in markdown files, spits out a website.
Invoked via command line with a few commands.
'''

# Various settings
PER_PAGE = 10        # How many posts should there be per page?
TEMPLATE_PATH = 'templates/'


# I wouldn't edit anything below here unless you're feeling adventorous. :)

import os
import sys
import shutil

import sqlite3
import markdown2
from jinja2 import Environment, FileSystemLoader

# Create a jinja environment
jenv = Environment(loader=FileSystemLoader(TEMPLATE_PATH), cache_size=0)


### Utility functions ###
def render_markdown(value):
    ''' Simple jinja filter to render markdown text '''
    return markdown2.markdown(value)
jenv.filters['markdown'] = render_markdown

def file_write(filename, html):
    try:
        file = open(filename, 'w')
        file.write(html)
    except Exception as e:
        print("Unable to write file: " + unicode(e))

### Command functions ###
def init():
    """ Initialize the blog. Create directories, database, etc. """

    if os.path.isfile('posts.db'):
        print("Uh-oh! Looks like you already have a posts database.")
        print("Reinitializing will destroy EVERYTHING.")
        print("Chiggity-check yourself before you wreck yourself.\n")
        response = raw_input("Type YES if you really want to do re-initialize: ")

        if response != "YES":
            print("\nYou didn't type YES, so I'm not doing to do anything.")
            quit()
        print("\nAlright then. I'm giving you a blank slate now.")

    print("\nInitializing your blog...")

    # Init the database
    sql_conn = sqlite3.connect("posts.db")
    cursor = sql_conn.cursor()
    cursor.execute('drop table if exists posts')
    cursor.execute('''create table posts (id integer primary key
                    autoincrement, title text, date text,
                    body text);''')
    sql_conn.commit()
    cursor.close()
    
    shutil.rmtree("output", ignore_errors=True)


def post(args):
    """ Add a new post to the database """
    if len(args) < 1:
        print("Using standard input as the input file\n")
        infile = sys.stdin
    else:
        infile = open(args[0])

    try:
        text = infile.read()
    except Exception as e:
        print("Unable to read from source: " + unicode(e))
        quit(-2)

    title = ''
    while title == "":
        title = raw_input("Give this post a title: ")
        if title == "":
            print("The post NEEDS a title. It will be sad without one! Try again.\n")

    time = raw_input("Enter a time for this post (YYYY-MM-DD HH:MM:SS, or blank for now: \n")
    if time == '':
        time = 'now'

    try:
        conn = sqlite3.connect("posts.db")
        cursor = conn.cursor()
        
        cursor.execute("insert into posts values (NULL, ?, ?, ?);", (title, time, text))
        if cursor.rowcount < 1:
            print("Hmm. For some reason the post couldn't be saved. I'm at a loss here...")
        print("Post added!")
        conn.commit()
        cursor.close()
    except Exception as e:
        print("Unable to save post to database: " + unicode(e))
        quit(-3)


def list_posts():
    """ Lists all of the posts in the database """
    cursor = sqlite3.connect("posts.db").cursor()
    cursor.execute("select * from posts")

    print("\nID\tPost Title")
    print("------------------")
    for row in cursor:
        print(unicode(row[0]) + "\t" + row[1])

    print("\n\nIf you would like to remove a post, do it like so:")
    print("posty.py rm [id] \nWhere [id] is the post id seen above.\n")


def rm(args):
    """ Remove a post from the database """
    try:
        id = int(args[0])
    except:
        print('''You either supplied no post it or one that's not a number!
                Find a suitable one via the list command.''')

    conn = sqlite3.connect("posts.db")
    cursor = conn.cursor()
    cursor.execute("delete from posts where id = %d" % int(id))

    if cursor.rowcount < 1:
        print("I couldn't find the post you're talking about. Check to see if it exists by using the list command.")
    else:
        print("Successfully deleted post #" + unicode(id) + "!")

    conn.commit()
    cursor.close()
    
    
def render(args):
    """ Render the posts and pages into a bunch of HTML files """
    
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()

    if os.path.isdir('output'):
        try:
            shutil.rmtree('output')
        except Exception as e:
            print("Unable to delete and recreate output folder. Please delete it by hand and try again.")
            print("Error: " + unicode(e))
            quit(-1)
    os.mkdir('output')

    cursor = sqlite3.connect('posts.db').cursor()

    try:
        cursor.execute('SELECT * FROM posts ORDER BY date DESC')
    except Exception as e:
        print("Unable to get the posts from the database: " + unicode(e))
        quit(-1)

    # Gather up the posts into a list of dicts
    posts = list()

    for row in cursor:
        post = dict()
        post['id'] = row[0]
        post['title'] = row[1]
        post['date'] = row[2]
        post['body'] = row[3]
        post['href'] = '/posts/' + unicode(post['id']) + ".html"

        posts.append(post)

    # Gather up the pages into a list of dicts
    pages = list()
    if os.path.isdir('pages'):
        page_list = os.listdir('pages')
        page_list.sort()
        

        for file in page_list:
            if os.path.isdir(file):
                dir = file
                subpage_list = os.listdir(os.path.abspath(file))
                subpage_list.sort()

                for file in subpage_list:
                    if os.path.isfile(file):
                        page = dict()
                        page['parent'] = dir
                        page['title'] = os.path.basename(file).capitalize()
                        page['content'] = open(file).read()
                        page['href'] = page['title'] + "/" + os.path.basename(file) + '.html'
                        pages.append(page)
            else:
                page = dict()
                page['parent'] = None
                page['title'] = file.capitalize()
                page['content'] = open('pages/' + file).read()
                page['href'] = page['title'] + ".html"
                pages.append(page)

    # Render the posts as individual pages
    outdir = 'output/posts/'
    os.mkdir(outdir)

    template = jenv.get_template('post.html')
    for post in posts:
        html = template.render(post=post, pages=pages)
        file_write(outdir + unicode(post['id']) + ".html", html)

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
            pages=pages, prev_page=prev_page, next_page= next_page)
        
        if start == 0:
            file_write(outdir + "index.html", html)
        else:
            file_write(outdir + "posts" + unicode(start) + ".html", html)

    # Render the pages
    outdir = 'output/pages/'
    os.mkdir(outdir)

    template = jenv.get_template('page.html')
    for page in pages:
        html = template.render(page=page, pages=pages)
        file_write(outdir + page['title'] + ".html", html)
        
    # Finally, copy all static content over
    shutil.copytree('static', 'output/static/')

    print("\nDone rendering! Check out output/index.html\n")

def main():
    try:
        cmd = sys.argv[1]
    except:
        print("You need to specify a command.")
        print("Valid commands include: init, post, list, rm, render")
        quit(-1)

    args = sys.argv[2:]

    if cmd == "init":
        init()
    elif cmd == "list":
        list_posts()
    elif cmd == "rm":
        rm(args)
    elif cmd == "render":
        render(args)
    elif cmd == "post":
        post(args)
    else:
        print("\n\nInvalid command!")

    # Everything must have gone quite swimmingly
    quit(0)


if __name__ == "__main__":
    main()
