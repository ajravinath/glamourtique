from django.db import models
from django.contrib.auth.models import User

from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE
from PIL import Image
# Create your models here.


class Customer(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    CATEGORY = ((
        'Earings', 'Earings',
    ), ('Accessory', 'Accessory'))
    image = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    description = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
            # print('ccccccccccccccccccccccccccccccccccccccccccccc', self.image)
            if self.image:
                img = Image.open(self.image.path)
                '''
                resize to 300x300 if larger
                '''
                if(img.height > 300 or img.width > 300):
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.image.path)
        except Exception as e:
            print('Failed to upload to ftp: ' + str(e))
            logger.error('Failed to upload to ftp: ' + str(e))

    def __str__(self):
        return self.name


class Order(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered')
    )
    customer = models.ForeignKey(
        Customer, null=True, on_delete=models.SET_NULL)
    products = models.ManyToManyField(Product)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    note = models.CharField(max_length=200, null=True)

    def get_categories(self):
        cats = []
        unique = [cats.append(product.category)
                  for product in self.products.all() if product.category not in cats]
        return cats

    def __str__(self):
        return self.customer.name + ' ' + str(self.date_created)
