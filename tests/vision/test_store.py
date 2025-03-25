import sys, pathlib
sys.path.append("packages/vision/store")
import bucket, vision
import base64

def test_store():
    buc = bucket.Bucket({})
    assert len(buc.find("cat")) == 0
    body = pathlib.Path("tests/vision/cat.jpg").read_bytes()
    print(f"body {body}")
    buc.write("cat.jpg", body)
    ls = buc.find("cat")
    assert len(ls) == 1
    sz =  buc.size(ls[0])
    assert sz > 0
    b64 = buc.read(ls[0])
    assert len(b64) >= sz
    vis = vision.Vision({})
    res = vis.decode(base64.b64encode(b64).decode("utf-8"))
    assert res.find("cat") != -1
    n = buc.remove(ls[0])
    assert n == 1
    assert len(buc.find("cat")) == 0
