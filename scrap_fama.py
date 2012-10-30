import lxml.html
import requests

#resp = requests.get('http://sdvi.fama.net.my/price/direct/price/daily_commodityRptPrev.asp?Pricing=A&LevelCd=03&PricingDt=2012/10/11&PricingDtAft=2012/10/11')
#print resp.content
html = open('fama.html').read()
page = lxml.html.fromstring(html)
area_tables = page.cssselect('html > body > table tr table')

headers = ['Nama', 'Gred', 'Unit', 'Tinggi', 'Purata', 'Rendah']

for area_table in area_tables:
    for tr in area_table.cssselect('tr'):
        line = []
        for td in tr.cssselect('td'):
            line.append(td.text_content().strip())

        new_line = ''
        if len(line) == 1:
            print line[0]
        else:
            new_line = ', '.join(line)

        if new_line.startswith('Nama Varieti'):
            continue
        if new_line.startswith('Tinggi'):
            continue

        print zip(headers, new_line.split(','))
