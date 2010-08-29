# Posty

Posty is a simple website generation tool using markdown for formatting and 
jinja2 for templating. It's based on the concepts of blog posts and static
pages.

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

Any files in the *pages* folder will been converted into HTML files in the 
output/pages/ folder. **Be careful** because the filename is the page name.
If a file is *pages/some_page.txt* then the page title will be 'Some_page.txt'

Posts aren't as finicky. You're asked to name and date every post you add. If
you come across some error about encoding/decoding text or bytestrings, you
likely have a problem with your post's encoding. It should either be plain 
ASCII or UTF8 unicode with no funky character sets.

