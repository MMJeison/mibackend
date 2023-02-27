
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from neomodel import Q
from neomodel import db
# from neomodel import config
# Create your views here.

def home(request):
    context = {
        'titulo': 'Bienvenido a mi sitio web',
        'mensaje': 'Este es el contenido de la página de inicio',
    }
    return render(request, 'home.html', context)

def about(request):
    context = {
        'titulo': 'Acerca de mi sitio web',
        'mensaje': 'Este es el contenido de la página "Acerca de"',
    }
    return render(request, 'about.html', context)



def paper_list(request):
    # Configuración de la base de datos
    # config.DATABASE_URL = 'bolt://neo4j:mipassword@localhost:7688'
    # config.ENCRYPTED_CONNECTION = False

    # Consulta Neo4j para recuperar todos los nodos de tipo Paper
    query = "MATCH (article:bibo__Document)<-[:aoc__annotatesResource]-(concept:aot__ExactQualifier)-[:aoc__hasTopic]->(ontology:n4sch__Class) \
            MATCH (author:foaf__Person)<-[]-(:rdf__Seq)<-[:bibo__authorList]-(article)-[:dct__publisher]->(organization:foaf__Organization) \
            WHERE ontology.dct__source[0] ='IOBC' WITH collect(distinct author.foaf__name[0]) AS Autores,article,ontology,organization \
            RETURN DISTINCT article.bibo__pmid[0] AS PMC_ID, article.dct__title[0] AS Título,article.dct__description[0] as Tipo,ontology.dct__source[0] AS Ontología,Autores,organization.foaf__name[0] \
            AS Organización,article.bibo__shortDescription AS Palabras_Clave,article.dct__created[0] as Fecha_de_publicación,article.bibo__abstract[0] as Abstract LIMIT 25"
    results, meta = db.cypher_query(query)

    papers = [{'id': rec[0],
                'title': rec[1],
                'subtitle': 'This is the subtitle',
                'article_type': rec[2],
                'Ontología': rec[3],
                'authors': [{'full_name': author} for author in rec[4]],
                'Organización': rec[5],
                'key_words': rec[6],
                'published_date': rec[7],
                'abstract': rec[8],
                'metrics': {'relevance': 15, 'views': 0},
              } for rec in results]

    # papers = []
    
    # for rec in list(results):
    #     print(rec)
    #     paper = {'id': rec[0],
    #             'title': rec[1],
    #             'subtitle': 'This is the subtitle',
    #             'article_type': rec[2],
    #             'Ontología': rec[3],
    #             'authors': rec[4],
    #             'Organización': rec[5],
    #             'key_words': rec[6],
    #             'published_date': rec[7],
    #             'abstract': rec[8],
    #             'metrics': {'relevance': 15, 'views': 0},
    #             }
    #     papers.append(paper)

    # Crear objetos Python a partir de los resultados de la consulta

    """ return render(request, 'paper_list.html', {'papers': papers}) """
    return JsonResponse(papers, safe=False)