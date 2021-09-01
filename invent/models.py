from django.db import models

# Create your models here.
from django.urls import reverse


class Inventory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование")
    tech_id = models.IntegerField(verbose_name="Тех. ID")
    invent_id = models.CharField(max_length=20, verbose_name="Инвентарный ID")
    room = models.ForeignKey('Location', on_delete=models.PROTECT, verbose_name="Кабинет")
    description = models.TextField(verbose_name="Описание")
    comment = models.TextField(max_length=200, verbose_name="Комментарий")
    department = models.ForeignKey('Department', on_delete=models.PROTECT, verbose_name="Отдел")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время последнего изменения")

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудования'
        ordering = ['name', 'time_create']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('inv', kwargs={'inv_id': self.id})


class Department(models.Model):
    name = models.CharField(max_length=40, verbose_name="Отдел")

    class Meta:
        ordering = ["name"]
        verbose_name = 'Отделы'
        verbose_name_plural = 'Отдел'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dep', args=[str(self.id)])


class Location(models.Model):
    room = models.CharField(max_length=40, verbose_name='Кабинет')
    comment = models.TextField(max_length=200, verbose_name='Комментарий')
    department = models.ForeignKey('Department', on_delete=models.PROTECT, verbose_name='Отдел')

    def __str__(self):
        return str(self.room)

    def get_absolute_id(self):
        return reverse('loc', args=[str(self.id)])

    class Meta:
        verbose_name = "Кабинеты"
        verbose_name_plural = "Кабинет"
        ordering = ['department', 'room']


class Repair(models.Model):
    inv_id = models.OneToOneField('Inventory', unique=True, on_delete=models.PROTECT, verbose_name="ID оборудования")
    comment = models.TextField(max_length=200, verbose_name="Комментарий")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('rep', args=[str(self.id)])

    class Meta:
        verbose_name = 'Ремонты'
        verbose_name_plural = 'Ремонт'
        ordering = ['created_date', 'inv_id']
