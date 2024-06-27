import requests, random, json, re
from bs4 import BeautifulSoup as bs
from fake_headers import Headers
def gen_headers():
    browsers = random.choice(['chrome','firefox','opera'])
    os = random.choice(['win','mac','lin'])
    headers = Headers(browser=browsers, os='win')
    return headers.generate()
result = []

for i in range(21):
    try:
        response = requests.get(f'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page={i}', headers=gen_headers())
        response.encoding = 'utf-8'
        main_html = response.text
        main_soup = bs(main_html, features='lxml')
        vakans_list = main_soup.find(name='div', id="a11y-main-content")
        vakanse_tags_list = vakans_list.find_all(name='div', attrs={'class':"serp-item serp-item_link"})
    except AttributeError:
        continue
    for j, vakanse_tag in enumerate(vakanse_tags_list):
        try:
            h3_tags = vakanse_tag.find(name='h3')
            a_tag = h3_tags.find(name='a')
            salary_tag_root = vakanse_tag.find(name='div', class_="vacancy-serp-item-body__main-info")
            salary_tag = salary_tag_root.find(name='span', attrs={'data-qa':"vacancy-serp__vacancy-compensation"})
            company_city_tag = vakanse_tag.find(name='div', class_="vacancy-serp-item-company")
            company_tag = company_city_tag.find(name='a', attrs={'data-qa':"vacancy-serp__vacancy-employer"})
            city_tag = company_city_tag.find(name='div', attrs={'data-qa':"vacancy-serp__vacancy-address"})
            company_name = company_tag.text
            city = city_tag.text
            title = h3_tags.find(name='span', class_="serp-item__title-link serp-item__title").text
            link = a_tag['href']
            salary = 'Зарплата не указана'
            if salary_tag is not None:    
                salary = salary_tag.text
            response1 = requests.get(link, headers=gen_headers())
            response1.encoding = 'utf-8'
            main_soup1 = bs(response1.text, features='lxml')
            vakans_root1_description_tag = main_soup1.find(name='div', id='HH-React-Root')
            vakans_root2_description_tag = vakans_root1_description_tag.find(name='div', class_='HH-MainContent HH-Supernova-MainContent')
            vakans_root3_description_tag = vakans_root2_description_tag.find(name='div', class_="bloko-text")
            vakans_root4_description_tag = vakans_root3_description_tag.find(name='div', class_="g-user-content")
            vakans_description_text = vakans_root4_description_tag.text
            key1 = re.search('Django', vakans_description_text, flags=re.IGNORECASE)
            key2 = re.search('Flask', vakans_description_text, flags=re.IGNORECASE)
            key_list = [key1, key2]
            if None not in key_list:
                print(key_list)
                res_dict = {
                    'title': title,
                    'сссылка': link,
                    'Зарплата': salary,
                    'Название компании': company_name,
                    'Город': city
                }
                result.append(res_dict)
        except AttributeError:
            continue

with open('result.json', 'w', encoding='utf8') as result_file:
    result_file.write(json.dumps(result, ensure_ascii=False, indent='\t'))