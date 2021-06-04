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

from urllib.parse import urldefrag
from lxml import etree

def add_sublement(element, tag, text=None):
    subelement = etree.SubElement(element, tag)
    if text:
        subelement.text = text
    return subelement    

def defrag_iri(iri):
    result = urldefrag(iri)
    if result:
        tag = result[0]
        fragment = result[1]
        if not fragment and ':' in iri:
            # defrag URNs
            idx = iri.rfind(":")
            tag = iri[:idx + 1]
            fragment = iri[idx + 1:]
    return (tag, fragment)