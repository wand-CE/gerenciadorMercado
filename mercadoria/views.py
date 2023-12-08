import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, UpdateView, FormView, DetailView

from mercadoria.forms import CategoriaForm, ProdutoForm, ClienteForm, VendedorForm, CompraForm
from mercadoria.models import Categoria, Configuracoes, Produto, Cliente, Vendedor, Compra, ItemCompra


class ConfiguracoesMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tema'] = Configuracoes.objects.first().temaEscuro
        return context


class SalvarConfiguracoes(View):

    def get(self, request):
        tema = request.GET.get('tema', None)
        if tema:
            configuracoes = Configuracoes.objects.first()
            configuracoes.temaEscuro = tema == 'true'
            configuracoes.save()

        return HttpResponse('')


class Home(ConfiguracoesMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tema'] = Configuracoes.objects.first().temaEscuro

        return context


class CreateCategory(ConfiguracoesMixin, CreateView):
    model = Categoria
    template_name = 'criarObjeto.html'
    form_class = CategoriaForm
    success_url = reverse_lazy('listarCategorias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_pagina'] = "Registrar Categoria"
        return context


class ListCategory(ConfiguracoesMixin, ListView):
    model = Categoria
    template_name = 'listarObjetos.html'
    context_object_name = 'elementos'

    def get_queryset(self):
        return Categoria.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos_objeto'] = [
            campo.name.title() for campo in Categoria._meta.fields if campo.name != 'id']

        context['nome_pagina'] = "Categorias"
        return context


class EditCategory(ConfiguracoesMixin, UpdateView):
    model = Categoria
    template_name = 'editarObjeto.html'
    form_class = CategoriaForm
    success_url = reverse_lazy('listarCategorias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_pagina'] = f"Editar {context['object'].nome}"
        return context


class ExcludeCategory(ConfiguracoesMixin, DeleteView):
    model = Categoria
    template_name = 'excluirObjeto.html'
    success_url = reverse_lazy('listarCategorias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_model'] = 'categoria'
        context['redirect_to'] = 'listarCategorias'

        context['nome_pagina'] = f"Excluir {context['object'].nome}"
        return context


class CreateProduto(ConfiguracoesMixin, CreateView):
    model = Produto
    template_name = 'criarObjeto.html'
    form_class = ProdutoForm
    success_url = reverse_lazy('listarProdutos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_pagina'] = "Registrar Produto"
        return context


class ListProduto(ConfiguracoesMixin, ListView):
    model = Produto
    template_name = 'listarObjetos.html'
    context_object_name = 'elementos'

    def get_queryset(self):
        return Produto.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos_objeto'] = ['Nome', 'Categoria', 'Qtd.', 'Preço']

        for produto in context['elementos']:
            produto.nome = produto.nome.title()
            produto.preco = f'R${produto.preco}'.replace(".", ",")

        context['nome_pagina'] = "Produtos"
        return context


class EditProduto(ConfiguracoesMixin, UpdateView):
    model = Produto
    template_name = 'editarObjeto.html'
    form_class = ProdutoForm
    success_url = reverse_lazy('listarProdutos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_pagina'] = f"Editar {context['object'].nome}"
        return context


class ExcludeProduto(ConfiguracoesMixin, DeleteView):
    model = Produto
    template_name = 'excluirObjeto.html'
    success_url = reverse_lazy('listarProdutos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_model'] = 'produto'
        context['redirect_to'] = 'listarProdutos'

        context['nome_pagina'] = f"Excluir {context['object'].nome}"
        return context


class CreateCliente(ConfiguracoesMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'criarObjeto.html'
    success_url = reverse_lazy('listarClientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_pagina'] = "Registrar Cliente"
        return context


class ListCliente(ConfiguracoesMixin, ListView):
    model = Cliente
    template_name = 'listarObjetos.html'
    context_object_name = 'elementos'

    def get_queryset(self):
        return Cliente.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos_objeto'] = [
            campo.name.title() for campo in Cliente._meta.fields if campo.name not in ['id', 'endereco']]

        for cliente in context['elementos']:
            cliente.nascimento = cliente.nascimento.strftime('%d/%m/%Y')
        context['nome_pagina'] = "Clientes"
        return context


class EditCliente(ConfiguracoesMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'editarObjeto.html'
    success_url = reverse_lazy('listarClientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nascimento = context['form']['nascimento']
        context['form']['nascimento'].initial = nascimento.initial.isoformat()

        context['nome_pagina'] = f"Editar cliente {context['object'].nome}"
        return context


class ExcludeCliente(ConfiguracoesMixin, DeleteView):
    model = Cliente
    template_name = 'excluirObjeto.html'
    success_url = reverse_lazy('listarClientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_model'] = 'cliente'
        context['redirect_to'] = 'listarClientes'

        context['nome_pagina'] = f"Excluir {context['object'].nome}"
        return context


class CreateVendedor(ConfiguracoesMixin, CreateView):
    model = Vendedor
    form_class = VendedorForm
    template_name = 'criarObjeto.html'
    success_url = reverse_lazy('listarVendedores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_pagina'] = "Registrar Vendedor"
        return context


class ListVendedor(ConfiguracoesMixin, ListView):
    model = Vendedor
    template_name = 'listarObjetos.html'
    context_object_name = 'elementos'

    def get_queryset(self):
        return Vendedor.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos_objeto'] = [
            campo.name.title() for campo in Vendedor._meta.fields if campo.name not in ['id', 'endereco']]
        for vendedor in context['elementos']:
            vendedor.nascimento = vendedor.nascimento.strftime('%d/%m/%Y')

        context['nome_pagina'] = "Vendedores"
        return context


class EditVendedor(ConfiguracoesMixin, UpdateView):
    model = Vendedor
    form_class = VendedorForm
    template_name = 'editarObjeto.html'
    success_url = reverse_lazy('listarVendedores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nascimento = context['form']['nascimento']
        context['form']['nascimento'].initial = nascimento.initial.isoformat()

        context['nome_pagina'] = f"Editar vendedor {context['object'].nome}"
        return context


class ExcludeVendedor(ConfiguracoesMixin, DeleteView):
    model = Vendedor
    template_name = 'excluirObjeto.html'
    success_url = reverse_lazy('listarVendedores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_model'] = 'vendedor'
        context['redirect_to'] = 'listarVendedores'

        context['nome_pagina'] = f"Excluir {context['object'].nome}"
        return context


class CreateCompra(ConfiguracoesMixin, CreateView):
    model = Compra
    form_class = CompraForm
    template_name = 'criarCompra.html'
    success_url = reverse_lazy('listarCompras')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_pagina'] = "Registrar compra"
        context['cliente_form'] = ClienteForm
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST
        vendedor_id = data.get('vendedor', None)
        cliente_id = data.get('cliente', None)
        produtos = data.get('produtos', None)
        if all([vendedor_id, cliente_id, produtos]):
            vendedor = Vendedor.objects.get(id=vendedor_id)
            cliente = Cliente.objects.get(id=cliente_id)

            produtos = json.loads(f'[{produtos}]')

            compra = Compra.objects.create(cliente=cliente, vendedor=vendedor)
            compra.save()

            for p in produtos:
                produto = Produto.objects.get(id=p['id'])
                quantidade = int(p['quantidade'])
                if quantidade:
                    if produto.quantidade_estoque:
                        if quantidade > produto.quantidade_estoque:
                            quantidade = produto.quantidade_estoque
                        item_compra = ItemCompra.objects.create(compra=compra, produto=produto,
                                                                quantidade=quantidade)
                        item_compra.save()
                        produto.quantidade_estoque -= quantidade
                        produto.save()
                    else:
                        messages.error(self.request, f'O produto {produto} está fora de estoque')
            return JsonResponse({'success': 'yes'})
        # return redirect('listarCompras')
        return JsonResponse({'success': 'yes'})


class ListCompra(ConfiguracoesMixin, ListView):
    model = Compra
    template_name = 'listarCompras.html'

    def get_queryset(self):
        return Compra.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos_objeto'] = [
            campo.name.title() for campo in self.model._meta.fields if campo.name != 'id']
        context['campos_objeto'].append('Total')

        context['elementos'] = {}

        for compra in self.get_queryset():
            context['elementos'][compra.id] = {
                'vendedor': compra.vendedor,
                'cliente': compra.vendedor,
                'HoraCompra': compra.horaCompra,
                'precoTotal': f'R${compra.valor_total()}'.replace('.', ','),
            }

        for compra in context['elementos']:
            print(compra)
        context['nome_pagina'] = "Compras"

        return context


class EditCompra(ConfiguracoesMixin, UpdateView):
    model = Compra
    form_class = CompraForm
    template_name = 'editarObjeto.html'
    success_url = reverse_lazy('listarCompras')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_pagina'] = f"Editar {context['object']}"
        return context


class ExcludeCompra(ConfiguracoesMixin, DeleteView):
    model = Compra
    template_name = 'excluirObjeto.html'
    success_url = reverse_lazy('listarCompras')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_model'] = 'compra'
        context['redirect_to'] = 'listarCompras'

        context['nome_pagina'] = f"Excluir {context['object']}"
        return context


class CreateClienteJson(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        form = ClienteForm(self.request.POST)
        if form.is_valid():
            cliente = form.save()
            return JsonResponse({'nome': f'{cliente}', 'cliente_id': cliente.id})
        else:
            return JsonResponse({'errors': form.errors})


class SearchProducts(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        value = self.request.GET.get('nameProduct', None)
        results = {'produtos': []}
        if value:
            for produto in Produto.objects.filter(nome__icontains=value):
                results['produtos'].append({
                    'id': produto.id,
                    'nome': produto.nome.title(),
                    'quantidade': produto.quantidade_estoque,
                    'preco': produto.preco,
                    'categoria': f'{produto.categoria}'.title(),
                })

        return JsonResponse(results)


class DetailCompra(ConfiguracoesMixin, LoginRequiredMixin, DetailView):
    model = Compra
    template_name = 'detalhesCompra.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['itensCompra'] = ItemCompra.objects.filter(compra=context['object'].id)
        return context
