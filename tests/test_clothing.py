from app.clothing import advice,comfort_score

def test_cold():
    assert comfort_score(-25,5,10,50) <= 5

def test_warm():
    a=advice(22,22,50,10,2,0,0)
    assert any("футбол" in x for x in a["clothes"])

def test_rain():
    a=advice(10,8,80,80,4,0,1)
    assert any("непромока" in x for x in a["shoes"])
    assert "зонт" in a["accessories"]

def test_snow():
    a=advice(-2,-5,80,70,5,2,0)
    assert any("утепл" in x for x in a["shoes"])

def test_sport():
    a=advice(8,6,60,10,2,0,0,"sport")
    assert any("спортив" in x for x in a["clothes"])
