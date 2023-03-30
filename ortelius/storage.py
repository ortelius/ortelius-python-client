"""Ortelius Class Defintions and Reusable functions."""

import json

import requests
import yaml

__all__ = ["save", "check", "status", "get_cid_data", "get_minimize_data"]


properties = {}
with open("nft.yml", mode="r", encoding="utf-8") as file_nft:
    properties = yaml.safe_load(file_nft)


def save(data, objtype):
    #
    # TODO: Create a Convert files to content-addressable archives (.car)
    #       No native python library exists.  Need to copy https://www.npmjs.com/package/ipfs-car
    #       echo -n '{"name":"GLOBAL"}' | ipfs-car pack --output a.car
    #
    #       Then use Content-Type: application/car instead of image/*
    #

    host = properties["nft"]["host"]
    access_token = properties["nft"]["API_KEY"]
    headers = {"Authorization": "Bearer " + access_token, "accept": "application/json", "Content-Type": "image/*"}
    min_data = data

    if objtype == "file":
        file_data = open(data, mode="r", encoding="utf-8")
        read_json = json.load(file_data)
        min_data = get_minimize_data(read_json)

    response = requests.post(f"{host}/upload", headers=headers, data=min_data, timeout=10)
    return response.json()


def check(cid):
    host = properties["nft"]["host"]
    access_token = properties["nft"]["API_KEY"]
    headers = {"Authorization": "Bearer " + access_token, "accept": "application/json"}

    response = requests.get(f"{host}/check/{cid}", headers=headers, timeout=10)
    return response.json()


def status(cid):
    host = properties["nft"]["host"]
    access_token = properties["nft"]["API_KEY"]
    headers = {"Authorization": "Bearer " + access_token, "accept": "application/json"}

    response = requests.get(f"{host}/{cid}", headers=headers, timeout=10)
    return response.json()


def get_cid_data(cid):
    url = f"https://{cid}.ipfs.nftstorage.link/?format=json"
    response = requests.get(url, headers={"accept": "application/json"}, timeout=10)
    data = get_minimize_data(response.json())
    return data


def get_cid_json(cid):
    url = f"https://{cid}.ipfs.nftstorage.link/?format=json"
    response = requests.get(url, headers={"accept": "application/json"}, timeout=10)
    return response.json()


def get_minimize_data(json_data):
    sorted_by_key = get_sorted(json_data)
    return json.dumps(sorted_by_key, separators=(",", ":"))


def get_sorted(dictionary_or_list):
    if isinstance(dictionary_or_list, dict):
        return get_sorted_object(dictionary_or_list)

    if isinstance(dictionary_or_list, list):
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
