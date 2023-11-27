from django.urls import path

from mercadoria import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('changeConfig/', views.SalvarConfiguracoes.as_view(), name='configuracoes'),

    path('criarCategoria/', views.CreateCategory.as_view(), name='criarCategoria'),
    path('listarCategorias/', views.ListCategory.as_view(), name='listarCategorias'),
    path('editarCategoria/<pk>', views.EditCategory.as_view(), name='editarCategoria'),
    path('excluirCategoria/<pk>', views.ExcludeCategory.as_view(), name='excluirCategoria'),

    path('criarProduto/', views.CreateProduto.as_view(), name='criarProduto'),
    path('listarProdutos/', views.ListProduto.as_view(), name='listarProdutos'),
    path('editarProduto/<pk>', views.EditProduto.as_view(), name='editarProduto'),
    path('excluirProduto/<pk>', views.ExcludeProduto.as_view(), name='excluirProduto'),

    path('criarCliente/', views.CreateCliente.as_view(), name='criarCliente'),
    path('listarClientes/', views.ListCliente.as_view(), name='listarClientes'),
    path('editarCliente/<pk>', views.EditCliente.as_view(), name='editarCliente'),
    path('excluirCliente/<pk>', views.ExcludeCliente.as_view(), name='excluirCliente'),

    path('criarVendedor/', views.CreateVendedor.as_view(), name='criarVendedor'),
    path('listarVendedores/', views.ListVendedor.as_view(), name='listarVendedores'),
    path('editarVendedor/<pk>', views.EditVendedor.as_view(), name='editarVendedor'),
    path('excluirVendedor/<pk>', views.ExcludeVendedor.as_view(), name='excluirVendedor'),

    path('criarCompra/', views.CreateCompra.as_view(), name='criarCompra'),
    path('listarCompras/', views.ListCompra.as_view(), name='listarCompras'),
    path('editarCompra/<pk>', views.EditCompra.as_view(), name='editarCompra'),
    path('excluirCompra/<pk>', views.ExcludeCompra.as_view(), name='excluirCompra'),
]
