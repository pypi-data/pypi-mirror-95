# -*- coding: utf-8 -*-

import spotlight
import time


from orbis_eval.plugins.aggregation.dbpedia_entity_types import Main as dbpedia_entity_types
from orbis_eval.core.base import AggregationBaseClass


import logging
logger = logging.getLogger(__name__)


class Main(AggregationBaseClass):

    def query(self, item):

        # old url:
        # client = f"http://model.dbpedia-spotlight.org/{self.config['aggregation']['service']['language']}/annotate"

        # new url:
        client = f"https://api.dbpedia-spotlight.org/{self.config['aggregation']['service']['language']}/annotate"

        only_pol_filter = {
            'policy': 'whitelist',
            'types': 'DBpedia:Person, DBpedia:Place, DBpedia:Location, DBpedia:Organisation, Http://xmlns.com/foaf/0.1/Person',
            'coreferenceResolution': True
        }
        text = item['corpus']

        time.sleep(2)
        try:
            response = spotlight.annotate(client, text=text, filters=only_pol_filter)
        except Exception as exception:
            logger.error(f"Query failed: {exception}")
            response = None
        return response

    def map_entities(self, response, item):
        entities = []

        if not response:
            return None

        if response:
            for idx, item in enumerate(response):
                item["key"] = item["URI"]
                item["key"] = item["key"].replace("http://en.wikipedia.org/wiki/", "http://dbpedia.org/resource/")
                item["key"] = item["key"].replace("http://de.dbpedia.org/resource/", "http://dbpedia.org/resource/")
                item = self.get_type(item)
                item["document_start"] = int(item["offset"])
                item["document_end"] = int(item["offset"]) + len(item["surfaceForm"])
                entities.append(item)
        return entities

    def get_type(self, item):
        places = ["place", "location", "settlement"]
        persons = ['http://xmlns.com/foaf/0.1/person', 'person']
        orgs = ["organisation"]
        item["entity_type"] = "undefined"

        for place in places:
            if place in item["types"].lower():
                item["entity_type"] = dbpedia_entity_types.normalize_entity_type("location")
        for person in persons:
            if person in item["types"].lower():
                item["entity_type"] = dbpedia_entity_types.normalize_entity_type("person")
        for org in orgs:
            if org in item["types"].lower():
                item["entity_type"] = dbpedia_entity_types.normalize_entity_type("organisation")
        return item
