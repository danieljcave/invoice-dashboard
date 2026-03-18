from django import forms
from .models import Invoice, LineItem, Client, Dog
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from django.forms import inlineformset_factory

# Invoice Form
class InvoiceForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Due Date"
    )

    class Meta:
        model = Invoice
        fields = ['client', 'due_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Invoice'))
        self.helper.layout = Layout(
            Field('client', css_class='form-control'),
            Field('due_date', css_class='form-control')
        )

# Line Item Form
class LineItemForm(forms.ModelForm):
    class Meta:
        model = LineItem
        fields = ['dog', 'service', 'quantity', 'unit_price']
        labels = {
            'dog': '',  # Remove labels to avoid duplication in table headers
            'service': '',
            'quantity': '',
            'unit_price': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('dog', css_class='form-select', label=''),
            Field('service', css_class='form-select', label=''),
            Field('quantity', css_class='form-control', label=''),
            Field('unit_price', css_class='form-control', label=''),
        )

# Create an inline formset for Line Items
InvoiceLineItemFormSet = inlineformset_factory(
    Invoice, LineItem, form=LineItemForm, extra=1, can_delete=True  # Enable line item deletions
)

# Client Form
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'name', 'email', 'phone',
            'address_line1', 'address_line2',
            'city', 'region', 'postcode', 'current_invoice_number'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Client'))
        self.helper.layout = Layout(
            Field('name', css_class='form-control', placeholder="Enter full name"),
            Field('email', css_class='form-control', placeholder="Enter email address"),
            Field('phone', css_class='form-control', placeholder="Enter phone number"),
            Field('address_line1', css_class='form-control', placeholder="Address Line 1"),
            Field('address_line2', css_class='form-control', placeholder="Address Line 2 (optional)"),
            Field('city', css_class='form-control', placeholder="Enter city"),
            Field('region', css_class='form-control', placeholder="Enter region"),
            Field('postcode', css_class='form-control', placeholder="Enter postcode"),
            Field('current_invoice_number', css_class='form-control', placeholder="Set starting invoice number"),
        )


class DogForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = ['name', 'client']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Dog'))
        self.helper.layout = Layout(
            Field('name', css_class='form-control'),
            Field('client', css_class='form-select'),
        )
