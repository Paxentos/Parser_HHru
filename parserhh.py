from turtle import title
import requests as req
from bs4 import BeautifulSoup
import json

data = {
    
    "data":[]
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}
for page in range(2):
    
    url = f"https://ulan-ude.hh.ru/search/vacancy?area=113&search_field=name&search_field=company_name&search_field=description&text=Python+разработчик&from=suggest_post&page={page}&hhtmFrom=vacancy_search_list"
    resp = req.get(url=url,headers=headers)

    soup = BeautifulSoup(resp.text,"lxml")
    tags = soup.find_all(class_='serp-item')

    
    for item in tags:
        a_title = item.find(attrs={"data-qa": "serp-item__title"})
        url_object = a_title.attrs["href"]
        resp_object = req.get(url_object, headers=headers)
        soup_object = BeautifulSoup(resp_object.text, "lxml")

        title = a_title.text
        work_experience = soup_object.find(attrs={"data-qa": "vacancy-experience"}).text
        region = item.find(attrs={"data-qa": "vacancy-serp__vacancy-address"}).text

        work_experience_element = soup_object.find(attrs={"data-qa": "vacancy-experience"})
        work_experience = work_experience_element.text if work_experience_element else "Опыт работы не указан"
        
        salary_element = soup_object.find(attrs={"data-qa": "vacancy-salary"})
        salary = salary_element.text if salary_element else "Зарплата не указана"

        data["data"].append({"Title": title, "Work_experience": work_experience, "Salary": salary, "Region": region})
        print(title, work_experience, region, salary)


        with open("parser.json","w",encoding='utf8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)