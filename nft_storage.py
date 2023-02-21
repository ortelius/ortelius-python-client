import nft_storage
from nft_storage.api import nft_storage_api
import yaml
from io import BytesIO
import requests
import json


properties = yaml.safe_load(open('./nft.yml'))

configuration = nft_storage.Configuration(
    host = properties['nft']['host']
)

configuration = nft_storage.Configuration(
    access_token = properties['nft']['API_KEY']
)

def save(data, type):
    with nft_storage.ApiClient(configuration) as client:
        storage = nft_storage_api.NFTStorageAPI(client)

        try:
            if(type == 'file'):
                fileData = open(data, 'rb')
                read_json = json.load(fileData)
                body = BytesIO(bytes(get_minimize_data(read_json), 'utf-8'))
            else :
                if(type == 'json'):
                    body = BytesIO(bytes(get_minimize_data(data), 'utf-8'))
                else:
                    raise Exception("Sorry, Ortelius do not support "+type+" as of now. Valid types are Json or file")

            return storage.store(body,  _check_return_type=False)

        except nft_storage.ApiException as e:
            print("Exception when calling nft_storage_utils.save(): %s\n" % e)
            return e
        except Exception as e:
            print("Exception when calling nft_storage_utils.save(): %s\n" % e)
            return e
        finally:
            client.close()

def check(cid):
    with nft_storage.ApiClient() as client:
        storage = nft_storage_api.NFTStorageAPI(client)
        try:
            return storage.check(cid, _check_return_type=False)
        except nft_storage.ApiException as e:
            print("Exception when calling nft_storage_utils.check(): %s\n" % e)
            return e

def status(cid):
    with nft_storage.ApiClient(configuration) as api_client:
        storage = nft_storage_api.NFTStorageAPI(api_client)
        try:
            return storage.status(cid, _check_return_type=False)
        except nft_storage.ApiException as e:
            print("Exception when calling nft_storage_utils.status(): %s\n" % e)
            return e

def getData(cid):
    try:
        url = f"https://ipfs.io/ipfs/{cid}?format=json"
        response = requests.get(url)
        data = get_minimize_data(response.json())
        # print(data)
        return data
    except nft_storage.ApiException as e:
        print("Exception when calling nft_storage_utils.getData(): %s\n" % e)
        return e


def get_minimize_data(jsonData):
  sorted_by_key = get_sorted(jsonData)
  return json.dumps(sorted_by_key, separators=(',', ':'))

def get_sorted(dictionaryOrList):

  if(isinstance(dictionaryOrList, dict)):
    return get_sorted_object(dictionaryOrList)
  elif(isinstance(dictionaryOrList, list)):
    collector = []
    for element in dictionaryOrList:
      collector.append(get_sorted_object(element))
    return collector
  
  return dictionaryOrList
    
    
def get_sorted_object(dictionary):
  for key in dictionary:
    if(isinstance(dictionary[key], list) and dictionary[key].__len__() != 0 and isinstance(dictionary[key][0], dict)):
      collector = []
      for element in dictionary[key]:
        collector.append(get_sorted(element))
    
      dictionary[key] = collector

    elif(isinstance(dictionary[key], list) and dictionary[key].__len__() != 0 and isinstance(dictionary[key][0], str)):
      dictionary[key].sort()

    elif(isinstance(dictionary[key], list) and dictionary[key].__len__() != 0 and isinstance(dictionary[key][0], int)):
      dictionary[key].sort()

    elif(isinstance(dictionary[key], list) and dictionary[key].__len__() != 0 and isinstance(dictionary[key][0], float)):
      dictionary[key].sort()

    elif(isinstance(dictionary[key], dict)):
      dictionary[key] = get_sorted(dictionary[key])
    
  return sort_dict_by_key(dictionary)

def sort_dict_by_key(dictionary):
  sorted_keys = sorted(dictionary.keys())
  return {key:dictionary[key] for key in sorted_keys}

