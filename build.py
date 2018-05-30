pages = [
    {
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

def main():
    import os
    import fileinput
    base_file = open('templates/base.html').read()
    for page in pages:
        content_file = open(page['filename']).read()
        print("Making " + page['title'])
        outfile = base_file.replace('{{title}}', page['title'])
        outfile = outfile.replace('{{content}}', content_file)
        outfile = outfile.replace(page['title']+'class','active')
        open('docs/'+page['filename'].replace('content/',''), 'w').write(outfile)
    print("Succesfully added files to docs/")

if __name__ == '__main__':
    main()
