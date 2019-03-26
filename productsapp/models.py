from django.db import models


class Types(models.Model):
    title = models.CharField(max_length=30, unique=True)


class Categories(models.Model):
    title = models.CharField(max_length=30, unique=True)


class Brands(models.Model):
    title = models.CharField(max_length=30, unique=True)


class Products(models.Model):
    type = models.ForeignKey(Types, on_delete=models.PROTECT)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brands, on_delete=models.PROTECT)
    name = models.CharField(max_length=250, verbose_name='Название', blank=True, null=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    price = models.IntegerField(verbose_name='Цена', blank=True, null=True)

    class Meta:
        ordering = ('id',)


class Pictures(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='pics')
    url = models.TextField(max_length=250)


class Links(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='links')
    url = models.TextField(max_length=250)
