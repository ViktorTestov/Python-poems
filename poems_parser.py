import urllib.request
from bs4 import BeautifulSoup
import os
import argparse
import codecs


# Open and read url
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
    parser = argparse.ArgumentParser(description='My arsg parser')
    parser.add_argument('--output_file', action="store", type=str)
    args = parser.parse_args()
    # parse the poems titles
    poem = parse_page(get_resource('http://taras-shevchenko.in.ua/virshi-shevchenka.html'))
    # create folder
    path = os.path.dirname(os.path.abspath(args.output_file))
    if not os.path.exists(path):
        os.makedirs(path)
    # open file
    file_to_write = codecs.open(args.output_file, "w", "utf-8")
    # write to file
    for p in poem:
        file_to_write.write(p.string.strip() + '\n')
    # close the file
    file_to_write.close()

    with codecs.open(args.output_file, "r", "utf-8") as file:
        print('Amount of poems =', len(file.readlines()))

    print("Absolute path = ", path)


if __name__ == '__main__':
    main()
