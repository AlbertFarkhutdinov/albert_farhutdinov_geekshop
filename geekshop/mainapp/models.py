from django.db import models


class ProductCategory(models.Model):
    objects = models.Manager()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(verbose_name='Имя', max_length=64, unique=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    is_active = models.BooleanField(db_index=True, verbose_name="Активный?", default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    objects = models.Manager()

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    category = models.ForeignKey(ProductCategory, db_index=True, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Имя продукта', max_length=128)
    image = models.ImageField(upload_to='products_images', blank=True)
    short_desc = models.CharField(verbose_name='Краткое описание продукта', max_length=60, blank=True)
    description = models.TextField(verbose_name='Описание продукта', blank=True)
    price = models.DecimalField(verbose_name='Цена продукта', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='Количество на складе', default=0)
    is_hot = models.BooleanField(verbose_name="Горячий?", default=False)
    is_featured = models.BooleanField(verbose_name="Рекомендуемый?", default=False)
    is_new = models.BooleanField(verbose_name="Новый?", default=False)
    is_active = models.BooleanField(db_index=True, verbose_name="Активный?", default=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).select_related().order_by('category', 'name')
