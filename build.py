import os
import fileinput
content = [ {
        'filename': 'content/index.html',
        'title': 'Home'
    },
    {
        'filename': 'content/about.html',
        'title': 'About',
    },
    {
        'filename': 'content/blog.html',
        'title': 'Blog',
    },
    {
        'filename': 'content/contact.html',
        'title': 'Contact',
    },
    {
        'filename': 'content/services.html',
        'title': 'Services',
    },
    {
        'filename': 'content/audio.html',
        'title': 'Audio',
    },
    {
        'filename': 'content/music.html',
        'title': 'Music',
    },
    {
        'filename': 'content/software.html',
        'title': 'Software',
    },
    {
        'filename': 'content/hardware.html',
        'title': 'Hardware',
    },
]
def make_posts():
    # Posts should be .md files in the content/blog/ folder.
    # When run, this script will publish a new post with a blog template.
    base_file = open('templates/blog.html').read()
    for r, d, f in os.walk('content/blog/'):
        for file in f:
            print("Found blog post at " + f)
            mtime = os.path.getmtime(file)
            ## Replace {{date}} with last modified time
            last_modified_date = datetime.fromtimestamp(mtime)

def make_pages(pages, base_file):
    for page in pages:
        content_file = open(page['filename']).read()
        print("Making " + page['title'])
        outfile = base_file.replace('{{title}}', page['title'])
        outfile = outfile.replace('{{content}}', content_file)
        outfile = outfile.replace(page['title']+'class','active')
        open('docs/'+page['filename'].replace('content/',''), 'w').write(outfile)
    print("Succesfully added files to docs/")

def main():
    make_pages(content, open('templates/base.html').read())



if __name__ == '__main__':
    main()
