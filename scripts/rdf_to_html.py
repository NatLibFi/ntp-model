"""
 Copyright 2021 University Of Helsinki (The National Library Of Finland)
 
 Licensed under the GNU, General Public License, Version 3.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     https://www.gnu.org/licenses/gpl-3.0.html
 
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

from rdflib import Graph, URIRef, Namespace, RDF, Literal
from rdflib.namespace import SKOS, XSD, OWL, DC, NamespaceManager
from lxml import etree, html
from urllib.parse import urldefrag
import argparse
import logging

HEADERS = {OWL.Class: 'Classes',
           OWL.ObjectProperty: 'Object Properties',
           OWL.DatatypeProperty: 'Datatype Properties',
           OWL.AnnotationProperty: 'Annotation Properties'}
           
TYPES = [OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty]

def add_sublement(element, tag, text=None):
    subelement = etree.SubElement(element, tag)
    if text:
        subelement.text = text
    return subelement    
        
class RDFtoHTML:

    def __init__(self):
        parser = argparse.ArgumentParser(description="Conversion of data model from RDF to HTML")
        parser.add_argument("-pl", "--pref_label",
            help="Property name for preferred labels e. g. skos:prefLabel", required=True)
        parser.add_argument("-l", "--language",  
            help="Language code of main language used in HTML documentation", required=True)
        parser.add_argument("-i", "--input_path",  
            help="Input path for rdf file", required=True)
        parser.add_argument("-o", "--output_path",  
            help="Output path for html documentation file", required=True)
        parser.add_argument("-u", "--base_url",  
            help="Namespace of concepts in input file", required=True)
        args = parser.parse_args()
        self.language = args.language
        self.pref_label = args.pref_label
        self.input_path = args.input_path
        self.output_path = args.output_path
        self.base_url = args.base_url
        self.parse_graph()
        
    def get_pref_label(self, graph, subject):
        for probj in graph.predicate_objects(subject):
            prop = probj[0]
            obj = probj[1]
            prop_ns = prop.n3(graph.namespace_manager)
            language = None
            prop_name = prop_ns
            if prop_ns == self.pref_label:
                if Literal(probj[1]).language:
                    if self.language == Literal(probj[1]).language:
                        return(obj)
                else:    
                    return(obj)
    
    def sort_properties(self, graph, properties):
        unsorted_properties = {}
        for prop in properties:
            pref_label = self.get_pref_label(graph, prop)
            unsorted_properties[pref_label] = {prop: properties[prop]}
        sorted_labels = sorted(unsorted_properties.keys(), key=str.casefold)
        sorted_properties = {}
        for pref_label in sorted_labels:
            sorted_properties.update(unsorted_properties[pref_label])
        return sorted_properties
    
    def create_contents(self, html_doc, graph, header, properties):
        header_element = add_sublement(html_doc, 'h2', text=header)
        paragraph = add_sublement(html_doc, 'p')
        for idx, subject in enumerate(properties):
            text = self.get_pref_label(graph, subject)
            result = urldefrag(subject)
            if result:
                tag = result[1]
                if idx < len(properties) - 1:
                    text = text + ", "
                anchor = add_sublement(paragraph, 'a', text) 
                anchor.set('href' , "#" + tag)
        
    def create_properties(self, html_doc, graph, header, properties):
        header_element = add_sublement(html_doc, 'h2', text=header)
        paragraph = add_sublement(html_doc, 'div')
        for subject in properties:
            result = urldefrag(subject)
            if result:
                pref_label = self.get_pref_label(graph, subject)
                div = add_sublement(paragraph, 'div')
                div.set('class', 'property')
                anchor = add_sublement(div, 'a', pref_label)
                anchor.set('id', result[1])
                table = add_sublement(paragraph, 'table')
                for prop in properties[subject]:
                    tablerow = add_sublement(table, 'tr')
                    td_key = add_sublement(tablerow, 'td', prop)
                    td_key.set('class', 'key')
                    td_value = add_sublement(tablerow, 'td')
                    td_value.set('class', 'value')
                    text = ""
                    for idx, value in enumerate(properties[subject][prop]):
                        if type(value) == URIRef:
                            root = etree.Element('a')
                            href_value = value
                            result = urldefrag(subject)
                            if result:
                                tag = result[0]
                                base_tag = urldefrag(self.base_url)[0]
                                if tag == base_tag and prop != 'URI':
                                    value_label = self.get_pref_label(graph, value)
                                    if value_label:
                                        value = value_label
                                        result = urldefrag(href_value)
                                        href_value = "#" + result[1]
                                else:
                                    root.set('target', '_blank')
                            else:
                                root.set('target', '_blank')
                            root.text = str(value)
                            root.set('href', str(href_value))
                            if idx < len(properties[subject][prop]) - 1:
                                root.tail = ", "
                            td_value.append(root)
                        else:                    
                            text += str(value)
                            if idx < len(properties[subject][prop]) - 1:
                                text += ", "        
                    try:
                        text = etree.fromstring(text)
                        td_value.append(text)
                    except etree.XMLSyntaxError:
                        try:
                            text = etree.fromstring(text)
                            td_value.append(text)
                        except etree.XMLSyntaxError:
                            td_value.text = text
            
    def parse_graph(self):
        g = Graph()
        g.parse(self.input_path, format="ttl")
        class_properties = set()         
        data_model = {}

        for t in TYPES:
            data_model[t] = {}
            for subject in g.subjects(RDF.type, t):
                result = urldefrag(subject)
                pref_label = self.get_pref_label(g, subject)
                if pref_label and result:
                    tag = result[1]
                    sorted_properties  = {}
                    subject_properties = {}
                    sorted_properties['URI'] = [subject]
                    result = urldefrag(subject)
                    pref_labels = []
                    other_properties = []
                    for probj in g.predicate_objects(subject):
                        prop = probj[0]
                        obj = probj[1]
                        prop_ns = prop.n3(g.namespace_manager)
                        language = None
                        prop_name = prop_ns
                        if Literal(probj[1]).language:
                            language = Literal(probj[1]).language
                            prop_name += " (" + Literal(probj[1]).language + ")"
                        if prop_ns == self.pref_label:
                            pref_labels.append({'language': language, 'prop': prop_name, 'obj': obj})
                        else:
                            other_properties.append({'language': language, 'prop': prop_name, 'obj': obj})
                            
                    sorted_languages = sorted(pref_labels, key=lambda k: (  
                        k['language'] != self.language,
                        k['language']
                    ))
                    
                    for sl in sorted_languages:
                        if sl['prop'] in sorted_properties:
                            sorted_properties[sl['prop']].append(sl['obj'])
                        else:
                            sorted_properties[sl['prop']] = [sl['obj']]
                    other_properties = sorted(other_properties, key=lambda k: (  
                        k['prop']
                    ))
                    for sl in other_properties:
                        if sl['prop'] in sorted_properties:
                            sorted_properties[sl['prop']].append(sl['obj'])
                        else:
                            sorted_properties[sl['prop']] = [sl['obj']]
                    data_model[t][subject] = sorted_properties

                else:
                    logging.warning("PrefLabel or URI fragment missing from %s"%subject)
        html_doc = etree.Element("html")
        head = etree.SubElement(html_doc, "head")
        link = add_sublement(head, "link", text=None)
        link.set('rel', 'stylesheet')
        link.set('href', 'stylesheet.css')
        link.tail = None
        body = etree.SubElement(html_doc, "body")
        for t in data_model:
            data_model[t] = self.sort_properties(g, data_model[t])
        for t in data_model:
            if data_model[t]:
                self.create_contents(html_doc, g, HEADERS[t], data_model[t])

        for t in data_model:
            if data_model[t]:
                self.create_properties(html_doc, g, HEADERS[t], data_model[t])

        with open(self.output_path, 'wb') as output:
            output.write(etree.tostring(html_doc, encoding='utf-8', pretty_print=True))
  
if __name__ == '__main__':
    RDFtoHTML()
    
