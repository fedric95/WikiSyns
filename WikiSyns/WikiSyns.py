from SPARQLWrapper import SPARQLWrapper
from SPARQLWrapper import JSON

import requests
import pandas as pd
import sys
import numpy as np


class WikipediaSyns:

  """
  Return all redirects to the given page.
  It is based on the API:Query module of MediaWiki, https://www.mediawiki.org/wiki/API:Query
  """
  def redirects_to(self, name):
      S = requests.Session()

      PARAMS = {
          "action": "query",
          "format": "json",
          "titles": name,
          "prop": "redirects"
      }

      R = S.get(url=self.URL, params=PARAMS, verify=True)
      DATA = R.json()
      PAGES = DATA["query"]["pages"]

      
      names = []
      for k, v in PAGES.items():
          if('redirects' in v.keys()):
              for re in v["redirects"]:
                  names.append(re['title'])
                  
                  
      names = list(set(names))
      return(names)

  
  """
  Get the redirection made accessing the given page. Ex: USA -> United_States
  It is based on the API:Query module of MediaWiki, https://www.mediawiki.org/wiki/API:Query
  """
  def resolve_redirect(self, name):

      S = requests.Session()
      PARAMS = {
          "action": "query",
          "redirects": True,
          "titles": name,
          "format":'json'
      }

      R = S.get(url=self.URL, params=PARAMS, verify=True)
      DATA = R.json()
      PAGES = DATA["query"]["pages"]
      names = []
      for k, v in PAGES.items():
          if(k!='-1' and 'title' in v.keys()):
              names.append(v['title'])

      names = list(set(names))
      return(names)


  def get_syns(self, name):

      names = []

      names.extend(self.resolve_redirect(name))
      names.extend(self.redirects_to(name))
      names.extend([name])

      names = list(set(names))
      return(names)

  def __init__(self):
      self.URL = "https://en.wikipedia.org/w/api.php"
      
      
      
class WikidataEntities:
  
  def __init__(self):
    self.URL = 'https://query.wikidata.org/sparql'

  def get_results(self, endpoint_url, query):
      user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
      sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
      sparql.setQuery(query)
      sparql.setReturnFormat(JSON)
      return (sparql.query().convert())
  
  def get_entities(self, instancetype):
    query = """
    SELECT  ?val WHERE {
        ?val wdt:P31 {instancetype} .
    }"""
    query = query.replace('{instancetype}', instancetype)
    results = self.get_results(self.URL, query)

    ents = []
    for result in results["results"]["bindings"]:
      ents.append('<'+result['val']['value']+'>')
    return(ents)
  
  #def get_property(self, entity, property, language):
  #
  #  if(language is not None):
  #    query = """
  #    SELECT ?val WHERE {
  #        {entity} {property} ?val .
  #        FILTER (LANG(?val) = "{language}")
  #    }"""
  #    query = query.replace('{language}', language)
  #  else:
  #    query = """
  #    SELECT ?val WHERE {
  #        {entity} {property} ?val .
  #    }"""
  #  query = query.replace('{entity}', entity)
  #  query = query.replace('{property}', property)
  #
  #  results = self.get_results(self.URL, query)
  #  values = []
  #  for result in results["results"]["bindings"]:
  #    values.append(result['val']['value'])
  #
  #  return(values)
  def get_entities_stock_symbols(self, instancetype):
    query = """
    SELECT ?entity ?val WHERE {
        ?entity wdt:P31 {instancetype} .
        ?entity p:P414 ?statement .
        ?statement pq:P249 ?val .
    }"""
    query = query.replace('{instancetype}', instancetype)

    results = self.get_results(self.URL, query)
    values = []
    for result in results["results"]["bindings"]:
      values.append({'ent':result['entity']['value'], 'val': result['val']['value']})

    return(values)
    


  def get_entities_property(self, instancetype, property, language):
    if(language is not None):
      query = """
      SELECT ?entity ?val WHERE {
          ?entity wdt:P31 {instancetype} .
          ?entity {property} ?val .
          FILTER (LANG(?val) = "{language}")
      }"""
      query = query.replace('{language}', language)
    else:
      query = """
      SELECT ?entity ?val WHERE {
          ?entity wdt:P31 {instancetype} .
          ?entity {property} ?val .
      }"""
    query = query.replace('{instancetype}', instancetype)
    query = query.replace('{property}', property)

    results = self.get_results(self.URL, query)
    values = []
    for result in results["results"]["bindings"]:
      values.append({'ent':result['entity']['value'], 'val': result['val']['value']})

    return(values)



  def get_syns(self, instancetype, language, wikipedia=True):
    wp = WikipediaSyns()

    res_label = self.get_entities_property(instancetype, 'rdfs:label', language)
    res_altLabel = self.get_entities_property(instancetype, 'skos:altLabel', language)
    res_stockSymbol = self.get_entities_stock_symbols(instancetype)
    
    if(wikipedia==True):
      res_wiki = []
      for r in res_label:
        wp_syns = wp.get_syns(r['val'])
        for wp_syn in wp_syns:
          res_wiki.append({'ent': r['ent'], 'val': wp_syn})
      res_altLabel = res_altLabel+res_wiki
    
    res_altLabel = res_altLabel+res_stockSymbol

    data_syns = []
    for r in (res_label+res_altLabel):
      data_syns.append([r['ent'], r['val']])
    
    
    res_desc = self.get_entities_property(instancetype, 'schema:description', language)
    data_descs = []
    for r in res_desc:
      data_descs.append([r['ent'], r['val']])


    data_syns = pd.DataFrame(np.array(data_syns), columns=['entity', 'value']).drop_duplicates()
    data_descs = pd.DataFrame(np.array(data_descs), columns=['entity', 'desc']).drop_duplicates()
    


    res = data_syns.merge(data_descs, how='left', on='entity')
    return(res)
