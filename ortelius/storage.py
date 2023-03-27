"""Ortelius Class Defintions and Reusable functions."""

import json
from io import BytesIO

import nft_storage
import requests
import yaml
from nft_storage.api import nft_storage_api

__all__ = ["save", "check", "status", "get_cid_data", "get_minimize_data"]


properties = {}
with open("nft.yml", mode="r", encoding="utf-8") as file_nft:
    properties = yaml.safe_load(file_nft)

configuration = nft_storage.Configuration(host=properties["nft"]["host"], access_token=properties["nft"]["API_KEY"])


def save(data, objtype):
    with nft_storage.ApiClient(configuration) as client:
        storage = nft_storage_api.NFTStorageAPI(client)

        try:
            if objtype == "file":
                file_data = open(data, "rb")
                read_json = json.load(file_data)
                body = BytesIO(bytes(get_minimize_data(read_json), "utf-8"))
            else:
                if objtype == "json":
                    body = BytesIO(bytes(get_minimize_data(data), "utf-8"))
                else:
                    raise Exception(f"Sorry, Ortelius do not support {objtype} as of now. Valid types are Json or file")

            return storage.store(body, _check_return_type=False)

        except nft_storage.ApiException as ex:
            print(f"Exception when calling nft_storage_utils.save(): {ex}\n")
            return ex
        except Exception as ex:
            print(f"Exception when calling nft_storage_utils.save(): {ex}\n")
            return ex
        finally:
            client.close()


def check(cid):
    with nft_storage.ApiClient() as client:
        storage = nft_storage_api.NFTStorageAPI(client)
        try:
            return storage.check(cid, _check_return_type=False)
        except nft_storage.ApiException as ex:
            print(f"Exception when calling nft_storage_utils.check(): {ex}\n")
            return ex


def status(cid):
    with nft_storage.ApiClient(configuration) as api_client:
        storage = nft_storage_api.NFTStorageAPI(api_client)
        try:
            return storage.status(cid, _check_return_type=False)
        except nft_storage.ApiException as ex:
            print(f"Exception when calling nft_storage_utils.status(): {ex}\n")
            return ex


def get_cid_data(cid):
    try:
        url = f"https://ipfs.io/ipfs/{cid}?format=json"
        response = requests.get(url, timeout=20)
        # print("Going to minimize:: "+ str(response.json()))
        data = get_minimize_data(response.json())
        # print(data)
        return data
    except nft_storage.ApiException as ex:
        print(f"Exception when calling nft_storage_utils.get_data_cid(): {ex}\n")
        return ex


def get_minimize_data(json_data):
    sorted_by_key = get_sorted(json_data)
    return json.dumps(sorted_by_key, separators=(",", ":"))


def get_sorted(dictionary_or_list):
    if isinstance(dictionary_or_list, dict):
        return get_sorted_object(dictionary_or_list)
    elif isinstance(dictionary_or_list, list):
        collector = []
        for element in dictionary_or_list:
            collector.append(get_sorted_object(element))
        return collector

    return dictionary_or_list


def get_sorted_object(dictionary):
    for key in dictionary:
        if isinstance(dictionary[key], list) and len(dictionary[key]) != 0 and isinstance(dictionary[key][0], dict):
            collector = []
            for element in dictionary[key]:
                collector.append(get_sorted(element))

            dictionary[key] = collector

        elif isinstance(dictionary[key], list) and len(dictionary[key]) != 0 and isinstance(dictionary[key][0], str):
            dictionary[key].sort()

        elif isinstance(dictionary[key], list) and len(dictionary[key]) != 0 and isinstance(dictionary[key][0], int):
            dictionary[key].sort()

        elif isinstance(dictionary[key], list) and len(dictionary[key]) != 0 and isinstance(dictionary[key][0], float):
            dictionary[key].sort()

        elif isinstance(dictionary[key], dict):
            dictionary[key] = get_sorted(dictionary[key])

    return sort_dict_by_key(dictionary)


def sort_dict_by_key(dictionary):
    sorted_keys = sorted(dictionary.keys())
    return {key: dictionary[key] for key in sorted_keys}
