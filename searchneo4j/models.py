from neomodel import Q
from neomodel import db

def run_query(query):
    results, meta = db.cypher_query(query)
    
    return results
