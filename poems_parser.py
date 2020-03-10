# Create file requirements.txt and put there all external modules (BeautifulSoup)
# https://pip.readthedocs.io/en/1.1/requirements.html

# Add .gitignore file to the repo, and configure it to ignore IDE specific folder ".idea"
# https://git-scm.com/docs/gitignore

# Please read how to create pull requests, it will be much more easier to review next changes
# https://help.github.com/en/desktop/contributing-to-projects/creating-a-pull-request
import urllib.request
from bs4 import BeautifulSoup
import os
import argparse
import codecs


# Open and read url
# This is one line function and you use it only once in your code, it's not necessary.
def get_resource(url):
    resource = urllib.request.urlopen(url)
    return resource.read()


# Parse html
def parse_page(html):
    res = []
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', width="99%", border="0", cellspacing="2", cellpadding="2")
    for row in table.find_all('td', valign='top'):
        res.append(row.find('a', class_='linki2'))
    return res


def main():
    # parse the arguments
    parser = argparse.ArgumentParser(description='My arsg parser')  # You can add better description :)
    parser.add_argument('--output_file', action="store", type=str)
    args = parser.parse_args()
    # parse the poems titles
    poem = parse_page(get_resource('http://taras-shevchenko.in.ua/virshi-shevchenka.html'))
    # create folder
    path = os.path.dirname(os.path.abspath(args.output_file))
    if not os.path.exists(path):   # in python3.7+ you can avoid this check, just:
        os.makedirs(path)          # os.makedirs(path, exist_ok=True)

    # There is a way to make it much more simple
    # with open(args.output_file, "w") as f:
    #     for p in poem:
    #         f.write(p.string.strip() + '\n')

    # open file
    file_to_write = codecs.open(args.output_file, "w", "utf-8")
    # write to file
    for p in poem:
        file_to_write.write(p.string.strip() + '\n')
    # close the file
    file_to_write.close()

    # you don't need read this data from file, just:
    # print('Amount of poems =', len(poem))

    with codecs.open(args.output_file, "r", "utf-8") as file:
        print('Amount of poems =', len(file.readlines()))

    print("Absolute path = ", path)


if __name__ == '__main__':
    main()
