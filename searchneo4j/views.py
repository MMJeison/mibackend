
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from neomodel import Q
from neomodel import db
import random as rd
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


# TO DO: Añadir lista completa de ontologías

# TO DO: Implementar consulta de busqueda sin ontología o concepto

# TO DO: Consulta de conceptos por PMCID
# MATCH (article:bibo__Document)<-[:aoc__annotatesResource]-(concept:aot__ExactQualifier)-[:aoc__hasTopic]->(ontology:n4sch__Class) WHERE article.bibo__pmid[0] = '33331612' WITH  article,ontology,concept
# RETURN DISTINCT article.bibo__pmid[0] AS PMC_ID,ontology.dct__source[0] AS Ontología,collect(concept.aoc__body[0]) AS Concepto limit 100

# TO DO: CONSULTA POR PMCID, AGRUPANDO CONCEPTOS POR ONTOLOGÍAS
# MATCH (article:bibo__Document)<-[:aoc__annotatesResource]-(concept:aot__ExactQualifier)-[:aoc__hasTopic]->(ontology:n4sch__Class) WHERE article.bibo__pmid[0] = '33331612' WITH  article,ontology,concept
# RETURN DISTINCT article.bibo__pmid[0] AS PMC_ID,ontology.dct__source[0] AS Ontología,collect(concept.aoc__body[0]) AS Concepto limit 100

# TO DO: //CONSULTA POR CONCEPTO ORDENADA POR FECHA MÁS RECIENTE
# MATCH (article:bibo__Document)<-[:aoc__annotatesResource]-(concept:aot__ExactQualifier)-[:aoc__hasTopic]->(ontology:n4sch__Class)
# MATCH (author:foaf__Person)<-[]-(:rdf__Seq)<-[:bibo__authorList]-(article)-[:dct__publisher]->(organization:foaf__Organization)
# WHERE concept.aoc__body[0] = 'SYSTEMATIC REVIEW'
# WITH collect(distinct author.foaf__name[0]) AS Autores,article,ontology,organization,concept
# RETURN DISTINCT
# article.bibo__pmid[0] AS PMC_ID, article.dct__title[0] AS Título,article.dct__description[0] as Tipo,
# concept.aoc__body[0] AS Concepto,ontology.dct__source[0] AS Ontología,Autores,organization.foaf__name[0] AS Organización,
# article.bibo__shortDescription AS Palabras_Clave,article.dct__created[0] as Fecha_de_publicación,article.bibo__abstract[0] as Abstract ORDER BY article.dct__created[0] DESC Limit 100

def paper_list(request):
    print("Request: ")
    ontologies = ['SNOMEDCT', 'OCHV', 'PREMEDONTO', 'NCIT', 'IOBC', 'HL7', 'COVID-19', 'MESH', 'CIDO', 'CODO', 'HPIO', 'IDO-COVID-19', 'VO', 'COVIDCRFRAPID', 'BAO']
    ontology = request.GET.get('ontology')
    if not ontology or ontology == '' or ontology == 'ALL':
        n = rd.randint(0, len(ontologies) - 1)
        ontology = ontologies[n]
    limit = request.GET.get('limit')
    if not limit or limit == '':
        limit = rd.randint(25, 30)
    # Consulta Neo4j para recuperar todos los nodos de tipo Paper
    query = "MATCH (article:bibo__Document)<-[:aoc__annotatesResource]-(concept:aot__ExactQualifier)-[:aoc__hasTopic]->(ontology:n4sch__Class) \
            MATCH (author:foaf__Person)<-[]-(:rdf__Seq)<-[:bibo__authorList]-(article)-[:dct__publisher]->(organization:foaf__Organization) \
            WHERE ontology.dct__source[0] ='" + ontology + "' WITH collect(distinct author.foaf__name[0]) AS Autores,article,ontology,organization \
            RETURN DISTINCT article.bibo__pmid[0] AS PMC_ID, article.dct__title[0] AS Título,article.dct__description[0] as Tipo,ontology.dct__source[0] AS Ontología,Autores,organization.foaf__name[0] \
            AS Organización,article.bibo__shortDescription AS Palabras_Clave,article.dct__created[0] as Fecha_de_publicación,article.bibo__abstract[0] as Abstract LIMIT " + str(limit)
    results, meta = db.cypher_query(query)
    
    papers = [{'id': rec[0],
                'title': rec[1],
                'subtitle': 'This is the subtitle',
                'article_type': rec[2],
                'ontology': rec[3],
                'authors': [{'full_name': author} for author in rec[4]],
                'organization': rec[5],
                'key_words': rec[6],
                'published_date': rec[7],
                'published_year': (rec[7].split(' ')[0]).split('-')[2] if (rec[7] and len(rec[7]) == 19) else None,
                'abstract': rec[8],
              } for rec in results]

    """ return render(request, 'paper_list.html', {'papers': papers}) """
    return JsonResponse(papers, safe=False)

# MATCH (article:bibo__Document)<-[:aoc__annotatesResource]-(concept:aot__ExactQualifier)-[:aoc__hasTopic]->(ontology:n4sch__Class) WHERE article.bibo__pmid[0] = '33331612' WITH  article,ontology,concept
# RETURN DISTINCT article.bibo__pmid[0] AS PMC_ID,ontology.dct__source[0] AS Ontología,collect(concept.aoc__body[0]) AS Concepto limit 100

def viewsPMCID (request):
    pmcid = request.GET.get('pmcid')
    if not pmcid or pmcid == '':
        return JsonResponse({'error': 'No se ha especificado el identificador del artículo'}, safe=False)
    query = "MATCH (article:bibo__Document)<-[:aoc__annotatesResource]-(concept:aot__ExactQualifier)-[:aoc__hasTopic]->(ontology:n4sch__Class) WHERE article.bibo__pmid[0] = '"+ pmcid +"' WITH  article,ontology,concept RETURN DISTINCT article.bibo__pmid[0] AS PMC_ID,ontology.dct__source[0] AS Ontología,collect(concept.aoc__body[0]) AS Concepto limit 100"
    results, meta = db.cypher_query(query)
    concepts = [{'id': rec[0],
                'ontology': rec[1],
                'concepts': rec[2],
              } for rec in results]
    return JsonResponse(concepts, safe=False)