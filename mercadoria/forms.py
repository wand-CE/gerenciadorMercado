from django import forms

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
    class Meta:
        model = Cliente
        fields = '__all__'


class VendedorForm(forms.ModelForm):
    class Meta:
        model = Vendedor
        fields = '__all__'


class CompraForm(forms.ModelForm):
    produtos = [(produto.id, f"{produto.nome} - Estoque: {produto.quantidade_estoque}") for produto in
                Produto.objects.all()]

    produto_quantidade = forms.ChoiceField(
        choices=produtos,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'selecione-produto'}),
    )

    def __init__(self, *args, **kwargs):
        super(CompraForm, self).__init__(*args, **kwargs)

        for produto in Produto.objects.all():
            self.fields[f'quantidades_{produto.nome}'] = forms.IntegerField(
                min_value=0,
                widget=forms.NumberInput(attrs={'class': 'selecione-quantidade'}),
                required=False,
            )

    class Meta:
        model = Compra
        fields = '__all__'
