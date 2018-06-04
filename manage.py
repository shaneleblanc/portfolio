import os
import sys
import fileinput
import glob
import markdown
from datetime import datetime
from jinja2 import Template
posts = []
content = []
navbar_links = []
post_template = Template(open('templates/post.html').read())
blog_template = Template(open('templates/blog.html').read())
base_template = Template(open('templates/base.html').read())

def scan_pages():
    print("Scanning pages...")
    content_files = glob.glob("content/*.md")
    for file in content_files:
        md = markdown.Markdown(extensions = ['markdown.extensions.meta'])
        page = {}
        html = md.convert(open(file).read())
        page['filename'] = os.path.basename(file).replace('content/','').replace('.md','.html')
        page['title'] = md.Meta["title"][0]
        page['md'] = markdown.markdownFromFile(input=file,encoding="UTF-8")
        #author = md.Meta["author"][0]
        content.append(page)

def update_content():
    print("Updating content...")
    content_files = glob.glob("content/*.md")
    for file in content_files:
        #print("Making"+os.path.basename(file).replace('content/','').replace('.md','.html'))
        md = markdown.Markdown(extensions = ['markdown.extensions.meta'])
        html = md.convert(open(file).read())
        result = base_template.render(
            title = md.Meta["title"][0],
            filename = os.path.basename(file).replace('content/','').replace('.md','.html'),
            content = html,
            links = navbar_links
        )
        outfile = result.replace(md.Meta["title"][0]+'class','active') # Adds 'active' class to the correct navbar link
        open('docs/'+os.path.basename(file).replace('content/','').replace('.md','.html'), 'w').write(outfile)

def update_navbar():
    print("Updating navbar...")
    for page in content:
        navbar_links.append(f'''<li class="nav-item"> <a class="nav-link {page['title']}class" href="{page['filename']}"> {page['title']}</a></li>''')
    print(navbar_links)

def update_blog():
    print("Updating blog...")
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

def new_post():
    action = input("New what? Please enter 'page' or 'post': ")
    if action == 'page':
        name = input("Great! What should the page be called? ")
        content = str(input("Enter optional content:")) or "This page is under construction."
        new_page = f'''title: {name}

# {name} page

{content}
'''
        open('content/'+name+'.md', 'w+').write(new_page)
        print('Succesfully written to content/'+name+'.md')
    elif action == 'post':
        name = str(input("Great! What should the post be called? "))
        author = str(input("Who is the author of this post? ")) or "Shane LeBlanc"
        content = str(input("Enter optional content: ")) or "Content goes here!"
        new_post = f"title: {name}\nauthor: {author}\n\n## A Heading\n\n{content}"
        open('posts/post_'+datetime.now().strftime("%m-%d-%y_%H-%M")+'.md', 'w+').write(new_post)
        print('Succesfully written to posts/post_'+datetime.now().strftime("%m-%d-%y_%H-%M")+'.md')
        update_blog()
    else:
        print("Try a valid input!")
        new_post()

def main():
    if len(sys.argv) <= 1:
        action = input("Hi, how are you? Please enter 'update' or 'new': ")
    else:
        action = sys.argv[1]

    if action == 'update':
        scan_pages()
        update_navbar()
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
