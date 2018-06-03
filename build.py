import os
import fileinput
import glob
import markdown
from datetime import datetime
from jinja2 import Template
posts = []
content = []
def update_content():
    content_files = glob.glob("content/*.md")
    base_template = Template(open('templates/base.html').read())
    for file in content_files:
        md = markdown.Markdown(extensions = ['markdown.extensions.meta'])
        page = {}
        html = md.convert(open(file).read())

        page['filename'] = os.path.basename(file)
        page['title'] = md.Meta["title"][0]
        page['md'] = markdown.markdownFromFile(input=file,encoding="UTF-8")
        #author = md.Meta["author"][0]
        content.append(page)
    print(content)

def update_blog():
    post_template = Template(open('templates/post.html').read())
    blog_template = Template(open('templates/blog.html').read())
    base_template = Template(open('templates/base.html').read())
    rendered_posts = []
    for r, d, f in os.walk('posts/'):
        for file in f:
            md = markdown.Markdown(extensions=["markdown.extensions.meta"])
            print("Found post at ", f)
            html = md.convert(open('posts/'+file).read())
            mtime = os.path.getmtime('posts/'+file)
            last_modified_date = datetime.fromtimestamp(mtime)

            result = post_template.render(
                title = md.Meta["title"][0],
                author = md.Meta["author"][0],
                date = last_modified_date,
                content = markdown.markdownFromFile(input='posts/'+file,encoding="UTF-8")
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

def main():
    update_content()
    update_blog()
    #make_pages(content, open('templates/base.html').read())



if __name__ == '__main__':
    main()
