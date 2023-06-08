import requests
import time
import pathlib
import os
from bs4 import BeautifulSoup
from ebook import Ebook

URL = 'https://www.shubaow.net/{}/{}.html'
HEADERS = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}

def make_ebook(title, id, start, end, shift=0):
    BOOK_TITLE = title
    BOOK_ID = id
    FROM = start
    SHIFT = shift
    TO = end
    PATH = str(pathlib.Path(__file__).parent / 'downloads' / BOOK_TITLE)

    if not os.path.exists(PATH):
        os.makedirs(PATH)

    ebook = Ebook(BOOK_TITLE, PATH)

    for i in range(FROM+SHIFT, TO):
        request = requests.get(URL.format(BOOK_ID, i), headers=HEADERS)
        if request.status_code != 200:
            print('Network Error: ', request.status_code)
            return

        soup = BeautifulSoup(request.text.encode('iso-8859-1').decode('gbk'), 'lxml')
        chapter_title = soup.find('div', {'class': 'bookname'}).h1.string.strip()
        chapter_path = PATH+'/{}.html'.format(chapter_title)
        content = soup.find('div', id='content')
        print('processing: {}'.format(chapter_title))

        with open(chapter_path, 'w', encoding='utf-8') as f:
            f.write('<head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /></head>\n')
            f.write('<body>\n')
            f.write('<h1>{}</h1>'.format(chapter_title) + '\n')
            f.write('\n')

            for e in content:
                if e.string:
                    p = e.string.strip()
                    if len(p) > 0:
                        f.write('<p>{}</p>'.format(p)+'\n')
                    else:
                        f.write('\n')
            f.write('</body>\n')

        ebook.create_chapter(chapter_title, chapter_path)
        time.sleep(3)

    ebook.save_to(BOOK_TITLE+'.mobi')

