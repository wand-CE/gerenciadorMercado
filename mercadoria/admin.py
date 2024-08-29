from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from mercadoria.models import Categoria, Produto, Cliente, Vendedor, Compra, ItemCompra


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao_atual']

    def descricao_atual(self, obj):
        return obj.descricao[:40] + '...' if len(obj.descricao) > 40 else obj.descricao

    descricao_atual.short_description = 'descrição'


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'preco', 'quantidade_estoque', 'categoria']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['cpf', 'nome', 'endereco', 'nascimento']


class VendedorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Vendedor
        fields = ('username', 'cpf', 'first_name', 'last_name', 'email', 'endereco', 'nascimento')


class VendedorChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Vendedor
        fields = ('username', 'cpf', 'first_name', 'last_name', 'email', 'endereco', 'nascimento')


@admin.register(Vendedor)
class VendedorAdmin(DefaultUserAdmin):
    form = VendedorChangeForm
    add_form = VendedorCreationForm

    list_display = ['cpf', 'username']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': (
            'first_name', 'last_name', 'email', 'cpf', 'nascimento', 'endereco')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('username', 'password1', 'password2', 'cpf', 'first_name', 'last_name', 'email', 'endereco',
                           'nascimento')}),
    )


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    pass


@admin.register(ItemCompra)
class ItemCompraAdmin(admin.ModelAdmin):
    list_display = ['nome', 'quantidade', 'precoAtual', 'precoTotal']

    def nome(self, obj):
        return obj.produto.nome
