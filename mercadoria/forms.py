from datetime import date

from django import forms
from django.core.exceptions import ValidationError

from mercadoria.models import Categoria, Produto, Cliente, Vendedor, Compra


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = '__all__'


class ClienteForm(forms.ModelForm):
    nascimento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Cliente
        fields = '__all__'

    def clean(self):
        errors = {}
        data = super().clean()
        try:
            int(data['cpf'])
        except ValueError:
            errors['cpf'] = 'CPF deve possuir apenas números'

        hoje = date.today()
        if data['nascimento'] >= hoje:
            errors['nascimento'] = 'Data deve ser antiga'
        if len(errors.values()):
            raise ValidationError(errors)
        return data


class VendedorForm(forms.ModelForm):
    class Meta:
        model = Vendedor
        fields = '__all__'


class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = '__all__'
