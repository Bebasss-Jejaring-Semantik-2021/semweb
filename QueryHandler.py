import rdflib
from SPARQLWrapper import SPARQLWrapper, JSON 


class MovieQueryHandler():
    def __init__(self):
        self.localq = """PREFIX tkp: <http://tkjentik.com/property/>
            PREFIX dbo: <http://dbpedia.org/ontology/> 
            SELECT ?dbpedia ?title ?type ?date ?year ?rating ?duration ?desc (GROUP_CONCAT(distinct ?director1; SEPARATOR=", ") AS ?directors) (GROUP_CONCAT(distinct ?cast1; SEPARATOR=", ") AS ?casts) (GROUP_CONCAT(distinct ?country1; SEPARATOR=", ") AS ?countries) (GROUP_CONCAT(distinct ?genre1; SEPARATOR=", ") AS ?genres)
            WHERE {{
                ?movie tkp:title "{}".
                OPTIONAL {{?movie tkp:dbpedia ?dbpedia .}}
                OPTIONAL {{?movie tkp:title ?title .}}
                OPTIONAL {{?movie tkp:type ?type .}}
                OPTIONAL {{?movie tkp:director ?director .}}
                OPTIONAL {{?movie tkp:cast ?cast .}}
                OPTIONAL {{?movie tkp:country ?country .}}
                OPTIONAL {{?movie tkp:date_added ?date .}}
                OPTIONAL {{?movie tkp:release_year ?year .}}
                OPTIONAL {{?movie tkp:rating ?rating .}}
                OPTIONAL {{?movie tkp:duration ?duration .}}
                OPTIONAL {{?movie tkp:genre ?genre .}}
                OPTIONAL {{?movie tkp:description ?desc .}}
                bind ( coalesce(?director,'') as ?director1 )
                bind ( coalesce(?cast,'') as ?cast1 )
                bind ( coalesce(?genre,'') as ?genre1 )
                bind ( coalesce(?country,'') as ?country1 )
            }}"""

        self.dbq = """PREFIX dbo: <http://dbpedia.org/ontology/>
            SELECT DISTINCT ?abstract ?distributor {{
                OPTIONAL{{ <{0}> dbo:abstract ?abstract .}}
                OPTIONAL{{ <{0}> dbo:distributor ?distributor .}}
                filter(langMatches(lang(?abstract), "en"))
            }}LIMIT 1"""

        self.graph = rdflib.Graph()
        self.graph.parse("disney.ttl", format="ttl")

    def query(self, uri):
        localq = self.localq.format(uri)
        q_result = list(self.graph.query(localq))
        try:
            res = q_result[0].asdict()
            if "dbpedia" not in res:
                return q_result, None

            dbq = self.dbq.format(res["dbpedia"].toPython())
            dbpedia = SPARQLWrapper("http://dbpedia.org/sparql")
            dbpedia.setQuery(dbq)
            dbpedia.setReturnFormat(JSON)
            results = dbpedia.query().convert()
            return q_result, results["results"]["bindings"]
        except:
            return q_result, None


class SearchQueryHandler():
    def __init__(self):
        self.searchq = """PREFIX tkp: <http://tkjentik.com/property/>
            SELECT DISTINCT ?title ?movie WHERE {{
            ?movie tkp:title ?title.
            FILTER(regex(str(?title), {}, "i")) .
            }}
            """
        self.graph = rdflib.Graph()
        self.graph.parse("disney.ttl", format="ttl")

    def query(self, title):
        searchq = self.searchq.format('"' + title + '"')
        result = list(self.graph.query(searchq))
        return result
