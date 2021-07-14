from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(
        'имя',
        max_length=64,
        unique=True,
    )
    description = models.TextField(
        'описание',
        blank=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField('активность', default=True)

    def __str__(self):
        return f'{self.name} ({self.updated})'

    class Meta:
        verbose_name = 'категория продукта'
        verbose_name_plural = 'категории продукта'
        ordering = ['name']

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save(using=using)


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE,)
    name = models.CharField('имя', max_length=128,)
    image = models.ImageField(upload_to='product_img', blank=True,)
    short_desc = models.CharField(
        'краткое описание',
        max_length=256,
        blank=True,
    )
    description = models.CharField(
        'описание',
        max_length=500,
        blank=True,
    )
    price = models.DecimalField(
        'цена продукта',
        max_digits=8,
        decimal_places=2,
        default=0,
    )
    quantity = models.PositiveIntegerField('количество товара на складе', default=0,)
    is_active = models.BooleanField('активность', default=True)

    def __str__(self):
        return f'{self.name} (категория: {self.category.name})'

    @classmethod
    def get_items(cls):
        return cls.objects.filter(is_active=True, category__is_active=True)

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['price']
