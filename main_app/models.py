from django.db import models


class ProductCategory(models.Model):
    categories = models.Manager()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    category_id = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name='Name', max_length=64, unique=True)
    description = models.TextField(verbose_name='Description', blank=True)
    is_active = models.BooleanField(
        db_index=True,
        verbose_name='Is Active?',
        default=True,
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    products = models.Manager()

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    category = models.ForeignKey(
        ProductCategory,
        db_index=True,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name='Product Name',
        max_length=128,
    )
    image = models.ImageField(
        upload_to='products_images',
        blank=True,
    )
    short_desc = models.CharField(
        verbose_name='Short description',
        max_length=60,
        blank=True,
    )
    description = models.TextField(
        verbose_name='Description',
        blank=True,
    )
    price = models.DecimalField(
        verbose_name='Price',
        max_digits=8,
        decimal_places=2,
        default=0,
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Quantity',
        default=0,
    )
    is_hot = models.BooleanField(
        verbose_name='Is hot?',
        default=False,
    )
    is_featured = models.BooleanField(
        verbose_name='Is featured?',
        default=False,
    )
    is_new = models.BooleanField(
        verbose_name='Is new?',
        default=False,
    )
    is_active = models.BooleanField(
        db_index=True,
        verbose_name='Is active?',
        default=True,
    )

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.category.name)

    @classmethod
    def get_items(cls):
        return Product.products.filter(
            is_active=True,
        ).select_related().order_by('category', 'name')
