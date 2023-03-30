"""Ortelius Class Defintions and Reusable functions."""

import json
import logging
import re

from ortelius import storage

__all__ = ["normalize", "convert_object_to_cid", "get_clean_json", "detect_inner_object", "convert_to_dict", "de_normalize", "decode_nft_helper", "convert_cid_to_object", "detect_nft", "remove_key"]

# Create a logger object.
logger = logging.getLogger(__name__)


def remove_key(obj):
    """
    This method scrolls the entire 'obj' to delete every key for which the regex returns
    True

    :param obj: a dictionary or a list of dictionaries to clean
    """
    if isinstance(obj, dict):
        # the call to `list` is useless for py2 but makes
        # the code py2/py3 compatible
        for key in list(obj.keys()):
            if re.match(r"^_key", str(key)):
                del obj[key]
            else:
                remove_key(obj[key])
    elif isinstance(obj, list):
        for i in reversed(range(len(obj))):
            if re.match(r"^_key", str(obj[i])):
                del obj[i]
            else:
                remove_key(obj[i])
    else:
        # neither a dict nor a list, do nothing
        pass


# This method will wrap json object and store all the nested objects as NFT recersively
def normalize(sbom):
    if isinstance(sbom, dict):
        for key in sbom:
            if isinstance(sbom[key], dict):
                sbom[key] = convert_object_to_cid(sbom[key])

            elif isinstance(sbom[key], list):
                list_of_element = []
                for elem in sbom[key]:
                    list_of_element.append(convert_object_to_cid(elem))
                sbom[key] = list_of_element

    elif isinstance(sbom, list):
        list_of_cids = []
        for elem in sbom:
            list_of_cids.append(convert_object_to_cid(elem))
        return list_of_cids
    return sbom


def convert_object_to_cid(json_data):
    if isinstance(json_data, list):
        list_of_cids = []
        for elem in json_data:
            list_of_cids.append(convert_object_to_cid(elem))
        return list_of_cids

    elif isinstance(json_data, dict) and detect_inner_object(json_data):
        # logger.debug("++ inner_object found inside ++" + str(jsonData))
        for key in json_data:
            if isinstance(json_data[key], dict):
                json_data[key] = convert_object_to_cid(json_data[key])
                get_clean_json(json_data)
                minified_json_element = storage.get_minimize_data(json_data)
                response = storage.save(minified_json_element, "json")
                return "ipfs://" + response["value"]["cid"]

            elif isinstance(json_data[key], list):
                list_of_element = []
                for elem in json_data[key]:
                    list_of_element.append(convert_object_to_cid(elem))
                json_data[key] = list_of_element
                get_clean_json(json_data)
                minified_json_element = storage.get_minimize_data(json_data)
                response = storage.save(minified_json_element, "json")
                return "ipfs://" + response["value"]["cid"]
    elif isinstance(json_data, dict):
        get_clean_json(json_data)
        minified_json_element = storage.get_minimize_data(json_data)
        response = storage.save(minified_json_element, "json")
        cid = response["value"]["cid"]
        return "ipfs://" + str(cid)

    else:
        return json_data


def get_clean_json(json_obj):
    json_obj.pop("_key", "No Key found")


def detect_inner_object(json_data):
    # logger.debug("++ traversing inside Object ++")
    for key in json_data:
        if isinstance(json_data[key], dict) or isinstance(json_data[key], list):
            return True


def convert_to_dict(obj):
    return json.loads(json.dumps(obj, default=lambda o: o.__dict__))


# Unwrap nft data to actual nested Json Object
def de_normalize(sbom):
    if isinstance(sbom, list):
        list_of_element = []
        for each_obj in sbom:
            list_of_element.append(decode_nft_helper(each_obj))

        return list_of_element

    elif isinstance(sbom, dict):
        return decode_nft_helper(sbom)

    return sbom


def decode_nft_helper(sbom):
    if isinstance(sbom, dict):
        for key in sbom:
            if isinstance(sbom[key], str) and detect_nft(sbom[key]) is not None:
                sbom[key] = convert_cid_to_object(sbom[key])

            elif isinstance(sbom[key], list):
                list_of_element = []
                for maybe_cid in sbom[key]:
                    if detect_nft(maybe_cid) is not None:
                        list_of_element.append(convert_cid_to_object(maybe_cid))
                    else:
                        list_of_element.append(maybe_cid)

                sbom[key] = list_of_element

    elif isinstance(sbom, str) and detect_nft(sbom) is not None:
        return convert_cid_to_object(sbom)

    return sbom


def convert_cid_to_object(cid):
    address = cid.split("://")[1]
    fetched_cid_data = json.loads(storage.get_cid_data(address))

    if isinstance(fetched_cid_data, dict):
        for key in fetched_cid_data:
            # logger.debug("detecting cids in --" + str(fetched_cid_data))
            if isinstance(fetched_cid_data[key], str) and detect_nft(fetched_cid_data[key]):
                # logger.debug("---- unwraping again inside ----"+ str(fetched_cid_data))
                fetched_cid_data[key] = convert_cid_to_object(fetched_cid_data[key])
            elif isinstance(fetched_cid_data[key], list):
                list_of_element = []
                for maybe_cid in fetched_cid_data[key]:
                    if detect_nft(maybe_cid) is not None:
                        list_of_element.append(convert_cid_to_object(maybe_cid))
                    else:
                        list_of_element.append(maybe_cid)

                fetched_cid_data[key] = list_of_element

    fetched_cid_data["_key"] = cid
    return fetched_cid_data


IPFS_REGEX = r"^ipfs://Qm[1-9A-HJ-NP-Za-km-z]{44,}|^ipfs://b[A-Za-z2-7]{58,}|^ipfs://B[A-Z2-7]{58,}|^ipfs://z[1-9A-HJ-NP-Za-km-z]{48,}|^ipfs://F[0-9A-F]{50,}"


# this method checks if this value is valid IPFS url or not
def detect_nft(value):
    if not str(value).startswith("ipfs:"):
        return None
    pattern = re.compile(IPFS_REGEX, re.IGNORECASE)
    return pattern.match(value)
