import sys, pathlib
sys.path.append("packages/vision/store")
import bucket, vision

def test_store():
    buc = bucket.Bucket({})
    assert len(buc.find("cat")) == 0
    body = pathlib.Path("tests/vision/cat.jpg").read_bytes()
    buc.write("cat.jpg", body)
    ls = buc.find("cat")
    assert len(ls) == 1
    sz =  buc.size(ls[0])
    assert sz > 0
    b64 = buc.read_b64(ls[0])
    assert len(b64) >= sz
    vis = vision.Vision({})
    res = vis.decode(b64)
    assert res.find("cat") != -1
    n = buc.remove(ls[0])
    assert n == 1
    assert len(buc.find("cat")) == 0
