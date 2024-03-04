from django.shortcuts import render
from main.models import Product, ProductAccess, Group, Teacher, Student, Lesson
from django.db.models import Q
from datetime import datetime
from rest_framework import serializers, viewsets


# функция для перераспределения по группам
def refresh_list_groups(request):
    product = request.GET['PRODUCT']
    data = {
        'name': product
    }
    # получаем группы по продукту
    groups = Group.objects.filter(product=product)
    # очищаем список для перераспределения
    for group in groups:
        group.list_student.clear()

    # вызываем функцию по занесению в группу по каждому студенту
    for access in ProductAccess.objects.filter(product=product):
        student = access.student.pk
        group_distribution(product, student)

    return render(request, 'main/refresh_groups.html', data)


# функция распределения по группам
def group_distribution(product, student):
    # Получить все группы продукта
    groups = Group.objects.filter(product=product)
    # количество групп
    count_groups = groups.count()
    # минимальное и максимальное количество участников в группе
    students_products = Product.objects.get(pk=product)
    min_students_products = students_products.min_students_group
    max_students_products = students_products.max_students_group
    group_min_number = 1000
    group_min = groups[0]

    # цикл для разбора каждой группы
    for counter, group in enumerate(groups):
        # количество студентов в группе
        students_group = group.list_student.count()
        if min_students_products > students_group:
            # добавляем студентов в группу если количество участников меньше минимума
            group.list_student.add(Student.objects.get(pk=student))
            # print(f'min_in_group:{students_group} min_in_product: {min_students_products}')
            break
        elif group_min_number > students_group:
            # запоминаем группу с минимальным количеством участников
            group_min_number = students_group
            group_min = group

        if counter == count_groups:
            # тут я вставляю студента в группу с наименьшим количеством участников
            if students_group < max_students_products:
                group_min.list_student.add(Student.objects.get(pk=student))
            elif students_group >= max_students_products:
                new_group = Group.objects.create(name_group='new_group', product_id=product)
                new_group.save()
                print('создана новая группа')
                # могу по идее вызывать функцию по перераспределению после создания
                group_distribution(product, student)

            # print(f'min_in_group:{students_group} min_in_product: {min_students_products}')
            break

        # print(f'min_in_group:{students_group} min_in_product: {min_students_products}')


# функция предоставления продукта студенту.
def access_products(product=1, student=1):
    data = {
        'product': product,
        'student': student
    }
    check = ProductAccess.objects.filter(Q(product=data['product']) & Q(student=data['student']))
    if not check.exists():
        open_access_product = ProductAccess.objects.create(product_id=data['product'], student_id=data['student'])
        open_access_product.save()
        group_distribution(product, student)


# views для обработки всех запросов
def distribute_max_values(request):
    data = {}
    if 'PRODUCT' in request.GET:
        data = {
            'product': Product.objects.all(),
            'teacher': Teacher.objects.all(),
            'product_access': ProductAccess.objects.all(),
            'student': Student.objects.all(),
            'lesson': Lesson.objects.all(),
            'group': Group.objects.all()
        }

        if 'ADD_STUDENT_IN_PRODUCT' in request.GET:
            student = request.GET['ADD_STUDENT_IN_PRODUCT']
            product = request.GET['PRODUCT']
            product_for_if = Product.objects.get(pk=product)
            # если продукт уже начался, тогда туда не будут допускаться студенты
            if product_for_if.date_start > datetime.today().date():
                access_products(product, student)

    return render(request, 'main/max_value.html', data)


# api для получения списка продуктов с количеством уроков
class ProductSerializer(serializers.ModelSerializer):
    num_lessons = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name_product', 'num_lessons', 'price', 'date_start')

    def get_num_lessons(self, obj):
        return Lesson.objects.filter(product=obj).count()


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# API для получения списка уроков по продукту, к которому студент имеет доступ
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'name_lesson', 'video')


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer

    def get_queryset(self):
        student = self.request
        # product_access = ProductAccess.objects.filter(student=student)
        # products = [access.product for access in product_access]
        # return Lesson.objects.filter(product__in=products)
        return student
