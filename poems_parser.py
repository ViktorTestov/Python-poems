import urllib.request
from bs4 import BeautifulSoup
import os
import argparse
import re
import operator


# Open resource
def get_resource(url):
    resource = urllib.request.urlopen(url)
    return resource.read()


# parser
def parse_page(html, url):
    res = []
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', width="99%", border="0", cellspacing="2", cellpadding="2")
    for row in table.find_all('td', valign='top'):
        poem_name = row.find('a', class_='linki2').text
        poem_ur = url + row.find('a', class_='linki2')['href']
        try:
            poem_year = row.find('span').text
        except AttributeError:
            continue
        poem_year = re.findall('[0-9]{4}', poem_year)

        res.append([poem_name, poem_year[0], poem_ur])
    return res


# парсить посилання на вірш
def parse_poem_by_url(url):
    poem_page = get_resource(url)
    soup = BeautifulSoup(poem_page, 'html.parser')
    poem_header = soup.find('span', class_="text-head2").text
    poem_text = soup.find('p', align='left').text
    poem = (poem_header + '\n' + poem_text + '\n')
    return poem


def print_whole_poem(poem_url):
    poem = parse_poem_by_url(poem_url)
    print(poem)


def main():
    # parse the poems titles
    url = 'http://taras-shevchenko.in.ua/'
    poem = parse_page(get_resource(url + 'virshi-shevchenka.html'), url)
    # parse the arguments
    parser = argparse.ArgumentParser(description='My arsg parser')
    parser.add_argument('--output_file', action="store", type=str)
    parser.add_argument('--sort_poems', '-name', '-years', action='store', nargs=1)
    parser.add_argument('--sort_order', '-asc', '-desc', action='store', nargs=1)
    parser.add_argument('--display_novel', action='store')
    args = parser.parse_args()
    reverse_sort_order = False
    if args.sort_order and args.sort_order[0] == 'desc':
        reverse_sort_order = True
    if args.output_file:
        # create folder
        path = os.path.dirname(os.path.abspath(args.output_file))
        if not os.path.exists(path):
            os.makedirs(path)
        # open file
        with open(args.output_file, "w", encoding='utf-8') as f:
            for p in poem:
                f.write((p[0].strip() + ' ' + p[1].strip()) + '\n')
        print('Count of poem =', len(poem))
        print("Absolute path = ", path)
    elif args.sort_poems and args.sort_poems[0] == 'name':
        sorted_poems = sorted(poem, key=operator.itemgetter(0), reverse=reverse_sort_order)
        for p in sorted_poems:
            print(p[0].strip() + ' ' + p[1])
    elif args.sort_poems and args.sort_poems[0] == 'years':
        sorted_poems = sorted(poem, key=operator.itemgetter(1), reverse=reverse_sort_order)
        for p in sorted_poems:
            print(p[0].strip() + ' ' + p[1])
    elif args.display_novel:
        novel_names = args.display_novel.split('|')
        for p in poem:
            for n in novel_names:
                if n.strip() == p[0]:
                    print_whole_poem(p[2])
    else:
        for p in poem:
            print(p[0].strip() + ' ' + p[1])


if __name__ == '__main__':
    main()
