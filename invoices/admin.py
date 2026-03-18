import base64
import os
from django.contrib import admin, messages
from django import forms
from django.utils.html import format_html
from django.urls import reverse, path
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.staticfiles import finders
from weasyprint import HTML  # Import WeasyPrint for PDF generation

from .models import Client, Dog, Invoice, LineItem

class InvoiceForm(forms.ModelForm):
    confirm_save = forms.BooleanField(
        required=True,
        label="Confirm Save",
        help_text="Check this box to confirm saving this invoice."
    )

    class Meta:
        model = Invoice
        fields = '__all__'

# Ensure this is defined before it's used in InvoiceAdmin
class LineItemInline(admin.TabularInline):
    model = LineItem
    extra = 1
    fields = ('dog', 'service', 'custom_service', 'quantity', 'unit_price')
    readonly_fields = ('line_total',)

    class Media:
        js = ('js/auto_fill_unit_price.js', 'js/toggle_service_fields.js')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address_line1', 'address_line2', 'city', 'region', 'postcode')

@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'client')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    form = InvoiceForm
    list_display = ('invoice_number', 'client', 'date_created', 'due_date', 'total_amount', 'download_pdf_link', 'send_email_link')
    inlines = [LineItemInline]
    readonly_fields = ('total_amount', 'client_address', 'invoice_number')

    def send_email_link(self, obj):
        url = reverse('invoices:send_invoice_email', args=[obj.id])
        return format_html('<a href="{}">Send Invoice Email</a>', url)
    send_email_link.short_description = 'Send Email'

    def download_pdf_link(self, obj):
        url = reverse('invoices:generate_invoice_pdf', args=[obj.id])
        return format_html('<a href="{}" target="_blank">Download PDF</a>', url)
    download_pdf_link.short_description = 'Download PDF'

    def client_address(self, obj):
        if obj.client:
            address_parts = [
                obj.client.address_line1 or '',
                obj.client.address_line2 or '',
                obj.client.city or '',
                obj.client.region or '',
                obj.client.postcode or ''
            ]
            formatted_address = '<br>'.join(part for part in address_parts if part)
            return formatted_address if formatted_address else "No address available"
        return "No client selected"
    client_address.short_description = "Client Address"
