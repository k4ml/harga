import os
import sys
import json
import requests

os.environ['DJANGO_SETTINGS_MODULE'] = 'harga.local_settings'

from django.db import connection
from django.db.utils import IntegrityError

from harga.models import Product

"""
max(substr(tarikh, 7)||substr(tarikh, 4, 2)||substr(tarikh, 1, 2))
"""

cur = connection.cursor()
cur.execute("select max(substr(tarikh, 7)||substr(tarikh, 4, 2)||substr(tarikh, 1, 2)) from swdata")

latest_tarikh = cur.fetchone()[0]

query = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=pricewatch_harga&query=select%20*%20from%20%60swdata%60%20where%20substr(tarikh%2C%207)%7C%7Csubstr(tarikh%2C%204%2C%202)%7C%7Csubstr(tarikh%2C%201%2C%202)%20%3E%20'{{LATEST_TARIKH}}'%20limit%2050%3B"
query = query.replace('{{LATEST_TARIKH}}', latest_tarikh)

resp = requests.get(query)

item_list = json.loads(resp.content) 

duplicates = 0
for item in item_list:
    print item
    product = Product(**item)
    tarikh_part = product.tarikh.split('-')
    product.tarikh_iso = '%s-%s-%s' % (tarikh_part[2], tarikh_part[1], tarikh_part[0])

    stop = False
    try:
        product.save()
    except IntegrityError:
        duplicates += 1
        continue
    except Exception as e:
        print e
        stop = True

    if stop:
        sys.exit(1)

print "Total: ", len(item_list)
print "Duplicates: ", duplicates
