
from django.shortcuts import render, redirect
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

    print(results)

    # Crear objetos Python a partir de los resultados de la consulta

    return render(request, 'paper_list.html', {'papers': results})