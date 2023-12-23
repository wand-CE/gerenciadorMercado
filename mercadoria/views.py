import datetime
import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.validators import RegexValidator
from django.db import transaction
from django.db.models.functions import ExtractMonth, ExtractYear
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, UpdateView, FormView, DetailView

from mercadoria.forms import CategoriaForm, ProdutoForm, ClienteForm, CompraForm, UserDataForm
from mercadoria.models import Categoria, Configuracoes, Produto, Cliente, Compra, ItemCompra

from django.db.models import Count, Sum


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


class ChangeUserData(LoginRequiredMixin, View):
    form_class = UserDataForm

    def get(self, request):
        form = self.form_class(request.GET)
        if form.is_valid():
            request.user.username = form.cleaned_data['username'].title()
            request.user.save()
            return JsonResponse({"success": "Nome trocado com sucesso", 'username': request.user.username})
        else:
            return JsonResponse({"warning": form.errors['username']})


class LoginUserView(ConfiguracoesMixin, LoginView):
    template_name = 'auth/login.html'

    def get(self, request, *args, **kwargs):
        usuario = request.user
        if usuario.is_authenticated:
            messages.error(self.request, f'Você já está logado como {usuario}')
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        usuario = self.request.user
        if usuario.is_authenticated:
            messages.error(self.request, f'Você já está logado como {usuario}')
            return redirect('home')
        usuario = form.cleaned_data['username']

        messages.success(self.request, f'Seja bem vindo {usuario}!!!')
        return super().form_valid(form)

    def form_invalid(self, form):
        usuario = self.request.user
        if usuario.is_authenticated:
            messages.error(self.request, f'Você já está logado como {usuario}')
            return redirect('home')
        return super().form_invalid(form)


class Home(ConfiguracoesMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['totaisVendidos'] = ItemCompra.objects.aggregate(
            quantidadeTotal=Sum('quantidade'),
            precoVendido=Sum('precoTotal')
        )
        context['em_falta'] = Produto.objects.filter(quantidade_estoque=0)

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

        context['valid_fields'] = [
            'nome', 'categoria', 'preco', 'quantidade_estoque']

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
                    compra = Compra.objects.create(
                        cliente=cliente, vendedor=vendedor)

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
        context['itensCompra'] = ItemCompra.objects.filter(
            compra=context['object'].id)
        return context


class ReportsView(ConfiguracoesMixin, LoginRequiredMixin, TemplateView):
    template_name = 'servicos/reports/reports.html'


class GenerateReportsView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        data = self.makeChart()
        return JsonResponse(data)

    def makeChart(self):
        request = self.request.GET
        tipo = request.get('tipoRelatorio', None)
        periodo = request.get('periodo', None)
        ordem = request.get('order', None)

        listTipos = ['produtos', 'clientes', 'categorias', 'meses', 'anos']

        if tipo and (tipo in listTipos):
            dateInit = request.get('dateInit', None)
            dateEnd = request.get('dateEnd', None)

            if periodo == 'range' and dateInit and dateEnd:
                objetosItemCompra = ItemCompra.objects.filter(
                    compra__horaCompra__range=[*sorted([dateInit, dateEnd])])
            else:
                objetosItemCompra = ItemCompra.objects

            result = eval(f'self.por_{tipo}(objetosItemCompra, ordem)')

            graphic_title = ''

            if tipo == 'produtos':
                graphic_title = f'{tipo.title()} {ordem.title()} Vendidos'
            elif tipo == 'categorias':
                graphic_title = f'{tipo.title()} {ordem.title()} Vendidas'
            elif tipo == 'clientes':
                graphic_title = f'{tipo.title()} que {ordem.title()} Compraram'
            elif tipo == 'meses':
                graphic_title = f'Lucros por Mês'
                return {'result': result, 'title': graphic_title, 'is_month': True}

            elif tipo == 'anos':
                graphic_title = f'Lucros por Anos'

            return {'result': result, 'title': graphic_title}

    def por_categorias(self, objeto, ordem):
        result = (objeto
                  .values('produto__categoria__nome')
                  .annotate(valor=Sum('precoTotal'), quantidade_vendida=Sum('quantidade'),
                            categ=Count('produto__categoria__nome'))
                  .order_by('-valor', 'quantidade_vendida'))

        if ordem == 'menos':
            result = result[::-1]

        return [[element['produto__categoria__nome'], element['valor'], element['categ']] for element in result[:10]]

    def por_produtos(self, objeto, ordem):
        result = (objeto
                  .values('produto__nome', 'produto__categoria__nome')
                  .annotate(valor=Sum('precoTotal'), quantidade_vendida=Sum('quantidade'))
                  .order_by('-valor', 'quantidade_vendida'))

        if ordem == 'menos':
            result = result[::-1]

        return [[element['produto__nome'], element['valor'], element['quantidade_vendida']] for element in result[:10]]

    def por_clientes(self, objeto, ordem):
        result = (objeto
                  .values('compra__cliente__nome')
                  .annotate(valor=Sum('precoTotal'), quantidade_vendida=Sum('quantidade'),
                            clientes=Count('compra__cliente__nome'))
                  .order_by('-valor', 'quantidade_vendida'))

        if ordem == 'menos':
            result = result[::-1]

        return [[element['compra__cliente__nome'], element['valor'], element['quantidade_vendida']] for element in
                result[:10]]

    def por_meses(self, objeto, ordem):
        result = (
            Compra.objects
            .annotate(mes=ExtractMonth('horaCompra', tzinfo=datetime.timezone.utc), quantidade=Count('horaCompra'))
            .order_by('-mes'))

        meses = {}
        for i in range(1, 13):
            meses[i] = 0

        for r in result:
            mes = r.mes
            meses[mes] = meses.get(mes) + r.valor_total()

        return [[mes, valorTotal, mes] for mes, valorTotal in meses.items()]

    def por_anos(self, objeto, ordem):
        result = (
            Compra.objects
            .annotate(ano=ExtractYear('horaCompra', tzinfo=datetime.timezone.utc), quantidade=Count('horaCompra'))
            .order_by('-ano'))

        anos = {}

        for r in result:
            ano = r.ano
            anos[ano] = anos.get(ano, 0) + r.valor_total()

        return [[ano, valorTotal, ano] for ano, valorTotal in sorted(anos.items())]
