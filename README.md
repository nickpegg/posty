# Posty

A simple static site generator tool. Reads in a series of posts and pages
containing YAML metadata and Markdown text, and renders them as HTML.

This is what powers [my personal website](https://nickpegg.com).

This was mostly written for fun. There are other, probably better and
definitely more full-featured static site generators out there.

## Super-Quickstart
```
$ posty init
$ vim pages/blah.yaml
$ vim posts/1970-01-01_my-post.yaml
$ posty build
# Then deploy to your web server
```

Go check out [the docs](http://posty.readthedocs.io/) for a more info.
