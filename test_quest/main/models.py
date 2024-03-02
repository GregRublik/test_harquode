from django.core.validators import MinValueValidator
from django.db import models


# ПРОДУКТ
class Product(models.Model):
    name_product = models.CharField(max_length=50)
    price = models.IntegerField()
    date_start = models.DateField()
    creator = models.ForeignKey('Teacher', on_delete=models.PROTECT)
    min_students_group = models.PositiveIntegerField()
    max_students_group = models.PositiveIntegerField()

    def __str__(self):
        return self.name_product


# ПРЕПОДАВАТЕЛЬ
class Teacher(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)


# ДОСТУП К ПРОДУКТУ
class ProductAccess(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.student.first_name) + " " + str(self.product.name_product)


# СТУДЕНТ
class Student(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    def __str__(self):
        return self.first_name


# УРОК
class Lesson(models.Model):
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    name_lesson = models.CharField(max_length=50)
    video = models.URLField()


# ГРУППА
class Group(models.Model):
    list_student = models.ManyToManyField('Student')
    name_group = models.CharField(max_length=50)
    product = models.ForeignKey('Product', on_delete=models.PROTECT)

    def __str__(self):
        return self.name_group
