from django.contrib import admin

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


@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ['cpf', 'nome', 'endereco', 'nascimento']


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    pass


@admin.register(ItemCompra)
class ItemCompraAdmin(admin.ModelAdmin):
    list_display = ['nome', 'quantidade', 'precoAtual', 'precoTotal']

    def nome(self, obj):
        return obj.produto.nome
