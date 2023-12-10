import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, UpdateView, FormView, DetailView

from mercadoria.forms import CategoriaForm, ProdutoForm, ClienteForm, CompraForm
from mercadoria.models import Categoria, Configuracoes, Produto, Cliente, Compra, ItemCompra


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


class LoginUserView(ConfiguracoesMixin, LoginView):
    template_name = 'auth/login.html'

    def form_valid(self, form):
        usuario = form.cleaned_data['username']

        messages.success(self.request, f'Seja bem vindo {usuario}!!!')
        return super().form_valid(form)


class Home(ConfiguracoesMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tema'] = Configuracoes.objects.first().temaEscuro

        return context


class CreateCategory(LoginRequiredMixin, ConfiguracoesMixin, CreateView):
    model = Categoria
    template_name = 'servicos/criarObjeto.html'
    form_class = CategoriaForm
    success_url = reverse_lazy('listarCategorias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_pagina'] = "Registrar Categoria"
        return context

    def form_valid(self, form):
        nome = form.cleaned_data['nome']
        messages.success(self.request, f'Categoria {nome} cadastrada!!!')
        return super().form_valid(form)


class ListCategory(ConfiguracoesMixin, ListView):
    model = Categoria
    template_name = 'servicos/listarObjetos.html'
    context_object_name = 'elementos'

    def get_queryset(self):
        return Categoria.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos_objeto'] = ['Nome', 'Descrição']

        context['valid_fields'] = ['nome', 'descricao']

        context['nome_pagina'] = "Categorias"
        return context


class EditCategory(ConfiguracoesMixin, UpdateView):
    model = Categoria
    template_name = 'servicos/editarObjeto.html'
    form_class = CategoriaForm
    success_url = reverse_lazy('listarCategorias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_pagina'] = f"Editar {context['object'].nome}"
        context['back_to'] = 'listarCategorias'

        return context

    def form_valid(self, form):
        nome = form.cleaned_data['nome']
        messages.success(self.request, f'Categoria {nome} editada!!!')
        return super().form_valid(form)


class ExcludeCategory(ConfiguracoesMixin, DeleteView):
    model = Categoria
    template_name = 'servicos/excluirObjeto.html'
    success_url = reverse_lazy('listarCategorias')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_model'] = 'categoria'
        context['redirect_to'] = 'listarCategorias'

        context['nome_pagina'] = f"Excluir {context['object'].nome}"
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Categoria excluída!!!')
        return super().form_valid(form)


class CreateProduto(LoginRequiredMixin, ConfiguracoesMixin, CreateView):
    model = Produto
    template_name = 'servicos/criarObjeto.html'
    form_class = ProdutoForm
    success_url = reverse_lazy('listarProdutos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_pagina'] = "Registrar Produto"
        return context

    def form_valid(self, form):
        nome = form.cleaned_data['nome']
        messages.success(self.request, f'Produto {nome} cadastrado!!!')
        return super().form_valid(form)


class ListProduto(ConfiguracoesMixin, ListView):
    model = Produto
    template_name = 'servicos/listarObjetos.html'
    context_object_name = 'elementos'

    def get_queryset(self):
        return Produto.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos_objeto'] = ['Nome', 'Categoria', 'Qtd.', 'Preço']

        context['valid_fields'] = ['nome', 'categoria', 'preco', 'quantidade_estoque']

        for produto in context['elementos']:
            produto.nome = produto.nome.title()
            produto.preco = f'R${produto.preco}'.replace(".", ",")

        context['nome_pagina'] = "Produtos"
        return context


class EditProduto(ConfiguracoesMixin, UpdateView):
    model = Produto
    template_name = 'servicos/editarObjeto.html'
    form_class = ProdutoForm
    success_url = reverse_lazy('listarProdutos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_pagina'] = f"Editar {context['object'].nome}"
        context['back_to'] = 'listarProdutos'

        return context

    def form_valid(self, form):
        nome = form.cleaned_data['nome']
        messages.success(self.request, f'Produto {nome} editado!!!')
        return super().form_valid(form)


class ExcludeProduto(ConfiguracoesMixin, DeleteView):
    model = Produto
    template_name = 'servicos/excluirObjeto.html'
    success_url = reverse_lazy('listarProdutos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_model'] = 'produto'
        context['redirect_to'] = 'listarProdutos'

        context['nome_pagina'] = f"Excluir {context['object'].nome}"
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Produto excluído!!!')
        return super().form_valid(form)


class CreateCliente(LoginRequiredMixin, ConfiguracoesMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'servicos/criarObjeto.html'
    success_url = reverse_lazy('listarClientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_pagina'] = "Registrar Cliente"
        return context

    def form_valid(self, form):
        nome = form.cleaned_data['nome']
        messages.success(self.request, f'Cliente {nome} cadastrado!!!')
        return super().form_valid(form)


class ListCliente(ConfiguracoesMixin, ListView):
    model = Cliente
    template_name = 'servicos/listarObjetos.html'
    context_object_name = 'elementos'

    def get_queryset(self):
        return Cliente.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campos_objeto'] = ['CPF', 'Nome']
        context['nome_pagina'] = "Clientes"

        context['valid_fields'] = ['cpf', 'nome']

        return context


class EditCliente(ConfiguracoesMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'servicos/editarObjeto.html'
    success_url = reverse_lazy('listarClientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nascimento = context['form']['nascimento']
        context['form']['nascimento'].initial = nascimento.initial.isoformat()

        context['nome_pagina'] = f"Editar cliente {context['object'].nome}"
        context['back_to'] = 'listarClientes'

        return context

    def form_valid(self, form):
        nome = form.cleaned_data['nome']
        messages.success(self.request, f'Cliente {nome} editado!!!')
        return super().form_valid(form)


class ExcludeCliente(ConfiguracoesMixin, DeleteView):
    model = Cliente
    template_name = 'servicos/excluirObjeto.html'
    success_url = reverse_lazy('listarClientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_model'] = 'cliente'
        context['redirect_to'] = 'listarClientes'

        context['nome_pagina'] = f"Excluir {context['object'].nome}"
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Cliente excluído!!!')
        return super().form_valid(form)


class CreateCompra(LoginRequiredMixin, ConfiguracoesMixin, CreateView):
    model = Compra
    form_class = CompraForm
    template_name = 'servicos/compras/criarCompra.html'
    success_url = reverse_lazy('listarCompras')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_pagina'] = "Registrar compra"
        context['cliente_form'] = ClienteForm
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST
        vendedor = request.user
        cliente_id = data.get('cliente', None)
        produtos = data.get('produtos', None)

        try:
            with transaction.atomic():
                if all([vendedor.is_authenticated, cliente_id, produtos]):
                    cliente = Cliente.objects.get(id=cliente_id)
                    produtos = json.loads(f'[{produtos}]')
                    compra = Compra.objects.create(cliente=cliente, vendedor=vendedor)

                    for p in produtos:
                        produto = Produto.objects.get(id=p['id'])
                        quantidade = int(p['quantidade'])
                        if quantidade:
                            if produto.quantidade_estoque:
                                if quantidade > produto.quantidade_estoque:
                                    message = f'O produto {produto.nome} não possui {quantidade} unidades em estoque'
                                    compra.delete()
                                    return JsonResponse({'success': False, 'message': message})
                                item_compra = ItemCompra.objects.create(
                                    compra=compra,
                                    produto=produto,
                                    quantidade=quantidade,
                                )

                                produto.quantidade_estoque -= quantidade
                                produto.save()
                            else:
                                message = self.request, f'O produto {produto} está fora de estoque'
                                compra.delete()
                                return JsonResponse({'success': False, 'message': message})

                    messages.success(self.request, 'Compra registrada!!!')
                    return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Não foi possível registrar a compra'})


class ListCompra(ConfiguracoesMixin, ListView):
    model = Compra
    template_name = 'servicos/compras/listarCompras.html'

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
                'cliente': compra.cliente,
                'HoraCompra': compra.horaCompra.strftime('%d/%m/%Y %H:%M'),
                'precoTotal': f'R${compra.valor_total()}'.replace('.', ','),
            }

        context['nome_pagina'] = "Compras"

        return context


class ExcludeCompra(ConfiguracoesMixin, DeleteView):
    model = Compra
    template_name = 'servicos/excluirObjeto.html'
    success_url = reverse_lazy('listarCompras')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_model'] = 'compra'
        context['redirect_to'] = 'listarCompras'

        context['nome_pagina'] = f"Excluir {context['object']}"
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Compra excluída!!!')
        return super().form_valid(form)


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
    template_name = 'servicos/compras/detalhesCompra.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['itensCompra'] = ItemCompra.objects.filter(compra=context['object'].id)
        return context
