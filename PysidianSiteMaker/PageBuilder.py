import markdown


def BuildPage(source, target):
    print ("source: " + source)
    print("target: " + target)

    contents = open(source).read()
    htmlContents = markdown.markdown(contents)

    with open(target, 'w') as f:
        f.write(htmlContents)