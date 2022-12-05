from django.contrib.auth.models import User
from django.db import models
from rest_framework.reverse import reverse


class AbstractModel(models.Model):
    name = models.CharField('Название', max_length=50, unique=True)
    slug = models.SlugField('URL', max_length=60, unique=True, help_text='Заполняется автоматически')

    class Meta:
        abstract = True
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['-id']

    def __str__(self):
        return f'{self.name}'


class Category(AbstractModel):

    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'slug': self.slug})


class Product(AbstractModel):
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True,
                                 related_name='product_set')
    price = models.PositiveIntegerField('Цена', default=0)
    stock_in = models.BooleanField('В наличии', default=False)
    photo = models.ImageField('Фото', blank=True, upload_to='products/')
    description = models.TextField('Описание', default='Нет описания!')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.SET_NULL, null=True,
                             related_name='comment_set')
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE, related_name='comments_set')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Родительский комментарий',
                               related_name='children', null=True, blank=True)
    description = models.TextField('Комментарий')
    date = models.DateTimeField('Время создание', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-date']

    def __str__(self):
        return f'{self.id}--{self.user}: {self.product}'

    def get_absolute_url(self):
        return reverse('comment-detail', kwargs={'pk': self.id})


class Basket(models.Model):
    product = models.ManyToManyField(Product, verbose_name='Корзина', related_name='bas_product', blank=True)
    user = models.CharField('Пользователь', max_length=50)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        ordering = ['-id']

    def __str__(self):
        return f'{self.id}--{self.user}'

    @staticmethod
    def get_absolute_url():
        return reverse('basket-list')
