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
def parse_page(html):
    """
    Html parser for parsing whole list of Shevchenko poems.
    :param html: HTML document
    :return: list of poems
    """
    res = []
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', width="99%", border="0", cellspacing="2", cellpadding="2")
    for row in table.find_all('td', valign='top'):
        poem_name = row.find('a', class_='linki2').text
        poem_url = row.find('a', class_='linki2')['href']
        try:
            poem_year = row.find('span').text
            poem_year = re.findall('[0-9]{4}', poem_year)
            poem_year = poem_year[0]
        except (AttributeError, IndexError):
            poem_year = ''
        res.append([poem_name, poem_year, poem_url])
    return res


def parse_poem_by_url(url):
    """
    Html parser for parsing selected poems.Returns poem name and whole poem text
    :param url: poem url
    :return: whole poem text
    """
    poem_page = get_resource(url)
    soup = BeautifulSoup(poem_page, 'html.parser')
    poem_header = soup.find('header', class_="entry-header clearfix").text
    poem_text = soup.find('p', align='left').text
    poem = (f'{poem_header.strip()} ' + '\n'
            f'{poem_text}' + '\n')
    return poem


def print_whole_poem(poem_url):
    """
    :param poem_url: url of selected poem
    :return: whole poem text
    """
    poem = parse_poem_by_url(poem_url)
    print(poem)
    return poem


def parse_args():
    """
    :return:  command line arguments
    """
    parser = argparse.ArgumentParser(description='Processing of command line arguments')
    parser.add_argument('--output_file', type=str)
    parser.add_argument('--sort_poems', choices=['name', 'years'], nargs=1, type=str)
    parser.add_argument('--sort_order', choices=['asc', 'desc'], default='asc', nargs=1, type=str)
    parser.add_argument('--display_novel', type=lambda x: x.split('|'))
    args = parser.parse_args()
    return args


def write_poem(poem, output_file):
    """
    Writes poem list in file and prints count of poem and absolute path to the  file.
    :param poem: list of poems
    :param output_file: command line argument
    """
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
    """
    :param poem: list of poems
    :param display_novel: command line argument
    """
    for p in poem:
        for n in display_novel:
            if n.strip() == p[0]:
                return [[p[0], print_whole_poem(p[2])]]


def sort_poem(poem, sort_order, sort_poems):
    """
    :param poem: list of poems
    :param sort_order: sort by [asc, desc]
    :param sort_poems: sort by [name, years]
    :return: sorted list of poems
    """
    column_index = 0
    sort_order = True if sort_order == 'desc' else False
    if sort_poems == 'name':
        column_index = 0
    elif sort_poems == 'years':
        column_index = 1
    sorted_poems = sorted(poem, key=operator.itemgetter(column_index), reverse=sort_order)
    return sorted_poems


def main(args):
    # parse the poems titles
    url = 'http://taras-shevchenko.in.ua/'
    poems = parse_page(get_resource(url + 'virshi-tarasa-shevchenka-kobzar'))

    if args.display_novel:
        poems = display_poem(poems, args.display_novel)

    if args.sort_poems:
        poems = sort_poem(poems, args.sort_order[0], args.sort_poems[0])

    if args.output_file:
        write_poem(poems, args.output_file)

    else:
        for p in poems:
            print(f'{p[0].strip()} {p[1]}')


if __name__ == '__main__':
    main(parse_args())
