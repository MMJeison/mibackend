
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
    PMCIDS = ["32837492",
      "32705994",
      "33032629",
      "32549076",
      "32569835",
      "32773850",
      "32677557",
      "32792322",
      "32989380",
      "33287080",
      "32843866",
      "33493188",
      "33163146",
      "32638025",
      "32912768",
      "33240837",
      "32680889",
      "29955859",
      "32363138",
      "32882347",
      "32536944",
      "32840492",
      "32247928",
      "32705485",
      "32780574",
      "32439956",
      "33384521",
      "32574184",
      "33376490",
      "32613654",
      "32835684",
      "32988991",
      "33274726",
      "32171058",
      "33013254",
      "33505860",
      "32410245",
      "15717217",
      "12757561",
      "32963508",
      "32838031",
      "33144275",
      "33519017",
      "33255672",
      "32834884",
      "33234656",
      "32257511",
      "32593116",
      "32488583",
      "33464206",
      "32830471",
      "32327946",
      "32834655",
      "33643929",
      "32769754",
      "33318721",
      "32412403",
      "32780149",
      "33212953",
      "32646656",
      "32305069",
      "32986741",
      "33063226",
      "32655724",
      "32580969",
      "33510633",
      "30935725",
      "33603709",
      "33606157",
      "33250552",
      "33163951",
      "33594628",
      "33001869",
      "32287412",
      "33244357",
      "32837287",
      "16028157",
      "32943211",
      "32967646",
      "22000601",
      "32616970",
      "33101676",
      "33088099",
      "33257496",
      "32795831",
      "33442303",
      "33352802",
      "32891255",
      "33318716",
      "32821920",
      "33041374",
      "33246864",
      "32913284",
      "33317745",
      "33603349",
      "32838064",
      "32445083",
      "30573330",
      "23810340",
      "33162696"]
    ontologies = ['SNOMEDCT', 'OCHV', 'PREMEDONTO', 'NCIT', 'IOBC', 'HL7', 'COVID-19', 'MESH', 'CIDO', 'CODO', 'HPIO', 'IDO-COVID-19', 'VO', 'COVIDCRFRAPID', 'BAO']
    papers = []
    for pmcid in PMCIDS:
        query = "MATCH (article:bibo__Document)<-[:aoc__annotatesResource]-()-[:aoc__hasTopic]->(ontology:n4sch__Class) MATCH (author:foaf__Person)-[:foaf__publications]->(article)-[:dct__publisher]->(organization:foaf__Organization) WHERE article.bibo__pmid[0] = '"+pmcid+"' WITH collect(DISTINCT author.foaf__name[0]) AS Autores,article,collect(distinct ontology.dct__source[0]) AS Ontología,organization RETURN DISTINCT article.bibo__pmid[0] AS PMC_ID,article.bibo__doi[0] AS DOI,article.dct__title[0] AS Título,article.bibo__abstract[0] as Abstract,article.dct__description[0] as Tipo,Ontología,Autores,organization.foaf__name[0] AS Organización,article.dct__created[0] as Fecha_de_publicación"
        rec, meta = db.cypher_query(query)
        #PMC_ID	DOI	Título	Abstract	Tipo	Ontología	Autores	Organización	Fecha_de_publicación
        rec = rec[0]
        paper = {'pmcid': rec[0],
                'doi': rec[1],
                'title': rec[2],
                'abstract': rec[3],
                'paper_type': rec[4],
                'ontologies': rec[5],
               'authors': [{'full_name': author} for author in rec[6]],
                'journal': rec[7],
                'published_date': (rec[7].split(' ')[0]) if (rec[7] and len(rec[7]) == 19) else '2010-01-01',
              }
        papers.append(paper)
    return JsonResponse(papers, safe=False)

def viewsPMCID (request):
    pmcid = request.GET.get('pmcid')
    pmcid = '33331612'
    if not pmcid or pmcid == '':
        return JsonResponse({'error': 'No se ha especificado el identificador del artículo'}, safe=False)
    query = "MATCH (article:bibo__Document)<-[:aoc__annotatesResource]-(concept:aot__ExactQualifier)-[:aoc__hasTopic]->(ontology:n4sch__Class) WHERE article.bibo__pmid[0] = '"+ pmcid +"' WITH  article,ontology,concept RETURN DISTINCT article.bibo__pmid[0] AS PMC_ID,ontology.dct__source[0] AS Ontología,collect(concept.aoc__body[0]) AS Concepto limit 100"
    results, meta = db.cypher_query(query)
    concepts = [{'id': rec[0],
                'ontology': rec[1],
                'concepts': rec[2],
              } for rec in results]
    return JsonResponse(concepts, safe=False)

# TO DO: CONSULTA POR PMCID, AGRUPANDO CONCEPTOS POR ONTOLOGÍAS
# MATCH (article:bibo__Document)<-[:aoc__annotatesResource]-(concept:aot__ExactQualifier)-[:aoc__hasTopic]->(ontology:n4sch__Class) WHERE article.bibo__pmid[0] = '33331612' WITH  article,ontology,concept
# ¡RETURN DISTINCT article.bibo__pmid[0] AS PMC_ID,ontology.dct__source[0] AS Ontología,collect(concept.aoc__body[0]) AS Concepto limit 100

def viewsPMCIDOntology (request):
    pmcid = request.GET.get('pmcid')
    pmcid = '33331612'
    if not pmcid or pmcid == '':
        return JsonResponse({'error': 'No se ha especificado el identificador del artículo'}, safe=False)
    query = "MATCH (article:bibo__Document)<-[:aoc__annotatesResource]-(concept:aot__ExactQualifier)-[:aoc__hasTopic]->(ontology:n4sch__Class) WHERE article.bibo__pmid[0] = '"+ pmcid +"' WITH  article,ontology,concept ¡RETURN DISTINCT article.bibo__pmid[0] AS PMC_ID,ontology.dct__source[0] AS Ontología,collect(concept.aoc__body[0]) AS Concepto limit 100"
    results, meta = db.cypher_query(query)
    papers = [{'id': rec[0],
                'title': rec[1],
                'subtitle': 'This is the subtitle',
                'article_type': rec[2],
                'concept': rec[3],
                'ontology': rec[4],
                'authors': [{'full_name': author} for author in rec[5]],
                'organization': rec[6],
                'key_words': rec[7],
                'published_date': rec[8],
                'published_year': (rec[8].split(' ')[0]).split('-')[2] if (rec[8] and len(rec[8]) == 19) else None,
                'abstract': rec[9],
              } for rec in results]
    return JsonResponse(papers, safe=False)

#CONSULTA DE CONCEPTOS AGRUPADOS CON CONTEOS AGRUPADOS POR ARTICULO
#MATCH (article:bibo__Document)<-[:aoc__annotatesResource]-(concept:aot__ExactQualifier)
#RETURN DISTINCT article.bibo__pmid[0] as PMCID,collect(concept.aoc__body[0]) AS Concepto,collect(concept.biotea__tf[0]) AS Conteo

def viewsPMCIDConcept (request):
    pmcid = request.GET.get('pmcid')
    pmcid = '33331612'
    if not pmcid or pmcid == '':
        return JsonResponse({'error': 'No se ha especificado el identificador del artículo'}, safe=False)
    query = "MATCH (article:bibo__Document)<-[:aoc__annotatesResource]-(concept:aot__ExactQualifier) WHERE article.bibo__pmid[0] = '"+ pmcid +"' RETURN DISTINCT article.bibo__pmid[0] as PMCID,collect(DISTINCT concept.aoc__body[0]) AS Concepto,collect(concept.biotea__tf[0]) AS Conteo"
    results, meta = db.cypher_query(query)
    papers = [{'id': rec[0],
                'concept': rec[1],
                'count': rec[2],
              } for rec in results]
    return JsonResponse(papers, safe=False)

#//CONSULTA POR PMCID, AGRUPANDO CONCEPTOS POR ONTOLOGÍAS
#MATCH (article:bibo__Document)<-[:aoc__annotatesResource]-(concept:aot__ExactQualifier)-[:aoc__hasTopic]->(ontology:n4sch__Class) 
#WHERE article.bibo__pmid[0] = '33331612' WITH  article,ontology,concept
#RETURN DISTINCT article.bibo__pmid[0] AS PMC_ID,ontology.dct__source[0] AS Ontología,collect(concept.aoc__body[0]) AS Concepto limit 100

def viewsPMCIDOntologyConcept (request):
    pmcid = request.GET.get('pmcid')
    pmcid = '33331612'
    if not pmcid or pmcid == '':
        return JsonResponse({'error': 'No se ha especificado el identificador del artículo'}, safe=False)
    query = "MATCH (article:bibo__Document)<-[:aoc__annotatesResource]-(concept:aot__ExactQualifier)-[:aoc__hasTopic]->(ontology:n4sch__Class) WHERE article.bibo__pmid[0] = '"+ pmcid +"' WITH  article,ontology,concept RETURN DISTINCT article.bibo__pmid[0] AS PMC_ID,ontology.dct__source[0] AS Ontología,collect(concept.aoc__body[0]) AS Concepto limit 100"
    results, meta = db.cypher_query(query)
    papers = [{'id': rec[0],
                'ontology': rec[1],
                'concepts': rec[2],
              } for rec in results]
    return JsonResponse(papers, safe=False)

#//CONSULTA POR CONCEPTO ORDENADA POR FECHA MÁS RECIENTE
#MATCH (article:bibo__Document)<-[:aoc__annotatesResource]-(concept:aot__ExactQualifier)-[:aoc__hasTopic]->(ontology:n4sch__Class)
#MATCH (author:foaf__Person)<-[]-(:rdf__Seq)<-[:bibo__authorList]-(article)-[:dct__publisher]->(organization:foaf__Organization)
#WHERE concept.aoc__body[0] = 'SYSTEMATIC REVIEW'
#WITH collect(distinct author.foaf__name[0]) AS Autores,article,ontology,organization,concept
#RETURN DISTINCT article.bibo__pmid[0] AS PMC_ID, article.dct__title[0] AS Título,article.dct__description[0] as Tipo,
#concept.aoc__body[0] AS Concepto,ontology.dct__source[0] AS Ontología,Autores,organization.foaf__name[0] AS Organización,
#article.bibo__shortDescription AS Palabras_Clave,article.dct__created[0] as Fecha_de_publicación,article.bibo__abstract[0] as Abstract ORDER BY article.dct__created[0] DESC Limit 100

def viewsConcept (request):
    concept = request.GET.get('concept')
    concept = 'SYSTEMATIC REVIEW'
    if not concept or concept == '':
        return JsonResponse({'error': 'No se ha especificado el concepto'}, safe=False)
    query = "MATCH (article:bibo__Document)<-[:aoc__annotatesResource]-(concept:aot__ExactQualifier)-[:aoc__hasTopic]->(ontology:n4sch__Class) MATCH (author:foaf__Person)<-[]-(:rdf__Seq)<-[:bibo__authorList]-(article)-[:dct__publisher]->(organization:foaf__Organization) WHERE concept.aoc__body[0] = '"+ concept +"' WITH collect(distinct author.foaf__name[0]) AS Autores,article,ontology,organization,concept RETURN DISTINCT article.bibo__pmid[0] AS PMC_ID, article.dct__title[0] AS Título,article.dct__description[0] as Tipo,concept.aoc__body[0] AS Concepto,ontology.dct__source[0] AS Ontología,Autores,organization.foaf__name[0] AS Organización,article.bibo__shortDescription AS Palabras_Clave,article.dct__created[0] as Fecha_de_publicación,article.bibo__abstract[0] as Abstract ORDER BY article.dct__created[0] DESC Limit 100"
    results, meta = db.cypher_query(query)
    papers = [{'id': rec[0],
                'title': rec[1],
                'subtitle': 'This is the subtitle',
                'article_type': rec[2],
                'concept': rec[3],
                'ontology': rec[4],
                'authors': [{'full_name': author} for author in rec[5]],
                'organization': rec[6],
                'key_words': rec[7],
                'published_date': rec[8],
                'published_year': (rec[8].split(' ')[0]).split('-')[2] if (rec[8] and len(rec[8]) == 19) else None,
                'abstract': rec[9],
              } for rec in results]
    return JsonResponse(papers, safe=False)

#//CONSULTA POR CONCEPTO SIN METADATOS ORDENADO POR CONTEOS
#MATCH (article:bibo__Document)<-[:aoc__annotatesResource]-(concept:aot__ExactQualifier)-[:aoc__hasTopic]->(ontology:n4sch__Class) 
#WHERE concept.aoc__body[0] = 'SYSTEMATIC REVIEW' RETURN article.bibo__pmid[0] as PMCID,ontology.dct__source[0] AS Ontología,
#concept.aoc__body[0] AS Concepto,concept.biotea__tf[0] AS Conteo ORDER BY concept.biotea__tf[0] DESC

def viewsConceptCount (request):
    concept = request.GET.get('concept')
    concept = 'SYSTEMATIC REVIEW'
    if not concept or concept == '':
        return JsonResponse({'error': 'No se ha especificado el concepto'}, safe=False)
    query = "MATCH (article:bibo__Document)<-[:aoc__annotatesResource]-(concept:aot__ExactQualifier)-[:aoc__hasTopic]->(ontology:n4sch__Class) WHERE concept.aoc__body[0] = '"+ concept +"' RETURN article.bibo__pmid[0] as PMCID,ontology.dct__source[0] AS Ontología,concept.aoc__body[0] AS Concepto,concept.biotea__tf[0] AS Conteo ORDER BY concept.biotea__tf[0] DESC"
    results, meta = db.cypher_query(query)
    papers = [{'id': rec[0],
                'ontology': rec[1],
                'concept': rec[2],
                'count': rec[3],
              } for rec in results]
    return JsonResponse(papers, safe=False)