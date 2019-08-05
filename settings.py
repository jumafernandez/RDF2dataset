from pathlib import Path

HDT_FILE = './dbpedia-3.8-en.hdt'

WORK_DIR = '/tmp/'

DATASET_FILE = Path(WORK_DIR) / 'dataset.csv'
OUTPUT_DATASET_FILE = Path(WORK_DIR) / 'output_dataset.csv'
STATS_FILE = Path(WORK_DIR) / 'statistics.csv'

PREDICATES_EXCLUDED = [
    "abstract", "thumbnail", "wikiPageExternalLink", "wikiPageExternalLink",
    "wikiPageID", "wikiPageInterLanguageLink", "wikiPageRevisionID",
    "wikiPageWikiLink", "website", "wikiPageUsesTemplate",
    "Template:Infobox_university", "owl#sameAs", "prov#wasDerivedFrom",
    "depiction", "homepage", "isPrimaryTopicOf", "imageName", "imageSize",
    "title", "titlestyle", "Template:Infobox_US_university_ranking",
    "Template:Navboxes", "subject", "point", "rdf-schema#comment",
    "rdf-schema#label"]

# Proporcion Faltantes, se eliminan los que no tengan esta cota minima de datos:
RATIO = 0.3

# Consulta
# Ontología: http://mappings.dbpedia.org/server/ontology/classes/
QUERY = "http://dbpedia.org/ontology/University"
#QUERY = "http://dbpedia.org/ontology/Film"
#QUERY = "http://dbpedia.org/ontology/Actor"
#QUERY = "http://dbpedia.org/ontology/HistoricPlace"


try:
    from settings_local import *
except ImportError:
    pass
