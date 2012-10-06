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

from django.db import models

class Keyword(models.Model):
    name = models.CharField(max_length=255)
    count = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class Kawasan(models.Model):
    oid = models.IntegerField(primary_key=True, db_column='oid')
    nama_negeri = models.TextField(blank=True)
    nama_kawasan = models.TextField(blank=True)
    kod_kawasan = models.TextField(blank=True)
    kod_negeri = models.TextField(blank=True)

    class Meta:
        db_table = u'kawasan'
        managed = False

class Product(models.Model):
    oid = models.IntegerField(primary_key=True, db_column='oid')
    harga = models.TextField(blank=True)
    nama = models.TextField(blank=True)
    tarikh = models.TextField(blank=True)
    kod_negeri = models.TextField(blank=True)
    kod_kawasan = models.TextField(blank=True)
    kategori = models.TextField(blank=True)
    kod_barang = models.TextField(blank=True)
    premis = models.TextField(blank=True)

    def get_kawasan(self):
        # naive, but we'll get to this later
        kaw = Kawasan.objects.get(kod_kawasan=self.kod_kawasan, kod_negeri=self.kod_negeri)
        return {'kawasan': kaw.nama_kawasan, 'negeri': kaw.nama_negeri}
    kawasan = property(get_kawasan)

    class Meta:
        db_table = u'swdata'
        managed = False
