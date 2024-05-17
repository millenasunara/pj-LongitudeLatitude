"""
URL configuration for Escola project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.abre_index, name='abre_index'),
    path('enviar_login', views.enviar_login, name='enviar_login'),
    path('confirmar_cadastro', views.confirmar_cadastro, name='confirmar_cadastro'),
    path('cad_turma/<int:id_professor>', views.cad_turma, name='cad_turma'),
    path('salvar_turma', views.salvar_turma_nova, name='salvar_turma_nova'),
    path('lista_turma/<int:id_professor>', views.lista_turma, name='lista_turma'),
    path('excluir_turma/<int:id_turma>/', views.excluir_turma, name='excluir_turma'),
    path('ver_atividades/<int:id_turma>/', views.ver_atividades, name='ver_atividades'),
    path('atividade/<int:id_turma>/cadastrar/', views.cadastrar_atividade, name='cadastrar_atividade'),
    path('exportar_excel_turma/',views.exportar_para_excel_turma, name='exportar_excel_turma'),
    path('exportar-excel/', views.exportar_para_excel_Atividades, name='exportar-excel'),
]
"""
URL configuration for Escola project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.abre_index, name='abre_index'),
    path('enviar_login', views.enviar_login, name='enviar_login'),
    path('confirmar_cadastro', views.confirmar_cadastro, name='confirmar_cadastro'),
    path('cad_turma/<int:id_professor>', views.cad_turma, name='cad_turma'),
    path('salvar_turma', views.salvar_turma_nova, name='salvar_turma_nova'),
    path('lista_turma/<int:id_professor>', views.lista_turma, name='lista_turma'),
    path('excluir_turma/<int:id_turma>/', views.excluir_turma, name='excluir_turma'),
    path('ver_atividades/<int:id_turma>/', views.ver_atividades, name='ver_atividades'),
    path('atividade/<int:id_turma>/cadastrar/', views.cadastrar_atividade, name='cadastrar_atividade'),
    path('exportar_excel_turma/',views.exportar_para_excel_turma, name='exportar_excel_turma'),
    path('exportar-excel/', views.exportar_para_excel_Atividades, name='exportar-excel'),
]
