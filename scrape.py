from bs4 import BeautifulSoup
import requests, json

def main():
    urls = [
    "https://catalog.metu.edu.tr/fac_inst.php?fac_inst=996",
    "https://catalog.metu.edu.tr/fac_inst.php?fac_inst=997",
    "https://catalog.metu.edu.tr/fac_inst.php?fac_inst=998"
    ]

    programs = []
    for url in urls:
        programs += get_program_links(url)

    courses = []
    for program in programs:
        courses += get_courses(program)

    with open('course_names.json', 'w', encoding='utf-8') as f:
        json.dump(list(set(courses)), f, ensure_ascii=False, indent=4)

    print("Scraping done!")


def get_program_links(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    table_items = soup.find_all("td")
    raw_program_links = [item.a for item in table_items]
    program_links = ["https://catalog.metu.edu.tr/"+item["href"] for item in raw_program_links if item != None]

    return program_links


def get_courses(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    table_items = soup.find_all("td", class_="short_course")
    raw_course_names = [item.text for item in table_items]
    course_names = [item[:-3] + " " + item[-3:] for item in raw_course_names if len(item) < 9]

    return course_names


main()
