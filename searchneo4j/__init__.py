# Importar los modelos creados con neomodel
# from searchneo4j.models import Paper, Author, Institution, ExternalId, Ontology, Subject

# Registrar los modelos en neomodel
from neomodel import config
config.DATABASE_URL = 'bolt://neo4j:pass@localhost:7688'
config.ENCRYPTED_CONNECTION = False
# config.AUTO_INSTALL_LABELS = True
# config.AUTO_INSTALL_PROPERTIES = True
# config.AUTO_INDEX_NODES = True
# config.AUTO_INDEX_RELATIONSHIPS = True

# Paper.registry.create_unique_constraint('Paper', 'id')
# Author.registry.create_unique_constraint('Author', 'id')
# Institution.registry.create_unique_constraint('Institution', 'id')
# ExternalId.registry.create_unique_constraint('ExternalId', 'id')
# Ontology.registry.create_unique_constraint('Ontology', 'acronym')
# Subject.registry.create_unique_constraint('Subject', 'name')