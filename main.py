from bs4 import BeautifulSoup
import requests
import csv


def scrap_page(soup_obj):
    listings = soup_obj.find_all('li', class_='clearfix job-bx wht-shd-bx')
    for (index, listing) in enumerate(listings):
        job_title = listing.header.h2.text.strip()
        company_name = listing.h3.text.replace('(More Jobs)', '').strip()
        ul_1 = listing.ul.select('li')
        experience = ul_1[0].text.replace('card_travel', '').replace(' yrs', '').strip()
        location = ul_1[-1].span.text.strip() or ''
        salary = ul_1[1].text.strip() if len(ul_1) > 2 else ''

        ul_2 = listing.select('ul')[1]
        job_description = ul_2.select('li')[0].text.replace('Job Description:', '').replace('... More Details',
                                                                                            '').strip()
        skills = ul_2.select('li')[1].text.replace('KeySkills:', '').strip()
        date = listing.find('span', class_='sim-posted').text.strip()

        with open('vue_listings.csv', 'a+', newline='') as csv_file:
            writer.writerow(
                {"Title": job_title, "Company Name": company_name, "Experience (yrs)": experience, "Location": location,
                 "Salary": salary, "Job Description": job_description, "Skills": skills, "Date Posted": date})
    return len(listings)


if __name__ == '__main__':
    csv_file = open('vue_listings.csv', 'a+', newline='')
    field_names = ['Title', 'Company Name', 'Experience (yrs)', 'Location', 'Salary', 'Job Description', "Skills",
                   "Date Posted"]
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()

    page_number = 1
    listings_count = 0
    keyword = 'vue'
    while True:
        url = f'https://www.timesjobs.com/candidate/job-search.html?from=submit&luceneResultSize=50&txtKeywords={keyword}&postWeek=60&searchType=personalizedSearch&actualTxtKeywords={keyword}&searchBy=0&rdoOperator=OR&pDate=I&sequence={page_number}&startPage=1'
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')
        if soup.find('span', class_='error-msg'):
            print(f'No more listings found. Stopped at page {page_number - 1} with {listings_count} listings scrapped.')
            break
        else:
            print(f'Scrapping page #{page_number}...')
            listings_count += scrap_page(soup) # Scrap the page then return the number of listings scrapped
            page_number += 1
    print('Scraping completed!')
