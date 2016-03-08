from urllib import request
from urllib import parse
import json
import re


def papers_to_short(input_file='paper_data/papers.txt', output_file='paper_data/papers_short.txt'):
    with open(input_file) as f:
        paper_set = {name.strip() for name in f.readlines()}
    with open(output_file, 'w') as f:
        f.write('''
'''.join(sorted(paper_set)))


def papers_to_url_auto(input_file='paper_data/papers_short.txt', output_file='paper_data/urls.json'):
    with open(input_file) as f:
        papers = f.read().split('''
''')

    try:
        with open(output_file) as f:
            urls = json.load(f)
    except FileNotFoundError:
        urls = dict()

    def paper_to_url(paper_name):
        try:
            return urls[paper_name]
        except KeyError:
            pass

        query = parse.quote_plus(paper_name)

        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers = {'User-Agent': user_agent}

        url = "http://www.google.com/search?hl=en&safe=off&q={}&btnI".format(query)

        req = request.Request(url, None, headers)
        response = request.urlopen(req)
        return response.geturl()

    for paper in papers:
        print('Processing {}'.format(paper))

        if 'his study' in paper:
            urls[paper] = 'THIS STUDY'
        else:
            urls[paper] = paper_to_url(paper)

    with open(output_file, 'w') as f:
        json.dump(urls, f, sort_keys=True, indent=2)


def papers_to_url_manual(input_file='paper_data/urls.json', output_file='paper_data/urls2.json'):
    with open(input_file) as f:
        original = json.load(f)

    try:
        with open(output_file) as f:
            new = json.load(f)
    except FileNotFoundError:
        new = dict()

    for name, url in original.items():
        if name in new:
            continue
        if 'google' not in url:
            new[name] = url
        else:
            new[name] = input(name + '\n').strip()

    with open(output_file, 'w') as f:
        json.dump(new, f, indent=2, sort_keys=True)


YEAR_RE = re.compile(r'\(\d\d\d\d\)')


def papers_to_names(input_file='paper_data/papers_short.txt', output_file='paper_data/names.json'):
    with open(input_file) as f:
        paper_list = f.read().split('\n')

    names = dict()

    for paper in paper_list:
        if 'his study' in paper:
            names[paper] = 'Schafer et al., (n.d.)'
        else:
            author = paper.split(',')[0]
            year = YEAR_RE.findall(paper)[0]

            names[paper] = '{} et al., {}'.format(author, year)

    with open(output_file, 'w') as f:
        json.dump(names, f, indent=2, sort_keys=True)

if __name__ == '__main__':
    papers_to_short()
    papers_to_url_auto()
    papers_to_url_manual()
    papers_to_names()
    print('done')
