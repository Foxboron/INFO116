
from owllib.ontology import Ontology
from rdflib import URIRef

import re


#TODO: convert to actual tests

ont = Ontology()
ont.load(source="./Wittg2.owl")



test_text = """

Noe annet svada

Similies

Wittgenstein


"""

test_text_result = """

Noe annet svada

Similies

Wittgenstein


"""

words = {""}



def get_name(url):
  return url.split("#")[-1]



def annotate_text(string):
  return


def create_namespace():
  l = {}
  f = open("./Wittg2.owl").read()

  n = re.findall("<[^/\!\?].* ", f)

  for i in n:
    s = i[1:].strip()

    namespace, property = s.split(":")
    l[property] = namespace


  return l



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
  for cls in ont.classes:
      if cls.is_named():
          print()
          # print("Word:", get_name(cls.uri))
          # print("Property:",get_name(list(cls.triples)[0][1]))

          for s, p, o in cls.triples:
              print(get_name(s), get_name(p), get_name(o))
          print("----")

          # if cls.children:
          #   print("- Parents")
          #   for parent in cls.children:
          #       print("\t"+get_name(parent.uri))

# print_stuff()
print("----")
print(get_ontology())



