import os, requests as req
import sys, pathlib, time
#sys.path.append("packages/vision/store")
import base64
import vision
import bucket

USAGE = """
Please upload a picture and I will tell you what I see, or
@<substring>      decode files starting with <substring>
?                 this message
"""
FORM = [
  {
    "label": "any pics?",
    "name": "pic",
    "required": "true",
    "type": "file"
  },
]

def form(args):
  res = {}
  out = USAGE
  inp = args.get("input", "")

  if type(inp) is dict and "form" in inp:
    img = inp.get("form", {}).get("pic", "")
    print(f"uploaded size {len(img)}")
    #print(f"img {img}")
    vis = vision.Vision(args)
    out = vis.decode(img)
    res['html'] = f'<img src="data:image/png;base64,{img}">'

    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename = "upload/image_" + timestr + ".jpg"
    out += "\n\n" + filename
    body = base64.b64decode(img)
    print(f"filename {filename}")
    print(f"body {body}")
    try:
      buc = bucket.Bucket(args)
      buc.write(filename, body)
    except Exception as err:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      out += f"\n\nUnexpected {err=}, {type(err)=}, {exc_type=}, {fname=}, {exc_tb.tb_lineno=}"
      
  res['form'] = FORM
  res['output'] = out
  return res
