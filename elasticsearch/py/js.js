const { Client } = require('@elastic/elasticsearch');
const client = new Client({ node: 'http://localhost:9200' });

// Fonction pour créer un index
async function createIndex(indexName) {
  const exists = await client.indices.exists({ index: indexName });
  if (!exists.body) {
    await client.indices.create({ index: indexName });
    console.log(`Index '${indexName}' créé.`);
  } else {
    console.log(`Index '${indexName}' existe déjà.`);
  }
}

// Fonction pour indexer un document
async function indexDocument(indexName, docId, document) {
  await client.index({
    index: indexName,
    id: docId,
    body: document
  });
  console.log(`Document indexé avec ID: ${docId}`);
}

// Fonction pour chercher un document
async function searchDocument(indexName, query) {
  const { body } = await client.search({
    index: indexName,
    body: {
      query: query
    }
  });
  body.hits.hits.forEach(hit => console.log(hit._source));
}

// Créer un index
createIndex('adresses_postales');

// Exemple de document JSON
const document = {
  nom: 'Jean Dupont',
  adresse: '123 Rue de l\'Église',
  code_postal: '75001',
  ville: 'Paris'
};

// Indexer un document
indexDocument('adresses_postales', 1, document);

// Rechercher un document
const searchQuery = { match: { nom: 'Jean Dupont' } };
searchDocument('adresses_postales', searchQuery);
