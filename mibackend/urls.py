"""mibackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from searchneo4j import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('about/', views.about, name='about'),
    path('papers/', views.paper_list, name='paper_list'),
    path('papers/view/', views.viewsPMCID, name='paperConcepts'),
    path('papers/ontology/', views.viewsPMCIDOntology, name='paperOntology'),
    path('papers/PMCIOntoConcept/', views.viewsPMCIDOntologyConcept, name='paperPMCIOntoConcept'),
    path('papers/concept/', views.viewsConcept, name='paperConcept'),
    path('papers/concept/PMCID', views.viewsPMCIDConcept, name='paperConceptPMCID'),
    path('papers/concept/count', views.viewsConceptCount, name='paperConceptCount'),
]
