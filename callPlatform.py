import json
import urllib.request
from typing import List, Dict, Set

def getSetIdSolanart(collection: str) -> Dict:
    print("Start Solanart")
    SetIdSol = dict()
    # url = "https://jmccmlyu33.medianetwork.cloud/nft_for_sale?collection=" + collection
    url = "https://qzlsklfacc.medianetwork.cloud/nft_for_sale?collection=" + collection
    try:
        counter= 0
        for elem in json.loads(urllib.request.urlopen(url).read()):
            if counter == 0:
                # print(elem["id"])
                # print(elem)
                counter = 1
            # SetIdSol[elem.get("id")] = elem
            SetIdSol[elem["id"]] = elem
        # print(SetIdSol)
        # return make_response(jsonify({"status": "ok", "data": SetIdSol}), 201)
        return SetIdSol
    except:
        # return_statement = "No Collection named"+ collection + "in SolanaArt"
        return "Collection not found"

def getSetIdDigitalEyes(collection: str) -> Dict:
    print("DigitalEye")
    setId = dict()
    url = "https://us-central1-digitaleyes-prod.cloudfunctions.net/offers-retriever?collection=" + collection
    try:
        offer_dict = json.loads(urllib.request.urlopen(url).read())
        for elem in offer_dict["offers"]:
            setId[elem["metadata"]["name"]] = elem
        return setId
    except:
        # return_statement = "No Collection named"+ collection + "in SolanaArt"
        return "Collection not found"
