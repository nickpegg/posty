# Posty

Posty is a simple website generation tool using markdown for formatting and 
jinja2 for templating. It's based on the concepts of blog posts and static
pages. All metadata is stored as a YAML header (see exmaple files).

A live version of what Posty produces can be found at 
[http://posty.nickpegg.com/](http://posty.nickpegg.com/)

I wrote this over the course of a couple of evenings, so I make no claims 
about the quality of this code. I wrote this for my own use after all. If you
want to use it for your own website or care to make improvements, go for it! :)

## Getting Started

1. Initialize Posty by running ./posty.py init
2. Write a post using markdown and save it somewhere
3. ./posty.py post [post_filename] - Adds the post to the database
4. ./posty.py render - Creates the HTML files in the output folder
5. Upload!

## Gotchas

If Posty complains about your YAML header being funky, your YAML header is 
probably funky. My regex is a bit finicky, so spaces can throw it off. Headers
should look like this:

		---
		title: I am a banana
		date: 2010-04-01
		---
		Post markdown text goes here

Note the lack of spaces after the hyphens, and the fact that there are three.
