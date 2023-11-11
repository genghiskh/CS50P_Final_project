from project import interaction_check
from project import get_rxcui
from project import combined_dict

drug_list = {"a": "207106","b": "152923","c": "656659"}

def test_interaction_check():

    assert len(interaction_check(drug_list, "onchigh")) > 0
    assert len(interaction_check(drug_list, "drugbank")) > 0


def test_get_rxcui():

    assert get_rxcui('simvastatin') == ['simvastatin',"36567"]
    assert get_rxcui('fluconazole') == ["fluconazole","4450"]


def test_combined_list():


    assert combined_dict({"a":1},{"b":2}) == {"a":1, "b":2}
    assert combined_dict({"a":1},{"b":0, "c":2}) == {"a":1, "b":0 , "c":2}







