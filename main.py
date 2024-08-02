from bs4 import BeautifulSoup

with open('home.html') as file:
    content = file.read()
    soup = BeautifulSoup(content, 'lxml')
    courses = soup.find_all('div', class_='card')
    for course in courses:
        course_name = course.h5.text
        course_desc = course.p.text
        course_price = course.a.text.split()[-1]
        print(f'{course_name}\n{course_desc}\n{course_price}\n')
        print('---------------------------------')
