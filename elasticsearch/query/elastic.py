from elasticsearch import Elasticsearch

# Connexion à Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# Fonction pour créer un index
def create_index(index_name):
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)
        print(f"L'index '{index_name}' a été créé.")
    else:
        print(f"L'index '{index_name}' existe déjà.")

# Fonction pour indexer un document
def index_document(index_name, doc_id, document):
    res = es.index(index=index_name, id=doc_id, body=document)
    print(f"Document indexé avec ID: {doc_id}")

# Fonction pour chercher un document
def search_document(index_name, query):
    res = es.search(index=index_name, body={"query": query})
    for hit in res['hits']['hits']:
        print(hit["_source"])

# Créer un index
create_index("adresses_postales")

# Indexer un document (exemple de document JSON)
document = {
    "nom": "Jean Dupont",
    "adresse": "123 Rue de l'Église",
    "code_postal": "75001",
    "ville": "Paris"
}
index_document("adresses_postales", 1, document)

# Rechercher un document
search_query = {"match": {"nom": "Jean Dupont"}}
search_document("adresses_postales", search_query)