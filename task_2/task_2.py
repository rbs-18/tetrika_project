import json
from typing import Dict

import requests
from bs4 import BeautifulSoup, element

HEADERS = {
    'user-agent': (
        f'Mozilla/5.0 (X11Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
        f'Chrome/100.0.4896.143 YaBrowser/22.5.0.1879 (beta) '
        f'Yowser/2.5 Safari/537.36'
    ),
    'accept': '*/*',
}
HOST = 'https://ru.wikipedia.org'


def get_response(url) -> requests.Response:
    """ Get response from url. """

    response = requests.get(url, headers=HEADERS)
    return response


def find_main_block(html: str) -> element.Tag:
    """ Searching main block for work. """

    soup = BeautifulSoup(html, 'html.parser')
    main_block = soup.find('div', id='mw-pages')
    return main_block


def find_next_page(main_block: element.Tag) -> str:
    """ Searching next page for parsing. """

    next_page = HOST
    pages = main_block.find_all('a', recursive=False)

    if pages[-1].get_text(strip=True) == 'Следующая страница':
        next_page += pages[-1].get('href')
    else:
        next_page = ''
    return next_page


def calculate_animals(
    main_block: element.Tag, animals_by_letter: Dict[str, int]
) -> None:
    """ Calculation animals by first letter. """

    letter_blocks = main_block.find_all('div', class_='mw-category-group')

    for letter_block in letter_blocks:
        letter = letter_block.find('h3').get_text(strip=True)
        animal_count = len(letter_block.find_all('li'))
        animals_by_letter[letter] = (
            animals_by_letter.get(letter, 0) + animal_count
        )


def write_result(data):
    """ Write result in file. """

    json.dump(data, open(
        'results.txt', 'w', encoding='utf-8'), indent='\t', ensure_ascii=False
    )


def parse(next_page: str, animals_by_letter: Dict[str, int]) -> None:
    """ Parsing html. """

    while next_page:
        response = get_response(next_page)

        if response.status_code == 200:
            html = response.text
            main_block = find_main_block(html)
            calculate_animals(main_block, animals_by_letter)
            next_page = find_next_page(main_block)
        else:
            print(f'Error, {response.status_code}')
            next_page = ''


if __name__ == '__main__':
    animals_by_letter: Dict[str, int] = {}
    next_page = 'https://inlnk.ru/jElywR'
    parse(next_page, animals_by_letter)
    write_result(animals_by_letter)
