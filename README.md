# ntp-model
Nimitietopalvelun tietomalli  - toimijakuvailut

KAM-kuvailuryhmässä vuosina 2015-2019 laaditun Nimitietopalvelun tietomallin versio 2.0 RDF-muodossa. 
Projekti ja tietomallin kuvaus https://www.kiwi.fi/pages/viewpage.action?pageId=85464271 

Luokat ja ominaisuudet perustuvat ensisijaisesti RDA registryn vastaaviin. 
Tarvittessa käytetty muita malleja, kuten GND ontologia https://d-nb.info/standards/elementset/gnd. 
Tomijoiden välisiin suhteisiin liittyvät ominasuudet on kuvattu Metatietosanastossa.

Mallin tämä versio on laadittu Kansalliskirjastossa vuonna 2020. 
Kehittämistä tehdään yhteistyössä KAM-kuvailuryhmän kanssa ja vahistetaan Toimijakuvailuverkostossa.

ntp Nimitietopalvelun elementtien ontologia (viimeisin versio)


# ntp-model element set
Class and Property Element set  for a Finnish Integrated Agent Name Metadata Service (Nimitietopalvelu, NTP)

Author: Jarmo Saarikko (National Library of Finland)

Contributors: Members of the KAM-kuvailuryhmä, staff mebers of the National Library of Finland.

Copyright: © the National Library of Finland, 2020-2021

License: This work is licensed under a Creative Commons - CC0 1.0 Universal License. This copyright applies to the documentation and the accompanying RDF specification. Regarding underlying technology, we use W3C's RDF technology, an open Web standard that can be freely used by anyone.

The original data model structure created in 2015 is based on the AHAA-model of the National Archive of Finland.
The properties are based on the RDA registry and are aligned with other ontologies, such as the Finnish "Metadata thesaurus" https://finto.fi/mts/en/ and the "GND Ontology" element set https://d-nb.info/standards/elementset/gnd.

# scripts
Scripts for converting data model to HTML and mapping data model property URIs to URNs are located in scripts directory of the project.

Usage example of converting data model to HTML: 
```
python rdf_to_html.py -pl="skos:prefLabel" -l="fi" -i="ntp" -o="ntp.html" -u="https://github.com/NatLibFi/ntp-model/tree/master/elementset/ntp#"
```

Usage example of mapping property URIs with URNs to XML file (to validate XML use parameter -v and XSD file from http://epc.ub.uu.se/schema/rs/3.0/rs-location-mapping-schema.xsd)
```
python html_urn_mapping.py -ns="URN:NBN:fi:schema:ntp:" -p="http://schema.finto.fi/ntp#" -i"ntp.ttl" -o="testi.xml"
```

Copyright: © the National Library of Finland, 2021

License: The software source code is licensed under a GNU, General Public License, Version 3.0.
