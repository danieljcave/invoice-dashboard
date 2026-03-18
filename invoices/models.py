from django.db import models
from django.core.exceptions import ValidationError  # Import ValidationError
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Max


class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    postcode = models.CharField(max_length=10, blank=True, null=True)
    current_invoice_number = models.IntegerField(default=1)  # Tracks the next invoice number for this client

    def __str__(self):
        return self.name


class Dog(models.Model):
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=50, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="dogs")
    weekly_walks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.client.name})"


class Invoice(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='invoices')
    due_date = models.DateField()
    invoice_number = models.CharField(max_length=20, editable=False)  # Managed automatically
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_created = models.DateTimeField(auto_now_add=True)  # Timestamp created automatically

    class Meta:
        unique_together = ('client', 'invoice_number')  # Enforce unique invoice numbers per client

    def save(self, *args, **kwargs):
        # Save the invoice first to get a primary key
        if not self.pk:
            super().save(*args, **kwargs)

        # Update the total amount after saving
        self.total_amount = sum(item.line_total for item in self.line_items.all())
        super().save(update_fields=['total_amount'])

    def delete(self, *args, **kwargs):
        # Handle updating client's current invoice number when an invoice is deleted
        client = self.client
        super().delete(*args, **kwargs)  # Delete the invoice

        # Recalculate the current invoice number based on existing invoices
        max_invoice_number = client.invoices.aggregate(Max('invoice_number'))['invoice_number__max']

        if max_invoice_number:
            try:
                # Ensure max_invoice_number is an integer
                max_invoice_number = int(max_invoice_number)
                client.current_invoice_number = max_invoice_number + 1
            except ValueError:
                # Handle non-integer max_invoice_number gracefully
                print(f"DEBUG: Non-integer max_invoice_number '{max_invoice_number}' encountered.")
                client.current_invoice_number = 1
        else:
            # If no invoices remain, reset the current invoice number
            client.current_invoice_number = 1

        # Debugging: Log the updated current_invoice_number
        print(f"DEBUG: Updated current_invoice_number for client {client.id}: {client.current_invoice_number}")

        client.save(update_fields=['current_invoice_number'])

    def __str__(self):
        client_name = self.client.name if self.client else "No Client"
        return f"Invoice {self.invoice_number} for {client_name}"


class LineItem(models.Model):
    SERVICE_CHOICES = [
        ('Group Walk', 'Group Walk'),
        ('Pet Visit', 'Pet Visit'),
        ('Dog Sitting', 'Dog Sitting'),
        ('Late Cancellation', 'Late Cancellation')  # Added Late Cancellation
    ]

    SERVICE_PRICES = {
        'Group Walk': 15,
        'Pet Visit': 11,
        'Dog Sitting': 40,
        'Late Cancellation': 15,  # Added Late Cancellation price
    }

    invoice = models.ForeignKey(Invoice, related_name='line_items', on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, null=True, blank=True)
    service = models.CharField(max_length=100, choices=SERVICE_CHOICES, blank=False, null=False)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    @property
    def line_total(self):
        return (self.quantity or 0) * (self.unit_price or 0)

    def save(self, *args, **kwargs):
        # Only set unit_price if it's missing and the service matches a predefined price
        if (self.unit_price is None or self.unit_price == 0) and self.service in self.SERVICE_PRICES:
            self.unit_price = self.SERVICE_PRICES[self.service]
        super().save(*args, **kwargs)

    def clean(self):
        # Enforce positive quantity
        if self.quantity <= 0:
            raise ValidationError({'quantity': 'Quantity must be greater than zero.'})
        super().clean()

    def __str__(self):
        return f"{self.dog.name if self.dog else 'No Dog'}, {self.service}, Quantity: {self.quantity}, Unit Price: {self.unit_price}, Total: {self.line_total}"


# Signals to update invoice total whenever a line item is saved or deleted
@receiver(post_save, sender=LineItem)
@receiver(post_delete, sender=LineItem)
def update_invoice_total(sender, instance, **kwargs):
    invoice = instance.invoice
    invoice.total_amount = sum(item.line_total for item in invoice.line_items.all())
    invoice.save(update_fields=['total_amount'])

