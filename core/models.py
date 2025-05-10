from django.db import models


# Product Model
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    # image_url = models.ImageField(upload_to='products/', blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'


# Costumer Model
class Customer(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'customer'


# Order Model
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    # notes = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name}"

    def update_total_amount(self):
        # Updates the total order amount based on items
        self.total_amount = sum(item.subtotal for item in self.items.all())
        self.save()

    class Meta:
        db_table = 'order'


# Order Item Model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Automatically calculate subtotal
        self.unit_price = self.product.price
        self.subtotal = self.unit_price * self.quantity
        super().save(*args, **kwargs)

        # Update order total amount
        self.order.update_total_amount()

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    class Meta:
        db_table = 'order_item'
