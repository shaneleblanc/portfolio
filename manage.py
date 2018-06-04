import os
import sys
import fileinput
import glob
import markdown
from datetime import datetime
from jinja2 import Template
posts = []
content = []
post_template = Template(open('templates/post.html').read())
blog_template = Template(open('templates/blog.html').read())
base_template = Template(open('templates/base.html').read())

def update_content():
    content_files = glob.glob("content/*.md")
    for file in content_files:
        print("Making",file)
        md = markdown.Markdown(extensions = ['markdown.extensions.meta'])
        page = {}
        html = md.convert(open(file).read())
        page['filename'] = os.path.basename(file).replace('content/','').replace('.md','.html')
        page['title'] = md.Meta["title"][0]
        page['md'] = markdown.markdownFromFile(input=file,encoding="UTF-8")
        #author = md.Meta["author"][0]
        content.append(page)
        result = base_template.render(
            title = md.Meta["title"][0],
            filename = os.path.basename(file),
            content = html
        )
        outfile = result.replace(page['title']+'class','active') # Adds 'active' class to the correct navbar link
        open('docs/'+page['filename'], 'w').write(outfile)

def update_blog():
    rendered_posts = []
    for r, d, f in os.walk('posts/'):
        for file in f:
            md = markdown.Markdown(extensions=["markdown.extensions.meta"])
            html = md.convert(open('posts/'+file).read())
            mtime = os.path.getmtime('posts/'+file)
            last_modified_date = datetime.fromtimestamp(mtime)

            result = post_template.render(
                title = md.Meta["title"][0],
                author = md.Meta["author"][0],
                date = last_modified_date,
                post_contents = html
            )
            post = {
                'title': md.Meta["title"][0],
                'author': md.Meta["author"][0],
                'date': last_modified_date,
                'content': markdown.markdownFromFile(input='posts/'+file,encoding="UTF-8")
            }
            rendered_posts.append(result)
            posts.append(post)
    blog_content = blog_template.render(
        rendered_posts = rendered_posts,
        posts = posts
    )
    blog = base_template.render(
        content = blog_content,
        title = "Blog"
    )
    blog = blog.replace('Blogclass','active') # Adds 'active' class to the correct navbar link
    open('docs/blog.html', 'w+').write(blog)

def make_pages(pages, base_file):
    base_template = Template(base_file)
    for page in pages:
        content_file = open(page['filename']).read()
        print("Making " + page['title'])
        outfile = base_file.replace('{{title}}', page['title'])
        outfile = outfile.replace('{{content}}', content_file)
        outfile = outfile.replace(page['title']+'class','active') # Adds 'active' class to the correct navbar link
        open('docs/'+page['filename'].replace('content/',''), 'w').write(outfile)
    print("Succesfully added files to docs/")

def new_post():
    action = input("New what? Please enter 'page' or 'post':")
    if action == 'page':
        name = input("Great! What should the page be called?")
        new_page = f'''title: {name}

        # {name} page

        Fill in the page here..!
        '''
        open('content/'+name+'.md', 'w+').write(new_page)
    elif action == 'post':

    else:
        print("Try a valid input!")
        new_post()
def main():
    if len(sys.argv) <= 1:
        action = input("Hi, how are you? Please enter 'update' or 'new'")
    else:
        action = sys.argv[1]

    if action == 'update':
        update_content()
        update_blog()
    elif action == 'new':
        new_post()
    else:
        print("Try a valid input!")
        main()
    #make_pages(content, open('templates/base.html').read())



if __name__ == '__main__':
    main()
