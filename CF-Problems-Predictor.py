import requests
from bs4 import BeautifulSoup

url = 'https://codeforces.com/contests'

def update_tags(page_url):
    r = requests.get(page_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    a_tags = soup.find_all('a')

    for a_tag in a_tags:
        if a_tag['href'].find('/problem/') != -1:
            print(a_tag['href'])


def work_on_div_tags():
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    td_tags = soup.find_all('td')

    cnt = 0
    for td_tag in td_tags:

        if (td_tag.text.find('(Div. 2)') != -1 or td_tag.text.find('(Rated for Div. 2)') != -1) and td_tag.text.find('Virtual participation') != -1:
            a_tags = td_tag.find_all('a')
            for a_tag in a_tags:
                if a_tag['href'].find('virtual') == -1:
                    link = 'https://codeforces.com' + a_tag['href']
                    # print(link)
                    update_tags(link)
                    cnt += 1
    return cnt

value = work_on_div_tags()
print(value)
