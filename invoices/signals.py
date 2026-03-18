from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import LineItem, Invoice

@receiver(post_save, sender=LineItem)
@receiver(post_delete, sender=LineItem)
def update_invoice_total(sender, instance, **kwargs):
    invoice = instance.invoice
    invoice.total_amount = sum(item.line_total for item in invoice.line_items.all())
    invoice.save(update_fields=['total_amount'])
