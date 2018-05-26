def main():
    import os
    import fileinput
    #Make sure top and bottom exist and are files...
    try:
        with open('templates/top.html') as file, open('templates/bottom.html') as file:
            pass
    except IOError as e:
        print(e)
    top = open('templates/top.html').read()
    bottom = open('templates/bottom.html').read

    for root, dirs, files in os.walk('content/'):
        for file in files:
            if file.endswith('.html'):
                print("Making " + file)
                newfile = top + open('content/'+file).read() + bottom;
                outfile = open('docs/'+file, 'w')
                outfile.write(newfile)
                outfile.close()
    print("Succesfully added files to docs/")

if __name__ == '__main__':
    main()
