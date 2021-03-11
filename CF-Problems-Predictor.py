import requests
import operator
from bs4 import BeautifulSoup


url = 'https://codeforces.com/contests?complete=true'

problems = {}
problem_count = {}


def load_server_problems():
    f = open("server_data.txt", "r")
    for data in f:
        problem_tag = ''
        tags = ''
        flag = 1
        for c in data:
            if c == '-' and flag == 1:
                flag = 0
            if flag == 1:
                problem_tag = problem_tag + c
            if flag == 0:
                tags = tags + c
        problems[problem_tag] = tags[1:]


def update_tags(page_url):
    tags_dict = {}
    r = requests.get(page_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    a_tags = soup.find_all('a')
    count = 0

    for a_tag in a_tags:
        try:
            if a_tag['href'].find('/problem/') != -1:
                if a_tag['href'] in tags_dict:
                    continue
                tags_dict[a_tag['href']] = 1
                final_tag = a_tag['href'].replace('/contest/', '')
                final_tag = final_tag.replace('problem/', '')
                # print(final_tag)
                count += 1

                single_tag = ''
                for ch in problems[final_tag]:
                    if ch == '/':
                        if single_tag in problem_count:
                            problem_count[single_tag] += 1
                        else:
                            problem_count[single_tag] = 1
                        single_tag = ''
                    else:
                        single_tag = single_tag + ch
        except:
            pass

    return count


def work_on_div_tags():
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    td_tags = soup.find_all('td')

    count_total_problems = 0
    cnt = 0
    for td_tag in td_tags:

        if (td_tag.text.find('(Div. 2)') != -1 or td_tag.text.find('(Rated for Div. 2)') != -1) and td_tag.text.find(
                'Virtual participation') != -1:
            a_tags = td_tag.find_all('a')
            for a_tag in a_tags:
                if cnt >= 30:
                    break
                try:
                    if a_tag['href'].find('virtual') == -1:
                        link = 'https://codeforces.com' + a_tag['href']
                        # print(link)
                        count_total_problems += update_tags(link)
                        cnt += 1
                        print("Getting Data", "{:.2f}".format((cnt/30)*100), "% completed")
                except:
                    pass
    return count_total_problems


# main
load_server_problems()
value = work_on_div_tags()
print("Total Calculated Recent Problems ->", value)

# to print count
# val=0
total_tags = 0
for problem_type in problem_count:
    total_tags += problem_count[problem_type]

problem_count = sorted(problem_count.items(), key=operator.itemgetter(1), reverse=True)
for problem_type in problem_count:
    # print(problem_type, '->', "{0:.2f}".format((problem_count[problem_type]/value)*100))
    print(problem_type[0], "->", "{0:.2f}".format((problem_type[1]/total_tags)*100), "%")
    # "{0:.2f}".format((problem_type[1]/value)*100),"% and ",
    # val += (problem_type[1]/total_tags)*100

# print(val)
