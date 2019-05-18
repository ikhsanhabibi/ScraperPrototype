import requests, bs4
import csv

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

root_url = "https://www.lookup.pk/dynamic/search.aspx?searchtype=kl&k=gym&l=lahore"
html = requests.get(root_url, headers=headers)
soup = bs4.BeautifulSoup(html.text, 'html.parser')

# Pagination
paging = soup.find("div",{"class":"pg-full-width me-pagination"}).find("ul",{"class":"pagination"}).find_all("a")
start_page = paging[1].text
last_page = paging[len(paging)-2].text

# Write to CSV file
outfile = open('gymlookup.csv','w', newline='')
writer = csv.writer(outfile)
writer.writerow(["Name", "Address", "Phone"])

# Scrape per page
pages = list(range(1,int(last_page)+1))
for page in pages:
    url = 'https://www.lookup.pk/dynamic/search.aspx?searchtype=kl&k=gym&l=lahore&page=%s' %(page)
    html = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(html.text, 'html.parser')

    #print(soup.prettify())
    print ('Processing page: %s' %(page))

    product_name_list = soup.findAll("div",{"class":"CompanyInfo"})
    for element in product_name_list:
        name = element.find('h2').text
        address = element.find('address').text.strip()
        phone = element.find("ul",{"class":"submenu"}).text.strip()

        writer.writerow([name, address, phone])

outfile.close()
print ('Done')