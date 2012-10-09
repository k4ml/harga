#-*- coding: utf-8 -*-

# Copyright (c) 2011(s), Mohd. Kamal Bin Mustafa <kamal.mustafa@gmail.com>
# 
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
# 
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import json
import logging
logger = logging.getLogger(__name__)

from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.db.models import F
from django.views.generic import TemplateView

import haystack
from haystack.views import SearchView
from haystack.forms import SearchForm
from haystack.query import SearchQuerySet

from harga.models import Product, Keyword

class ProductSearchView(SearchView):
    form_class = SearchForm

    def __init__(self, *args, **kwargs):
        super(ProductSearchView, self).__init__(self, *args, **kwargs)
        self.form_class = SearchForm
        self.template = 'search.html'

    def extra_context(self):
        extra = super(ProductSearchView, self).extra_context()
        qs = Keyword.objects.all().order_by('-modified')
        extra['latest_searches'] = qs[:30]
        result_count = self.results.count()

        if self.query:
            kw_obj, kw_created = Keyword.objects.get_or_create(name=self.query)
            if not kw_created:
                kw_obj.count = F('count') + 1

            kw_obj.save()

        return extra

    def create_response(self):
        if self.request.GET.get('format', None) != 'json':
            return super(ProductSearchView, self).create_response()

        (paginator, page) = self.build_page()
        out = {}
        out['item_total'] = len(self.results)
        out['item_per_page'] = paginator.per_page
        out['page'] = page.number
        out['items'] = []
        for result in page.object_list:
            item = {}
            item['nama'] = result.object.nama
            item['premis'] = result.object.premis
            item['kawasan'] = result.object.kawasan
            item['kod_kawasan'] = result.object.kod_kawasan
            item['kod_negeri'] = result.object.kod_negeri
            item['kod_barang'] = result.object.kod_barang
            item['kategori'] = result.object.kategori
            item['tarikh'] = result.object.tarikh
            out['items'].append(item)

        return HttpResponse(json.dumps(out, indent=4), mimetype='application/json')

class FAQView(TemplateView):
    template_name = 'faq.html'

faq = FAQView.as_view()

def tmp_result(request):
    context = {}
    simple_backend = haystack.load_backend('simple')
    query = request.GET.get('q', '')
    results = SearchQuerySet().auto_query(query)

    paginator = Paginator(results, 20) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    context['query'] = query
    context['page'] = products

    return render(request, 'search.html', context)
