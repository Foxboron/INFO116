
from owllib.ontology import Ontology
from rdflib import URIRef

import re


#TODO: convert to actual tests

ont = Ontology()
ont.load(source="./Wittg2.owl")




test_text = """

Logic

value Value
Value value

Language

Right or wrong

Absolute Judgement

Judgement


Judgement Bullshit
Bullshit Judgement


value
Value
value Value

Value value
"""

words = {""}
print(test_text)
print()
ready_text = [i.split(" ") for i in test_text.split("\n")]
print(ready_text)

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
    check = string[0].capitalize()+"_"+"_".join(string[1:]).lower()
    return word,check


def annotate_text(string, ont, check=None):
    print(string)
    s = "<span property=\"{0}\">{1}</span>"
    for k,v in ont.items():
        if check:
            if check in v:
                return s.format(k,string)
        if string in v:
            return s.format(k,string)

ont = get_ontology()


for n,i in enumerate(ready_text):
    for nn,w in enumerate(i):
        word = None

        # Check forward and backwards
        if nn+1 <= len(i)-1 and nn-1 >= 0:
            w, w_check = format_string(ready_text[n][nn-1],ready_text[n][nn], ready_text[n][nn+1])
            word = annotate_text(w,ont,check=w_check)
            if word:
                ready_text[n][nn-1] = None
                ready_text[n][nn+1] = None
                ready_text[n][nn] = word

        # Checked forwards
        if nn+1 <= len(i)-1 and not word:
            w, w_check = format_string(ready_text[n][nn], ready_text[n][nn+1])
            word = annotate_text(w,ont,check=w_check)
            if word:
                ready_text[n][nn+1] = None
                ready_text[n][nn] = word

        # Check only single word
        if not word:
            if ready_text[n][nn]:
                w = ready_text[n][nn]
                w_check = ready_text[n][nn].capitalize()
                word = annotate_text(w,ont, check=w_check)
                if word:
                    ready_text[n][nn] = word


print(ready_text)
print()
print("\n".join(" ".join([ii for ii in i if ii]) for i in ready_text))


