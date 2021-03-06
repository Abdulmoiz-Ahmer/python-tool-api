from flask import Flask, jsonify, request, Response, make_response
import urllib.request
import json
import time
from typing import List, Dict, Set
from enum import Enum
import flask
from flask_cors import cross_origin
import callPlatform as api_calls
import requests

DIGITAL_CONSTANT = 1000000000

app = Flask(__name__)
@cross_origin()

def notification(location=None):
    return "notification"

# collekce se jmenuji trochu jinak na solanart a digitaleyes
# prvni hodnota je solanart, druha digitaleyes
class Collection(Enum):
    solbears = ["solbears", "SolBear"]
    Thugbirdz = [None, "Thugbirdz"]
    boldBadgers = ["boldbadgers", None]
    solarians = [None, "Solarians"]


def print_solanart(nft):
    return ("New :" + str(nft["price"]) +
          " with attributes:" + nft["attributes"])

def print_digital(nft, value=None):
    return("New: " + str(nft["price"]/DIGITAL_CONSTANT) +
          "attributes filtering for : " + str(value))

users = [{'id': 0, 'name': 'Server'}]
collections = ['123', 'afsgnaof', '16468']
@app.route('/api/collections')
def get_collections():
    response_col = flask.jsonify({'Coll': collections})
    try:
        response_col.headers.add('Access-Control-Allow-Origin', '*')
    except Exception as e:
        print("172", e)
    return response_col

@app.route('/api/collections/<string:coll_inp>', methods=['GET'])
def getCollections(coll_inp: str) -> Dict:
    collDict = dict()
    list_coll_name = requests.get('https://cryptobros-76836-default-rtdb.firebaseio.com/Collections/'+coll_inp+'.json')

    # ret_list = []
    collDict['collections'] = []
    for x in list_coll_name.json():
        # print(list_coll_name.json()[x].keys())
        collDict['collections'].append(list_coll_name.json()[x]["name"])
    
    response = flask.jsonify({'response': collDict})
    try:
        response.headers.add('Access-Control-Allow-Origin', '*')
    except Exception as e:
        print("172", e)
    return response


@app.route('/api/solanart/attributes/<string:att_inp>', methods=['GET'])
def getSolanartAttributes(att_inp: str) -> Dict:
    attDict = dict()
    # url = "https://jmccmlyu33.medianetwork.cloud/nft_for_sale?collection=" + collection
    url = "https://qzlsklfacc.medianetwork.cloud/nft_for_sale?collection=" + att_inp
    url = url.replace(" ", "").replace("&", "and").replace("2D Soldiers", "solarmy2d").replace("3D Soldiers", "solarmy3d").lower()
    try:
        for elem in json.loads(urllib.request.urlopen(url).read()):
            try:
                # print('\n', elem.get("attributes"), '\n')
                current_attributes = elem.get("attributes")
                # if counter == 0 :
                #     for att in current_attributes.split(','):
                #         print(att)
                #     counter+= 1
                for att in current_attributes.split(','):
                    att_key = att.split(':')[0]
                    att_val = att.split(':')[1]
                    if not att_key in attDict.keys():
                        attDict[att_key] = [att_val]
                    else:
                        if not att_val in attDict[att_key]:
                            attDict[att_key].append(att_val)
                        else:
                            pass
                        # print(att)
            except:
                print("92", "except")
                current_attributes = ""
            # attDict[elem.get("name")] = current_attributes
    except:
        attDict["response"] = "NULL"
        pass
    # print(attDict)
    response = flask.jsonify({'Attribute': attDict})
    # print("170", response)
    try:
        response.headers.add('Access-Control-Allow-Origin', '*')
    except Exception as e:
        print("172", e)
    return response
    # return "attDict"

@app.route('/api/digitaleye/attributes/<string:att_inp>', methods=['GET'])
def getDigitalEyeAttributes(att_inp: str) -> Dict:
    DigEyeatt = dict()
    print("99", att_inp)
    att_inp = att_inp.replace(" ", "%20")
    url = "https://us-central1-digitaleyes-prod.cloudfunctions.net/offers-retriever?collection=" + att_inp
    # url = url.replace(" ", "").replace("&", "and").replace("2D Soldiers", "solarmy2d").replace("3D Soldiers", "solarmy3d").lower()
    try:
        offer_dict = json.loads(urllib.request.urlopen(url).read())
        for elem in offer_dict["offers"]:
            try:
                # print('\n', elem.get("attributes"), '\n')
                current_attributes = elem["metadata"]["attributes"]
                # if counter == 0 :
                #     for att in current_attributes.split(','):
                #         print(att)
                #     counter+= 1
                for att in current_attributes:
                    att_key = att["trait_type"]
                    att_val = att["value"]
                    if not att_key in DigEyeatt.keys():
                        DigEyeatt[att_key] = [att_val]
                    else:
                        if not att_val in DigEyeatt[att_key]:
                            DigEyeatt[att_key].append(att_val)
                        else:
                            pass
                        # print(att)
            except Exception as e:
                print("117", "except", e)
                current_attributes = ""
            # DigEyeatt[elem.get("name")] = current_attributes
    except:
        DigEyeatt["response"] = "NULL"
        pass
    # print(DigEyeatt)
    response = flask.jsonify({'Attribute DigitalEye': DigEyeatt})
    # print("170", response)
    try:
        response.headers.add('Access-Control-Allow-Origin', '*')
    except Exception as e:
        print("172", e)
    return response
    # return "DigEyeatt"

@app.route('/api/nft/magiceden/<string:coll_inp>/<float:price_inp>', methods=['GET'])
@app.route('/api/nft/magiceden/<string:coll_inp>/<int:price_inp>', methods=['GET'])
@app.route('/api/nft/magiceden/<string:coll_inp>/<string:att_inp>/<float:price_inp>', methods=['GET'])
@app.route('/api/nft/magiceden/<string:coll_inp>/<string:att_inp>/<int:price_inp>', methods=['GET'])
def get_response_mgcedn(coll_inp, price_inp, att_inp='attribute')-> Dict:
    ret_dic_nft = dict()

    price = price_inp

    filter_attribute = True

    if att_inp == "attribute":
        filter_attribute = False

    att_value = att_inp
    try:
        second_mgcedn = api_calls.getSetIdMagicEden(coll_inp)
        print('143 ME')
        if second_mgcedn == "Collection not found" or len(second_mgcedn) == 0:
            pass
        else:
            print('147 ME')
            ret_dic_nft["resp_MagicEden"] = []

            for elem in second_mgcedn:
                try:
                    nft: Dict = second_mgcedn.get(elem)
                except:
                    nft: Dict = second_mgcedn['elem']
                
                # print('154 ME')

                if nft.get("price") < price:
                    # print('157 ME')
                    # nft.get("title")
                    if filter_attribute:
                        list_att_val = att_value.split(',')
                        all_attr = nft.get("attributes")
                        list_att_str = []
                        for att_ind in all_attr:
                            # print(att_ind)
                            # print(att_ind.get("trait_type"))
                            list_att_str.append(att_ind.get("trait_type").lower()+": "+att_ind.get("value").lower())
                        # print(list_att_str)
                        all_att_ok = True
                        for att_val_i in list_att_val:
                            if att_val_i.lower() in list_att_str:
                                # print('212 ---------------------')
                                # ret_dic_nft["resp_Solanart"] = notification()
                                # ret_dic_nft["resp_Solanart"].append(nft.get("name") + " -- https://solanart.io/search/?token=" +nft.get("token_add"))
                                pass
                            else:
                                all_att_ok = False
                                break
                                # ret_dic_nft["resp_Solanart"].append("Attribute does not fit")
                                pass
                        if all_att_ok:
                            ret_dic_nft["resp_MagicEden"].append(nft.get("title") + " -- https://www.magiceden.io/item-details/" +nft.get("mintAddress"))
                        else:
                            pass
                    else:
                        ret_dic_nft["resp_MagicEden"].append(nft.get("title") + " -- https://www.magiceden.io/item-details/" +nft.get("mintAddress"))
                    # ret_dic_nft["resp_MagicEden"].append(nft.get("title"))
                    # print('159 ME')
                    pass
                else:
                    pass
            pass
    except Exception as e:
        print('Exception Mgcedn', e)

    response = flask.jsonify({'NFT': ret_dic_nft})
    print("163", response)
    try:
        response.headers.add('Access-Control-Allow-Origin', '*')
    except Exception as e:
        print("167", e)
    return response


    response = flask.jsonify({'NFT': ret_dic_nft})
    print("163", response)
    try:
        response.headers.add('Access-Control-Allow-Origin', '*')
    except Exception as e:
        print("167", e)
    return response

    

@app.route('/api/nft/<string:coll_inp>/<float:price_inp>', methods=['GET'])
@app.route('/api/nft/<string:coll_inp>/<int:price_inp>', methods=['GET'])
@app.route('/api/nft/<string:coll_inp>/<string:att_inp>/<float:price_inp>', methods=['GET'])
@app.route('/api/nft/<string:coll_inp>/<string:att_inp>/<int:price_inp>', methods=['GET'])
def get_response(coll_inp, price_inp, att_inp='attribute')-> Dict:
    ret_dic_nft = dict()

    # price = 14
    price = price_inp

    # SOLANART FILTERING
    # set to True to check if att_value is in attributes of the nft
    filter_solanart = True

    if att_inp == "attribute":
        filter_solanart = False

    # value of the attribute
    # att_value = "Zombie"
    att_value = att_inp

    trait_type = "Title"
    value = "Monitor"
    
    collection = [coll_inp, coll_inp]

    check_solanaArt = True
    check_DigitalEye = True

    if collection[0] is not None:
        print("\n\n\nstarted parsing solanart")
        try:
            # first_solanart = getSetIdSolanart(collection[0])
            first_solanart = "fds"
            if first_solanart == "Collection not found":
                check_solanaArt = False
        except:
            print("91", "Error on initial check")

    print("parsed initial")

    notify = False

    msg = "new data parsed for " + \
        str(collection[0]) + \
        " for maximum : " + str(price)
    if filter_solanart:
        msg = msg + " filtering for :" + att_value + " on solanart"
    if trait_type is not None:
        msg = msg + " filtering for " + value + " on digieyes"
    ret_dic_nft["msg"] = msg

    ret_dic_nft["resp_Solanart"] = []
    if collection[0] is not None and check_solanaArt:
        print("183", "Into collection[0]")
        try:
            # second_solanart = getSetIdSolanart(collection[0])
            second_solanart = api_calls.getSetIdSolanart(collection[0])
            # second_solanart = second
            print("169 -------------------")
            # print(second_solanart)
            # try:
            #     diff_solanart = second_solanart.keys() - first_solanart.keys()
            # except Exception as e:
            #     print("173 :", e)
            print("171 ===============")
            if len(second_solanart) == 0:
            # if len(diff_solanart) == 0:
                print("Solanart: No new key")
                # ret_dic_nft["resp_Solanart"].append("No new key")
            else:
                print("173, fgnafln")
                for elem in second_solanart:
                    try:
                        nft: Dict = second_solanart.get(elem)
                    except:
                        nft: Dict = second_solanart['elem']
                    # print('206 ///////////////////')
                    if nft.get("price") < price:
                        res_URL ="https://qzlsklfacc.medianetwork.cloud/nft_for_sale?collection=" + collection[0]
                        if filter_solanart:
                            list_att_val = att_value.split(',')
                            all_att_ok = True
                            list_all_att = nft.get("attributes").lower()
                            for att_val_i in list_att_val:
                                if att_val_i.lower() in list_all_att:
                                    # print('212 ---------------------')
                                    # ret_dic_nft["resp_Solanart"] = notification()
                                    # ret_dic_nft["resp_Solanart"].append(nft.get("name") + " -- https://solanart.io/search/?token=" +nft.get("token_add"))
                                    pass
                                else:
                                    all_att_ok = False
                                    break
                                    # ret_dic_nft["resp_Solanart"].append("Attribute does not fit")
                                    pass
                            if all_att_ok:
                                ret_dic_nft["resp_Solanart"].append(nft.get("name") + " -- https://solanart.io/search/?token=" +nft.get("token_add"))
                            else:
                                pass
                        else:
                            # ret_dic_nft["resp_Solanart"] = notification()
                            ret_dic_nft["resp_Solanart"].append(nft.get("name") + " -- https://solanart.io/search/?token=" +nft.get("token_add"))
                    else:
                        # ret_dic_nft["resp_Solanart"].append("Price does not fit")
                        pass
        except Exception as e:
            print("196", e)
            # ret_dic_nft["resp_Solanart"].append("ERROR: data source unavailable")
    else:
        return_statement = "No Collection named '"+ collection[0] + "' in SolanaArt"
        print("Solanart:",return_statement)
        # ret_dic_nft["resp_Solanart"].append(return_statement)

    if collection[1] is not None:
        print("\n\n\nstarted parsing digitalEyes")
        # first_digeye = api_calls.getSetIdDigitalEyes(collection[1])
        first_digeye = 'bkh'
        if first_digeye == "Collection not found":
            check_DigitalEye = False

    ret_dic_nft["resp_DigitalEye"] = []
    if collection[1] is not None and check_DigitalEye:
        print("210", "Into collection[1]")
        try:
            second_digeye = api_calls.getSetIdDigitalEyes(collection[1])
            print("242 -------------------")
            # print("127", second_digeye.keys())
            # diff_digieye = second_digeye.keys() - first_digeye.keys()
            print("245 ===============")
            if len(second_digeye) == 0:
            # if len(second_digeye) == 0:
                print("DigitalEye: No new Key")
                # ret_dic_nft["resp_DigitalEye"].append("No new key")
            else:
                for elem in second_digeye:
                    try:
                        nft: Dict = second_digeye.get(elem)
                    except:
                        nft: Dict = second_digeye['elem']                    
                    # print('256 ///////////////////')
                    # print("167", nft["price"]/DIGITAL_CONSTANT)
                    if nft["price"] < price * DIGITAL_CONSTANT:
                        ret_dic_nft["resp_DigitalEye"].append(nft["metadata"]["name"] + " -- https://digitaleyes.market/item/" + coll_inp + "/" + nft["mint"] + "?pk=" + nft["pk"])

                        
                        # print('259 ..........................')
                        # print("169", nft["price"]/DIGITAL_CONSTANT)
                        # if trait_type is not None:
                        #     # print('262 ,,,,,,,,,,,,,,,,,,,,,,,', nft["metadata"]["attributes"])
                        #     for att in nft["metadata"]:
                        #         # try:
                        #         #     print('264 ..............', att)
                        #         # except:
                        #         #     print('267 ..............', nft.get("attributes"))
                        #         for att_val in nft["metadata"]["attributes"]:
                        #             print(att_val['value'])
                        #         if nft["metadata"]["attributes"]["trait_type"] == trait_type and nft["metadata"]["attributes"]["value"] == value:
                        #             # print('266 ,,,,,,,')
                        #             # ret_dic_nft["resp_DigitalEye"].append(res_URl)
                        #             ret_dic_nft["resp_DigitalEye"].append(att["name"] + " -- " + att["image"])
                        #         else:
                        #             pass
                        #             # ret_dic_nft["resp_DigitalEye"].append("Trait or attribute does not match")
                        # else:
                        #     # ret_dic_nft["resp_DigitalEye"].append(res_URl)
                        #     ret_dic_nft["resp_DigitalEye"].append(nft["metadata"]["name"] + " -- " + nft["metadata"]["image"])
                    else:
                        pass
                        # ret_dic_nft["resp_DigitalEye"].append("Price does not fit")
        except Exception as e:
            print("279", e)
            # ret_dic_nft["resp_DigitalEye"].append("ERROR: data source unavailable")
    else:
        return_statement = "No Collection named '"+ collection[0] + "' in DigitalEye"
        print("DigitalEye:",return_statement)
        # ret_dic_nft["resp_DigitalEye"].append(return_statement)

    response = flask.jsonify({'NFT': ret_dic_nft})
    print("287", response)
    try:
        response.headers.add('Access-Control-Allow-Origin', '*')
    except Exception as e:
        print("292", e)
    return response

@app.route('/api/check/<string:coll>')
def check_api(coll)-> Dict:
    ret_dic = dict()
    ret_dic["abs"] = coll
    ret_dic["csv"] = "checking 2 is working fine"
    return ret_dic


if __name__ == '__main__':
    app.run(port=5050)
