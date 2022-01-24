import json
import urllib.request
from typing import List, Dict, Set
import requests

headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0",
        "Accept": "gzip, deflate, br,text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1"}

def read_text_file(file_name):
    f = open(file_name, 'r', encoding='Latin1')
    file_text = f.readlines()
    return file_text

def get_list_ofcoll_link(Collenction, collec_name):

    list_coll_name = requests.get('https://cryptobros-76836-default-rtdb.firebaseio.com/Collections/'+Collenction+'.json')
    ret_coll = "not_found"
    for x in list_coll_name.json():
        coll_name = list_coll_name.json()[x]["name"]
        link_name = list_coll_name.json()[x]["link"]
        # print(coll_name, link_name)
        if collec_name == coll_name:
            ret_coll =  link_name
            break

    if not ret_coll == "not_found":
        # print('34')
        return ret_coll
    else:
        # print('37')
        return collec_name
    
def getSetIdMagicEden(collection: str) -> Dict:
    print("Start Magic Eden")
    SetIdMgc = dict()
    collection = get_list_ofcoll_link("Magiceden",collection)
    url_test = "https://api-mainnet.magiceden.io/rpc/getListedNFTsByQuery?q={%22$match%22:{%22collectionSymbol%22:%22"+collection+"%22},%22$sort%22:{%22createdAt%22:-1},%22$skip%22:0,%22$limit%22:20}"
    r = requests.get(url_test,
                        headers=headers,
                        stream = True)
    # return r.content
    
    # print(url_test)
    try:
        # count = 1
        for elem in json.loads(r.content)["results"]:
            # print(count)
            SetIdMgc[elem["id"]] = elem
            # count += 1
        return SetIdMgc
    except:
        return "Collection not found"


def getSetIdSolanart(collection: str) -> Dict:
    print("Start Solanart")
    SetIdSol = dict()
    # collection = collection.lower()
    # url = "https://jmccmlyu33.medianetwork.cloud/nft_for_sale?collection=" + collection
    collection = get_list_ofcoll_link("Solanart",collection)
    # url = "https://qzlsklfacc.medianetwork.cloud/nft_for_sale?collection=" + collection
    url_test = "https://qzlsklfacc.medianetwork.cloud/get_nft?collection="+collection+"&page=0&limit=100&order=&fits=any&trait=&search=&min=0&max=0&listed=true&ownedby=&attrib_count="
    total_pages = json.loads(urllib.request.urlopen(url_test).read())["pagination"]["maxPages"]
    print('pagination', total_pages)
    # url = url.replace(" ", "").replace("&", "and").replace("2D Soldiers", "solarmy2d").replace("3D Soldiers", "solarmy3d").lower()
    try:
        for x in range(total_pages):
            for elem in json.loads(urllib.request.urlopen(url_test).read())["items"]:
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
