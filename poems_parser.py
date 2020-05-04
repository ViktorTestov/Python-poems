import urllib.request
from bs4 import BeautifulSoup
import os
import argparse
import re
import operator


# Open resource
def get_resource(url):
    """ Function for getting url."""
    resource = urllib.request.urlopen(url)
    return resource.read()


# parser
def parse_page(html, url):
    """Html parser for parsing whole list of Shevchenko poems.Returns the list of poems"""
    res = []
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', width="99%", border="0", cellspacing="2", cellpadding="2")
    for row in table.find_all('td', valign='top'):
        poem_name = row.find('a', class_='linki2').text
        poem_ur = url + row.find('a', class_='linki2')['href']
        try:
            poem_year = row.find('span').text
            poem_year = re.findall('[0-9]{4}', poem_year)
            poem_year = poem_year[0]
        except (AttributeError, IndexError):
            poem_year = ''
        res.append([poem_name, poem_year, poem_ur])
    return res


def parse_poem_by_url(url):
    """Html parser for parsing selected poems.Returns poem name and whole poem text"""
    poem_page = get_resource(url)
    soup = BeautifulSoup(poem_page, 'html.parser')
    poem_header = soup.find('span', class_="text-head2").text
    poem_text = soup.find('p', align='left').text
    poem = (f'{poem_header} {poem_text}' + '\n')
    return poem


def print_whole_poem(poem_url):
    """function prints whole poems text"""
    poem = parse_poem_by_url(poem_url)
    print(poem)


def parse_args():
    """Function for parsing command line arguments."""
    parser = argparse.ArgumentParser(description='Processing of command line arguments')
    parser.add_argument('--output_file', type=str)
    parser.add_argument('--sort_poems', choices=['name', 'years'], nargs=1, type=str)
    parser.add_argument('--sort_order', choices=['asc', 'desc'], default='asc', nargs=1, type=str)
    parser.add_argument('--display_novel', type=lambda x: x.split('|'))
    args = parser.parse_args()
    return args


def write_poem(poem, output_file):
    """Writes poem in file and prints count of poem and absolute path for file."""
    # create folder
    path = os.path.dirname(os.path.abspath(output_file))
    if not os.path.exists(path):
        os.makedirs(path)
    # open file
    with open(output_file, "w", encoding='utf-8') as f:
        for p in poem:
            f.write(f'{p[0].strip()} {p[1].strip()} \n')
    print('Count of poem =', len(poem))
    print("Absolute path = ", path)


def display_poem(poem, display_novel):
    """Prints whole text of selected poem"""
    for p in poem:
        for n in display_novel:
            if n.strip() == p[0]:
                print_whole_poem(p[2])


def sort_poem(poem, sort_order, sort_poems):
    """prints sorted poems by [name, years] ar [asc, desc]"""
    column_index = 0
    sort_order = True if sort_order == 'desc' else False
    if sort_poems == 'name':
        column_index = 0
    elif sort_poems == 'years':
        column_index = 1
    sorted_poems = sorted(poem, key=operator.itemgetter(column_index), reverse=sort_order)
    for p in sorted_poems:
        print(f'{p[0].strip()} {p[1]}')


def main(args):
    # parse the poems titles
    url = 'http://taras-shevchenko.in.ua/'
    poem = parse_page(get_resource(url + 'virshi-tarasa-shevchenka-kobzar'), url)

    if args.display_novel:
        display_poem(poem, args.display_novel)

    elif args.sort_poems:
        sort_poem(poem, args.sort_order[0], args.sort_poems[0])

    elif args.output_file:
        write_poem(poem, args.output_file)
    else:
        for p in poem:
            print(f'{p[0].strip()} {p[1]}')


if __name__ == '__main__':
    main(parse_args())
