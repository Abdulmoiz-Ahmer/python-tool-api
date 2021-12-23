import json
import urllib.request
from typing import List, Dict, Set
import requests

def read_text_file(file_name):
    f = open(file_name, 'r', encoding='Latin1')
    file_text = f.readlines()
    return file_text

def get_list_ofcoll_link(collec_name):
    list1 = read_text_file("coll_link_solanart.txt")
    ret_coll = "not_found"
    for x in list1:
        coll_name = x.split('~:')[0]
        link_name = x.split('~:')[1].replace('\n', '')
        # print(coll_name, link_name)
        if collec_name == coll_name:
            ret_coll =  link_name
            break

    if not ret_coll == "not_found":
        return ret_coll
    else:
        return collec_name

def getSetIdSolanart(collection: str) -> Dict:
    print("Start Solanart")
    SetIdSol = dict()
    # collection = collection.lower()
    # url = "https://jmccmlyu33.medianetwork.cloud/nft_for_sale?collection=" + collection
    collection = get_list_ofcoll_link(collection)
    url = "https://qzlsklfacc.medianetwork.cloud/nft_for_sale?collection=" + collection
    # url = url.replace(" ", "").replace("&", "and").replace("2D Soldiers", "solarmy2d").replace("3D Soldiers", "solarmy3d").lower()
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
    URL = "https://us-central1-digitaleyes-prod.cloudfunctions.net//offers-retriever"
    PARAMS = {'collection':collection}
    # url = 'https://us-central1-digitaleyes-prod.cloudfunctions.net//offers-retriever?collection=' + collection
    # print('Platform-31 ', url)
    try:
        try:
        #     offer_dict = json.loads(urllib.request.urlopen(url).read())
        # except:
        #     try:
            offer_dict = requests.get(url = URL, params = PARAMS)
            offer_dict = offer_dict.json()
            # print('43', offer_dict)
        except Exception as e:
            offer_dict = ""
            print("Call 37", e)
        for elem in offer_dict["offers"]:
            setId[elem["metadata"]["name"]] = elem
        return setId
    except:
        # return_statement = "No Collection named"+ collection + "in SolanaArt"
        return "Collection not found"
