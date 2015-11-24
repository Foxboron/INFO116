
from owllib.ontology import Ontology
from rdflib import URIRef

import re


#TODO: convert to actual tests

ont = Ontology()
ont.load(source="../final.rdf")


mentions = {}
global mentions

def get_name(url):
  return url.split("#")[-1]


def create_namespace():
  l = {}
  f = open("../final.rdf").read()
  n = re.findall("<[^/\!\?].* ", f)
  for i in n:
    s = i[1:].strip()
    namespace, property = s.split(":")
    l[property] = namespace
  return l


def get_types(triple):
    if get_name(triple[1]) == "type" and get_name(triple[2]) != "Class":
        return get_name(triple[0])



def print_stuff():
  for cls in ont.classes:
      if cls.is_named():
          print()
          print("Word:", get_name(cls.uri))
          for s, p, o in cls.triples:
              print(get_name(s), get_name(p), get_name(o))

          if cls.children:
            print("- Parents")
            for parent in cls.children:
                print("\t"+get_name(parent.uri))

def get_ontology():
    dd = {}
    for cls in ont.classes:
        value=[]
        key = get_name(cls.uri)
        if cls.is_named():# and get_name(cls.uri) == "Author":
          for i in cls.triples:
              l = get_types(i)
              if l:
                  value.append(l)
        dd[key]=value
    return dd

#<span property="addressRegion">PA</span>



def format_string(*string):
    string = [i for i in string if i]
    word = " ".join(string)
    string = [i.strip("\"\'`\(\)") for i in string if i]
    check = string[0].capitalize()+"_"+"_".join(string[1:]).lower()
    return word,check


def annotate_text(string, ont, check=None):
    s = "<span property=\"{0}\">{1}</span>"
    for k,v in ont.items():
        if check:
            if check in v:
                return s.format(k,string)
        if string in v:
            return s.format(k,string)

ont = get_ontology()


def process_text(text, name=None):
    ready_text = [i.split(" ") for i in text.split("\n")]

    global mentions
    mentions[name] = []

    for n,i in enumerate(ready_text):
        print(i)
        for nn,w in enumerate(i):
            word = None
            if w:
                # Check forward and backwards
                if nn+1 <= len(i)-1 and nn-1 >= 0:
                    w, w_check = format_string(ready_text[n][nn-1],ready_text[n][nn], ready_text[n][nn+1])
                    word = annotate_text(w,ont,check=w_check)
                    if word:
                        ready_text[n][nn-1] = None
                        ready_text[n][nn+1] = None
                        ready_text[n][nn] = word
                        mentions[name].append(w_check)

                # Checked forwards
                if nn+1 <= len(i)-1 and not word:
                    w, w_check = format_string(ready_text[n][nn], ready_text[n][nn+1])
                    word = annotate_text(w,ont,check=w_check)
                    if word:
                        ready_text[n][nn+1] = None
                        ready_text[n][nn] = word
                        mentions[name].append(w_check)

                # Check only single word
                if not word:
                    if ready_text[n][nn]:
                        w = ready_text[n][nn]
                        w_check = ready_text[n][nn].strip(".,\'\`\(\)\"").capitalize()
                        word = annotate_text(w,ont, check=w_check)
                        if word:
                            ready_text[n][nn] = word
                            mentions[name].append(w_check)
    return "\n".join(" ".join([ii for ii in i if ii]) for i in ready_text)

def main():
    import os
    s = list(os.walk("source"))
    dir = s[0][0]
    files = s[0][2]
    for i in files:
        f = open("{0}/{1}".format(dir, i)).read()
        r = process_text(f, name=i)
        f = open("done/{0}".format(i), "w")
        f.write("<span vocab=\"http://example.org/index.rdf\" typeof=\"Source\">")
        f.write(r)
        f.write("</span>")
        f.close()

main()

{
    "@context": {
        "uib": "http://example.org/index.rdf#",
        "owl": "http://www.w3.org/2002/07/owl#"
    },
    "@type": [
        "http://www.w3.org/2002/07/owl#NamedIndividual",
        "uib:Source"
    ],
    "wit:hasAuthor": {
    "@id": ""
    },
    "wit:Secondary": {
    "@id": ""
    },
    "wit:mentions": [
    {
    }
]
}

def format_owl(string,name):
    m = {"deirdre.html": ("Smith_text", "Secondary"),
         "formosa.html": ("Formosa_text", "Secondary"),
         "wittgenstein.html": ("Wittgenstein_text", "Primary"),
         "janyne.html": ("Sattler_text", "Secondary")}
    s = """
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/something/ontologies/2015/10/untitled-ontology-9#{0}">
        <rdf:type rdf:resource="http://www.semanticweb.org/something/ontologies/2015/10/untitled-ontology-9#{1}"/>
        <mentions rdf:resource="http://www.semanticweb.org/something/ontologies/2015/10/untitled-ontology-9#{2}"/>
    </owl:NamedIndividual>
    """
    return s.format(m[name][0], m[name][1], string)


def format_json_ld(string,name):
    return "{\"@id\": \"wit:\""+string+"\"},\n"




with open("additions", "w") as f:
    for k,v in mentions.items():
        for i in v:
            f.write(format_owl(i,k))


with open("json_ld", "w") as f:
    for k,v in mentions.items():
        f.write("\n\n"+k+"\n")
        for i in set(v):
            f.write(format_json_ld(i,k))



