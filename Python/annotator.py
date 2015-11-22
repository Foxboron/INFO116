
from owllib.ontology import Ontology
from rdflib import URIRef

import re


#TODO: convert to actual tests

ont = Ontology()
ont.load(source="./Wittg2.owl")


test_text = """
Logic

Language


Absolute Judgement
"""

words = {""}



def get_name(url):
  return url.split("#")[-1]




def create_namespace():
  l = {}
  f = open("./Wittg2.owl").read()
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
          print()
          for i in cls.triples:
              l = get_types(i)
              if l:
                  value.append(l)
        dd[key]=value
    return dd

#<span property="addressRegion">PA</span>
def annotate_text(string, ont):
    s = "<span property=\"{0}\">{1}</span>"
    for k,v in ont.items():
        if string in v:
            print(s.format(k,string))

ont = get_ontology()



for i in test_text.split("\n"):
    for w in i.split():
        annotate_text(w, ont)



