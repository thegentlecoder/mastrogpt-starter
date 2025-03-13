import vdb
import urllib.request
from bs4 import BeautifulSoup
from bs4.element import Comment
import re
import nltk

USAGE = f"""Welcome to the Vector DB Loader.
Write text to insert in the DB.
Start with * to do a vector search in the DB.
Start with ! to remove text with a substring.
"""

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

def sentence_tokenize(text):
    tokens = text.split(".")
    return tokens

def tokenize(text):
    tokens = text.split()
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        if re.match(r'\d{1,2}[/-]\d{1,2}[/-]\d{4}', token):
            pass
        
        elif re.match(r"\w+'s", token):
            token = re.sub(r"(\w+)'s", r"\1 's", token)
        
        elif re.match(r"\w+'\w+", token):
            token = token.replace("'", "")
        
        elif re.match(r"\w+-\w+", token):
            pass
        
        elif re.match(r"\d+(,\d+)*", token):
            pass
        
        else:
            token = re.sub(r"([^\w\s]+)", r" \1 ", token)
        
        token = re.sub(r"(\w+)\.", r"\1", token)
        token = re.sub(r"(\w+),", r"\1", token)
        token = re.sub(r"U\.S\.A\.", r"U.S.A.", token)
        
        tokens[i] = token
        i += 1
    
    return tokens

def load(args):
  
  collection = args.get("COLLECTION", "default")
  out = f"{USAGE}Current colletion is {collection}"
  inp = str(args.get('input', ""))
  db = vdb.VectorDB(args)
  
  if inp.startswith("*"):
    if len(inp) == 1:
      out ="please specify a search string"
    else:
      res = db.vector_search(inp[1:])
      if len(res) > 0:
        out = f"Found:\n"
        for i in res:
          out += f"({i[0]:.2f}) {i[1]}\n"
      else:
        out = "Not found"
  elif inp.startswith("!"):
    count = db.remove_by_substring(inp[1:])
    out = f"Deleted {count} records."
  elif inp != '':
    if (inp.startswith("https://")):
      try:
        #inp = "https://openserverless.apache.org/"
        f = urllib.request.urlopen(inp)
        html = f.read()
        soup = BeautifulSoup(html)
        text = text_from_html(html)
        tokens = sentence_tokenize(text)
        out = "Inserted" 
        for token in tokens:
          res = db.insert(token)
          out += "\n" + " ".join([str(x) for x in res.get("ids", [])])
          #out += "\n" + token
      except:
        return {"output": "Failed to connect to or import text from the https source"}
    else:
      res = db.insert(inp)
      out = "Inserted " 
      out += " ".join([str(x) for x in res.get("ids", [])])

  return {"output": out}
  
