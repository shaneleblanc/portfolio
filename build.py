import os
import fileinput
import glob
import markdown
from datetime import datetime
from jinja2 import Template
md = markdown.Markdown(extensions=["markdown.extensions.meta"])
content = []
def update_content():
    import glob
    all_html_files = glob.glob("content/*.html")
    print(all_html_files)
    for file in all_html_files:
        print(file)
        page = {}
        html = md.convert(open(file).read())
        page['filename'] = os.path.basename(file)
        page['title'] = md.Meta["title"][0]
        #author = md.Meta["author"][0]
        content.append(page)
    print(content)
    for r, d, f in os.walk('content/'):
        pass

def update_blog():
    base_file = open('templates/blog.html').read()
    blog_template = Template(base_file)
    for r, d, f in os.walk('posts/'):
        for file in f:
            print("Found blog post at ", f)
            html = md.convert(open('posts/'+file).read())

            mtime = os.path.getmtime('posts/'+file)
            ## Replace {{date}} with last modified time
            last_modified_date = datetime.fromtimestamp(mtime)
            blog_post_template = Template('''
                # {{ title }}
            ''')
            ## Replace {{content}} with file contents

def make_pages(pages, base_file):
    for page in pages:
        content_file = open(page['filename']).read()
        print("Making " + page['title'])
        outfile = base_file.replace('{{title}}', page['title'])
        outfile = outfile.replace('{{content}}', content_file)
        outfile = outfile.replace(page['title']+'class','active') # Adds 'active' class to the correct navbar link
        open('docs/'+page['filename'].replace('content/',''), 'w').write(outfile)
    print("Succesfully added files to docs/")

def main():
    update_content()
    update_blog()
    #make_pages(content, open('templates/base.html').read())



if __name__ == '__main__':
    main()
