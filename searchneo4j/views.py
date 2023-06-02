
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from neomodel import Q
from neomodel import db
import random as rd
import json
# from neomodel import config
# Create your views here.}
# import idpapers

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
    # leamos la lista de PMCIDS del achivo .json que se este directorio
    PMCIDS = [
    "32837492",
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
    "33162696",
    "32315667",
    "32428041",
    "33234111",
    "32541234",
    "33041632",
    "32577428",
    "33186795",
    "33466895",
    "33238523",
    "15882360",
    "33106788",
    "32998916",
    "33195316",
    "32903905",
    "32404975",
    "32747672",
    "32313807",
    "32299201",
    "33575405",
    "33163000",
    "32837868",
    "33195595",
    "32564028",
    "33304316",
    "33166301",
    "32790752",
    "33082924",
    "32973584",
    "32502333",
    "33558153",
    "32838033",
    "33012971",
    "33410760",
    "33294588",
    "32393774",
    "32475827",
    "33225870",
    "32952300",
    "32699679",
    "32247013",
    "32389541",
    "33218215",
    "31401954",
    "32742305",
    "15573058",
    "32576319",
    "33195626",
    "33429988",
    "32142626",
    "33520610",
    "33332295",
    "31873811",
    "32416984",
    "32164053",
    "33132575",
    "32695959",
    "33623742",
    "32948990",
    "33354067",
    "32494911",
    "33546500",
    "33404813",
    "32404630",
    "31240121",
    "32527596",
    "33013243",
    "32678897",
    "33581925",
    "33471776",
    "33358480",
    "21761137",
    "32875502",
    "33642896",
    "32288095",
    "30284042",
    "33422205",
    "32112336",
    "33337529",
    "32916836",
    "31869359",
    "33519333",
    "27230822",
    "33373680",
    "32886958",
    "32846654",
    "15814187",
    "33275982",
    "33352320",
    "32439306",
    "33540788",
    "32713621",
    "20680674",
    "32214079",
    "32948443",
    "33194223",
    "33442167",
    "33101826",
    "33029562",
    "15178195",
    "32934635",
    "32695050",
    "32842988",
    "33472772",
    "32734516",
    "33041493",
    "33519045",
    "33193772",
    "33307158",
    "33271861",
    "32999949",
    "33396275",
    "33233447",
    "33225100",
    "33260201",
    "33585156",
    "32734936",
    "32392096",
    "33114676",
    "32529040",
    "33377665",
    "33078089",
    "32963423",
    "32741195",
    "32134205",
    "32536738",
    "32756382",
    "32959148",
    "33344608",
    "32867727",
    "33008097",
    "32697279",
    "32399942",
    "33169271",
    "33432292",
    "32680626",
    "32437022",
    "32804353",
    "21354628",
    "33051749",
    "26319169",
    "33532963",
    "31640591",
    "33560451",
    "32321654",
    "20180866",
    "32754465",
    "32160149",
    "33354062",
    "31995857",
    "33284783",
    "33418182",
    "32541352",
    "32785570",
    "32999856",
    "32836891",
    "32405517",
    "33570267",
    "33619426",
    "32590830",
    "31992846",
    "32921851",
    "31852635",
    "32313879",
    "32921800",
    "32838030",
    "32513515",
    "30423150",
    "16647790",
    "33038383",
    "32344809",
    "32660240",
    "33324574",
    "32874851",
    "32213786",
    "33606167",
    "33294591",
    "33425051",
    "33237892",
    "33643113",
    "32747164",
    "33485187",
    "33180027",
    "33580226",
    "33001872",
    "32322102",
    "32440660",
    "33642658",
    "32784498",
    "32690337",
    "32585864",
    "33261677",
    "32521041",
    "33462529",
    "32834378",
    "33147213",
    "32380891",
    "23803486",
    "33394120",
    "33138975",
    "32663797",
    "32542946",
    "32850809",
    "32395720",
    "33131500",
    "32214684",
    "33170799",
    "33531734",
    "33326924",
    "33623478",
    "33292566",
    "32589673",
    "32971323",
    "32865577",
    "33288420",
    "33091782",
    "33112126",
    "33557776",
    "19520475",
    "32834468",
    "32915873",
    "33610241",
    "31541215",
    "33282336",
    "33250545",
    "32790782",
    "17599315",
    "32904371",
    "33374748",
    "33269260",
    "33527786",
    "32836476",
    "33274541",
    "32651513",
    "33110402",
    "33157341",
    "32534458",
    "32837523",
    "32221729",
    "32921730",
    "33101539",
    "33223784",
    "32589799",
    "33496668",
    "31746222",
    "33262559",
    "33225098",
    "33270613",
    "33424145",
    "33535992",
    "32835088",
    "33558788",
    "32807895",
    "32239515",
    "33644499",
    "32367889",
    "33153482",
    "32787496",
    "32413713",
    "32247926",
    "32888112",
    "33218677",
    "32921870",
    "33362920",
    "32570084",
    "19515609",
    "32512826",
    "33236086",
    "33174963",
    "33109234",
    "33124935",
    "32333552",
    "33457497",
    "32801227",
    "32461245",
    "32754879",
    "32677113",
    "32816942",
    "33481925",
    "32622032",
    "32617365",
    "33572833",
    "32830041",
    "32350571",
    "33301725",
    "33303910",
    "33091762",
    "32736332",
    "33317015",
    "33320823",
    "32596806",
    "33585031",
    "32915252",
    "33311501",
    "33041631",
    "32458206",
    "33226861",
    "33364438",
    "33008491",
    "32837855",
    "32423791"
    ]
        
    ontologies = ['SNOMEDCT', 'OCHV', 'PREMEDONTO', 'NCIT', 'IOBC', 'HL7', 'COVID-19', 'MESH', 'CIDO', 'CODO', 'HPIO', 'IDO-COVID-19', 'VO', 'COVIDCRFRAPID', 'BAO']
    papers = []
    for pmcid in PMCIDS:
        query = "MATCH (article:bibo__Document)<-[:aoc__annotatesResource]-()-[:aoc__hasTopic]->(ontology:n4sch__Class) MATCH (author:foaf__Person)-[:foaf__publications]->(article)-[:dct__publisher]->(organization:foaf__Organization) WHERE article.bibo__pmid[0] = '"+pmcid+"' WITH collect(DISTINCT author.foaf__name[0]) AS Autores,article,collect(distinct ontology.dct__source[0]) AS Ontología,organization RETURN DISTINCT article.bibo__pmid[0] AS PMC_ID,article.bibo__doi[0] AS DOI,article.dct__title[0] AS Título,article.bibo__abstract[0] as Abstract,article.dct__description[0] as Tipo,Ontología,Autores,organization.foaf__name[0] AS Organización,article.dct__created[0] as Fecha_de_publicación"
        rec, meta = db.cypher_query(query)
        #PMC_ID	DOI	Título	Abstract	Tipo	Ontología	Autores	Organización	Fecha_de_publicación
        if len(rec) > 0:
            rec = rec[0]
            paper = {'pmcid': rec[0],
                    'doi': rec[1],
                    'title': rec[2],
                    'abstract': rec[3],
                    'paper_type': rec[4],
                    'ontologies': rec[5],
                    'authors': [{'full_name': author} for author in rec[6]],
                    'journal': rec[7],
                    'published_date': rec[8].split(' ')[0] if rec[8] else '01-01-2010',
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