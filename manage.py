import os
import sys
import io
import fileinput
import glob
import markdown
from datetime import datetime
from jinja2 import Template
posts = []
content = []
navbar_links = []
navbar_projects = []
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
        page['md'] = html
        content.append(page)

def update_content():
    print("Updating content...")
    content_files = glob.glob("content/*.md")
    for file in content_files:
        #print("Making"+os.path.basename(file).replace('content/','').replace('.md','.html'))
        md = markdown.Markdown(extensions = ['markdown.extensions.meta'])
        file_name = os.path.basename(file).replace('content/','').replace('.md','.html')
        html = md.convert(open(file).read())
        result = base_template.render(
            title = md.Meta["title"][0],
            content = html,
            links = navbar_links,
            filename = file_name
        )
        outfile = result.replace(md.Meta["title"][0]+'class','active') # Adds 'active' class to the correct navbar link
        open('docs/'+file_name, 'w').write(outfile)

def update_navbar():
    print("Updating navbar...")
    navbar_links.append(['Blog', 'blog.html'])
    for page in content:
        # # TODO: put the HTML on jinja side, then allow sorting by alphabetical
        navbar_links.append([page['title'], page['filename']])
        #f'''<li class="nav-item"> <a class="nav-link {page['title']}class" href="{page['filename']}"> {page['title']}</a></li>'''
    navbar_links.remove(['Home', 'index.html'])
    print(navbar_links)

def update_blog():
    print("Updating blog...")
    rendered_posts = []
    for root, dirs, files in os.walk('posts/'):
        for file in files:
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
                'content': html
            }
            rendered_posts.append(result)
            posts.append(post)
    # Put POSTS into Blog page template
    blog_content = blog_template.render(
        rendered_posts = rendered_posts,
        posts = posts
    )
    # Put Blog page into Base site template
    blog = base_template.render(
        content = blog_content,
        title = "Blog",
        links = navbar_links
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
        update_content()
    elif action == 'post':
        name = str(input("Great! What should the post be called? "))
        author = str(input("Who is the author of this post? ")) or "Shane LeBlanc"
        content = str(input("Enter optional content: ")) or "Content goes here!"
        new_post = f"title: {name}\nauthor: {author}\n\n## A Heading\n\n{content}"
        date_now = datetime.now().strftime("%m-%d-%y_%H-%M")
        open('posts/post_'+date_now+'.md', 'w+').write(new_post)
        print('Succesfully written to posts/post_'+date_now+'.md')
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
        exit()
    elif action == 'new':
        new_post()
    else:
        print("Try a valid input!")
        main()
    #make_pages(content, open('templates/base.html').read())



if __name__ == '__main__':
    main()
