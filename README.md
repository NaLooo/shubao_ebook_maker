# shubao_ebook_maker
Crawl content from www.shubaow.net and produce .mobi ebook

## Quick Start
``` python
from main import make_ebook

# A typical url from the site:
# https://www.shubaow.net/187_187811/40361966.html

make_ebook(title='提灯看刺刀', id='187_187811', start=40361966, end=40362031)

```

## Requirements

-   Python >= 3.0
-   requests >= 2.28.1
-   beautifulsoup4 >= 4.11.1
