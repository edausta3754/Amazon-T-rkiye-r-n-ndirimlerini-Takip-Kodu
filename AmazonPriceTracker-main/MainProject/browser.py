from playwright.sync_api import sync_playwright


def browser_setup():
    pw = sync_playwright().start()
    browser = pw.chromium.launch()
    page = browser.new_page()

    return page


def create_amazon_url(keyword=''):
    keyword = keyword.replace(' ', '+')
    url = f"https://www.amazon.com.br/s?k={keyword}"
    return url


def goto_nextpage(page_soup):
    next_page = page_soup.find('a',
                               class_='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator')
    if next_page:
        return f"https://www.amazon.com.br{next_page['href']}"
    else:
        return None
