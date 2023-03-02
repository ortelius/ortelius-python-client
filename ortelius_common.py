"""Ortelius Class Defintions and Reusable functions."""
from __future__ import annotations
import hashlib
import os
from datetime import datetime
import socket
from typing import Optional
import copy

import requests
from fastapi import HTTPException, Request, status
from pydantic import BaseModel
from pprint import pprint
import json
from collections import defaultdict
import re
import normalize_api

class StatusMsg(BaseModel):
    status: str
    service_name: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "status": "UP",
                "service_name": "ms-compver-crud"
            }
        }

class Domain(BaseModel):
    _key: str
    name: str

    class Config:
        schema_extra = {
            "example": {
                "_key": 1,
                "name": "GLOBAL"
            }
        }

class User(BaseModel):
    _key: str
    name: str
    domain: Domain
    email: Optional[str] = None
    phone: Optional[str] = None
    realname: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "_key": 1,
                "name": "admin",
                "domain": {
                    "_key": 1,
                    "name": "GLOBAL"
                },
                "name": "admin",
                "email": "admin@ortelius.io",
                "phone": "505-444-5566",
                "realname": "Ortelius Admin"
            }
        }


class Group(BaseModel):
    _key: str
    name: str
    domain: Domain

    class Config:
        schema_extra = {
            "example": {
                "_key": 1,
                "name": "Administrators",
                "domain": {
                    "_key": 1,
                    "name": "GLOBAL"
                }
            }
        }


class Groups2Users(BaseModel):
    group_key: str
    user_key: str

    class Config:
        schema_extra = {
            "example": {
                "goup_key": 1,
                "user_key": 1
            }
        }


class GroupsForUser(BaseModel):
    groups: Optional[list[Group]] = None

    class Config:
        schema_extra = {
            "example": {
                "groups": [
                    {
                        "_key": 1,
                        "name": "Administrators",
                        "domain": {
                            "_key": 1,
                            "name": "GLOBAL"
                        }
                    }
                ]
            }
        }


class UsersForGroup(BaseModel):
    users: Optional[list[User]] = None

    class Config:
        schema_extra = {
            "example": {
                "users": [
                    {
                        "_key": 1,
                        "name": "admin",
                        "domain": {
                            "_key": 1,
                            "name": "GLOBAL"
                        },
                        "email": "admin@ortelius.io",
                        "phone": "505-444-5566",
                        "realname": "Ortelius Admin"
                    }
                ]
            }
        }


class AuditRecord(BaseModel):
    _key: str
    action: str
    user: User
    when: datetime

    class Config:
        schema_extra = {
            "example": {
                "_key": 1,
                "action": "Created",
                "user": {
                    "domain": {
                        "_key": 1,
                        "name": "GLOBAL"
                    },
                    "email": "admin@ortelius.io",
                    "name": "admin",
                    "phone": "505-444-5566",
                    "realname": "Ortelius Admin"
                },
                "when": '2023-04-23T10:20:30.400+02:30'
            }
        }


class Package(BaseModel):
    purl: str
    name: str
    version: str
    license_key: str
    license: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "purl": "pkg:deb/debian/libc-bin@2.19-18+deb8u7?arch=amd64&upstream=glibc&distro=debian-8",
                "name": "libc-bin",
                "version": "2.19.18+deb8u7",
                "license_key": 23,
                "license": "GP-2.0"
            }
        }


class Readme(BaseModel):
    _key: str
    content: list[str]

    class Config:
        schema_extra = {
            "example": {
                "_key": 2344,
                "content": [
                    "# README",
                    "## Sample"
                ]
            }
        }


class License(BaseModel):
    _key: str
    content: list[str]

    class Config:
        schema_extra = {
            "example": {
                "_key": 1244,
                "content": [
                    "# Apache 2",
                    "## Summary"
                ]
            }
        }


class Swagger(BaseModel):
    _key: str
    content: list[str]

    class Config:
        schema_extra = {
            "example": {
                "_key": 334,
                "content": [
                    "# Rest APIs",
                    "## GET /user"
                ]
            }
        }


class Vulnerabilty(BaseModel):
    _key: str
    name: str

    class Config:
        schema_extra = {
            "example": {
                "_key": 5534,
                "name": "CVE-1823"
            }
        }


class Providing(BaseModel):
    _key: str
    provides: list[str]

    class Config:
        schema_extra = {
            "example": {
                "_key": 5987,
                "provides": [
                    "/user"
                ]
            }
        }


class Consuming(BaseModel):
    _key: str
    comsumes: list[str]

    class Config:
        schema_extra = {
            "example": {
                "_key": 911,
                "consumes": [
                    "/user"
                ]
            }
        }


class ComponentVersion(BaseModel):
    _key: str
    name: str
    domain: Domain
    parent: Optional[ComponentVersion] = None
    predecessor: Optional[ComponentVersion] = None

    class Config:
        schema_extra = {
            "example": {
                "_key": 911,
                "name": "Hello World;v1.0.0",
                "domain": {
                    "_key": 100,
                    "name": "GLOBAL.My Project"
                },
                "parent": None,
                "predecessor": None
            }
        }


class ApplicationVersion(BaseModel):
    _key: str
    name: str
    domain: Domain
    parent: Optional[ApplicationVersion] = None
    predecessor: Optional[ApplicationVersion] = None
    deployments: Optional[list[int]] = None

    class Config:
        schema_extra = {
            "example": {
                "_key": 554,
                "name": "Hello App;v1",
                "domain": {
                    "_key": 100,
                    "name": "GLOBAL.My Project"
                },
                "parent": None,
                "predecessor": None,
                "deployments": [
                    121
                ]
            }
        }


class CompAttrs(BaseModel):
    builddate: Optional[str] = None
    buildid: Optional[str] = None
    buildurl: Optional[str] = None
    chart: Optional[str] = None
    chartnamespace: Optional[str] = None
    chartrepo: Optional[str] = None
    chartrepourl: Optional[str] = None
    chartversion: Optional[str] = None
    discordchannel: Optional[str] = None
    dockerrepo: Optional[str] = None
    dockersha: Optional[str] = None
    dockertag: Optional[str] = None
    gitcommit: Optional[str] = None
    gitrepo: Optional[str] = None
    gittag: Optional[str] = None
    giturl: Optional[str] = None
    hipchatchannel: Optional[str] = None
    pagerdutybusinessurl: Optional[str] = None
    pagerdutyurl: Optional[str] = None
    repository: Optional[str] = None
    serviceowner: Optional[User] = None
    slackchannel: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "builddate": "Mon Jan 31 16:18:26 2022",
                "build_key": "178",
                "buildurl": "https://circleci.com/gh/ortelius/store-cartservice/178",
                "chart": "chart/ms-cartservice",
                "chartnamespace": "default",
                "chartrepo": "msproject/ms-chartservice",
                "chartrepourl": "https://helm.msprogject/stable/msproject/ms-chartservice",
                "chartversion": "1.0.0",
                "discordchannel": "https://discord.gg/A4hx3",
                "dockerrepo": "myproject/ms-chartservice",
                "dockersha": "5d3d677e1",
                "dockertag": "v1.0.0",
                "gitcommit": "2adc111",
                "gitrepo": "msproject/ms-chartservice",
                "gittag": "main",
                "giturl": "https://github.com/msproject/ms-chartservice",
                "hipchatchannel": "",
                "pagerdutybusinessurl": "https://pagerduty.com/business/ms-chartservice",
                "pagerdutyurl": "https://pagerduty.com/business/ms-chartservice",
                "serviceowner": {
                    "_key": 1,
                    "name": "admin",
                    "domain": "GLOBAL",
                    "email": "admin@ortelius.io",
                    "phone": "505-444-5566",
                    "realname": "Ortelius Admin"
                },
                "slackchannel": "https://myproject.slack.com/444aaa"
            }
        }


class ComponentVersionDetails(ComponentVersion):
    owner: User
    creator: User
    created: datetime
    comptype: str
    packages: Optional[list[Package]] = None
    vulnerabilties: Optional[list[Vulnerabilty]] = None
    readme: Optional[Readme] = None
    license: Optional[License] = None
    swagger: Optional[Swagger] = None
    applications: Optional[list[ApplicationVersion]] = None
    providing: Optional[Providing] = None
    consuming: Optional[Consuming] = None
    attrs: Optional[CompAttrs] = None
    auditlog: Optional[list[AuditRecord]] = None

    class Config:
        schema_extra = {
            "example": {
                "_key": 911,
                "name": "Hello World;v1.0.0",
                "domain": {
                    "_key": 100,
                    "name": "GLOBAL.My Project"
                },
                "parent": None,
                "predecessor": None,
                "owner": {
                    "_key": 1,
                    "name": "admin",
                    "domain": {
                        "_key": 1,
                        "name": "GLOBAL"
                    },
                    "email": "admin@ortelius.io",
                    "phone": "505-444-5566",
                    "realname": "Ortelius Admin"
                },
                "creator": {
                    "_key": 1,
                    "name": "admin",
                    "domain": {
                        "_key": 1,
                        "name": "GLOBAL"
                    },
                    "email": "admin@ortelius.io",
                    "phone": "505-444-5566",
                    "realname": "Ortelius Admin"
                },
                "created": '2023-04-23T10:20:30.400+02:30',
                "comptype": "docker",
                "packages": [
                    {
                        "purl": "pkg:deb/debian/libc-bin@2.19-18+deb8u7?arch=amd64&upstream=glibc&distro=debian-8",
                        "name": "libc-bin",
                        "version": "2.19.18+deb8u7",
                        "license_key": 23,
                        "license": "GP-2.0"
                    }
                ],
                "vulnerabilties": [
                    {
                        "_key": 5534,
                        "name": "CVE-1823"
                    }
                ],
                "readme": {
                    "_key": 2344,
                    "content": [
                        "# README",
                        "## Sample"
                    ]
                },
                "license": {
                    "_key": 1244,
                    "content": [
                        "# Apache 2",
                        "## Summary"
                    ]
                },
                "swagger": {
                    "_key": 334,
                    "content": [
                        "# Rest APIs",
                        "## GET /user"
                    ]
                },
                "applications": [

                ],
                "providing": {
                    "_key": 5987,
                    "provides": [
                        "/user"
                    ]
                },
                "consuming": {
                    "_key": 911,
                    "consumes": [
                        "/user"
                    ]
                },
                "attrs": {
                "builddate": "Mon Jan 31 16:18:26 2022",
                "build_key": "178",
                "buildurl": "https://circleci.com/gh/ortelius/store-cartservice/178",
                "chart": "chart/ms-cartservice",
                "chartnamespace": "default",
                "chartrepo": "msproject/ms-chartservice",
                "chartrepourl": "https://helm.msprogject/stable/msproject/ms-chartservice",
                "chartversion": "1.0.0",
                "discordchannel": "https://discord.gg/A4hx3",
                "dockerrepo": "myproject/ms-chartservice",
                "dockersha": "5d3d677e1",
                "dockertag": "v1.0.0",
                "gitcommit": "2adc111",
                "gitrepo": "msproject/ms-chartservice",
                "gittag": "main",
                "giturl": "https://github.com/msproject/ms-chartservice",
                "hipchatchannel": "",
                "pagerdutybusinessurl": "https://pagerduty.com/business/ms-chartservice",
                "pagerdutyurl": "https://pagerduty.com/business/ms-chartservice",
                "serviceowner": {
                    "_key": 1,
                    "name": "admin",
                    "domain": "GLOBAL",
                    "email": "admin@ortelius.io",
                    "phone": "505-444-5566",
                    "realname": "Ortelius Admin"
                },
                "slackchannel": "https://myproject.slack.com/444aaa"
            }
            }
        }


class ApplicationVersionDetails(ApplicationVersion):
    owner: User
    creator: User
    created: datetime
    components: Optional[list[ComponentVersion]] = None
    auditlog: Optional[list[AuditRecord]] = None

    class Config:
        schema_extra = {
            "example": {
                "_key": 554,
                "name": "Hello App;v1",
                "domain": {
                    "_key": 100,
                    "name": "GLOBAL.My Project"
                },
                "parent": None,
                "predecessor": None,
                "deployments": None,
                "owner": {
                    "_key": 1,
                    "name": "admin",
                    "domain": {
                        "_key": 1,
                        "name": "GLOBAL"
                    },
                    "email": "admin@ortelius.io",
                    "phone": "505-444-5566",
                    "realname": "Ortelius Admin"
                },
                "creator": {
                    "_key": 1,
                    "name": "admin",
                    "domain": {
                        "_key": 1,
                        "name": "GLOBAL"
                    },
                    "email": "admin@ortelius.io",
                    "phone": "505-444-5566",
                    "realname": "Ortelius Admin"
                },
                "created": '2023-04-23T10:20:30.400+02:30',
                "components": [
                    {
                        "_key": 911,
                        "name": "Hello World;v1.0.0",
                        "domain": {
                            "_key": 100,
                            "name": "GLOBAL.My Project"
                        },
                        "parent": None,
                        "predecessor": None
                    }
                ],
                "auditlog": None
            }
        }


class Environment(BaseModel):
    _key: str
    name: str
    domain: str
    owner: User
    creator: User
    created: datetime

    class Config:
        schema_extra = {
            "example": {
                "_key": 911,
                "name": "Hello World;v1.0.0",
                "domain": "GLOBAL.My Project",
                "owner": {
                    "_key": 1,
                    "name": "admin",
                    "domain": {
                        "_key": 1,
                        "name": "GLOBAL"
                    },
                    "name": "admin",
                    "email": "admin@ortelius.io",
                    "phone": "505-444-5566",
                    "realname": "Ortelius Admin"
                },
                "creator": {
                    "_key": 1,
                    "name": "admin",
                    "domain": {
                        "_key": 1,
                        "name": "GLOBAL"
                    },
                    "name": "admin",
                    "email": "admin@ortelius.io",
                    "phone": "505-444-5566",
                    "realname": "Ortelius Admin"
                },
                "created": '2023-04-23T10:20:30.400+02:30'
            }
        }


class Deployment(BaseModel):
    _key: str
    environment: Environment
    application: ApplicationVersion
    components: list[ComponentVersion]
    starttime: datetime
    endtime: Optional[datetime] = None
    result: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "environment": {
                    "_key": 911,
                    "name": "Hello World;v1.0.0",
                    "domain": "GLOBAL.My Project",
                    "owner": {
                        "_key": 1,
                        "name": "admin",
                        "domain": {
                            "_key": 1,
                            "name": "GLOBAL"
                        },
                        "email": "admin@ortelius.io",
                        "phone": "505-444-5566",
                        "realname": "Ortelius Admin"
                    },
                    "creator": {
                        "_key": 1,
                        "name": "admin",
                        "domain": {
                            "_key": 1,
                            "name": "GLOBAL"
                        },
                        "email": "admin@ortelius.io",
                        "phone": "505-444-5566",
                        "realname": "Ortelius Admin"
                    },
                    "created": '2023-04-23T10:20:30.400+02:30'
                },
                "application": {
                    "_key": 554,
                    "name": "Hello App;v1",
                    "domain": {
                        "_key": 100,
                        "name": "GLOBAL.My Project"
                    },
                    "parent": None,
                    "predecessor": None,
                    "deployments": None
                },
                "components": [
                    {
                        "_key": 911,
                        "name": "Hello World;v1.0.0",
                        "domain": {
                            "_key": 100,
                            "name": "GLOBAL.My Project"
                        },
                        "parent": None,
                        "predecessor": None,
                    }
                ],
                "starttime": '2023-04-23T10:20:30.400+02:30',
                "endtime": '2023-04-23T10:30:30.400+02:30',
                "result": 0
            }
        }


class DeploymentDetails(Deployment):
    log: Optional[list[str]] = None

    class Config:
        schema_extra = {
            "example": {
                "environment": {
                    "_key": 911,
                    "name": "Hello World;v1.0.0",
                    "domain": "GLOBAL.My Project",
                    "owner": {
                        "_key": 1,
                        "name": "admin",
                        "domain": {
                            "_key": 1,
                            "name": "GLOBAL"
                        },
                        "email": "admin@ortelius.io",
                        "phone": "505-444-5566",
                        "realname": "Ortelius Admin"
                    },
                    "creator": {
                        "_key": 1,
                        "name": "admin",
                        "domain": {
                            "_key": 1,
                            "name": "GLOBAL"
                        },
                        "email": "admin@ortelius.io",
                        "phone": "505-444-5566",
                        "realname": "Ortelius Admin"
                    },
                    "created": '2023-04-23T10:20:30.400+02:30'
                },
                "application": {
                    "_key": 554,
                    "name": "Hello App;v1",
                    "domain": {
                        "_key": 100,
                        "name": "GLOBAL.My Project"
                    },
                    "parent": None,
                    "predecessor": None,
                    "deployments": None
                },
                "components": [
                    {
                        "_key": 911,
                        "name": "Hello World;v1.0.0",
                        "domain": {
                            "_key": 1,
                            "name": "GLOBAL.My Project"
                        },
                        "parent": None,
                        "predecessor": None,
                    }
                ],
                "starttime": '2023-04-23T10:20:30.400+02:30',
                "endtime": '2023-04-23T10:30:30.400+02:30',
                "result": 0
            },
            "log": [
                "Deploying Hello World",
                "Success"
            ]
        }

class AllModels(BaseModel):
    user: User
    group: Group
    group2users: Groups2Users
    groups4user: GroupsForUser
    user4group: UsersForGroup
    audit_record: AuditRecord
    package: Package
    readme: Readme
    license: License
    swagger: Swagger
    vulnerabilty: Vulnerabilty
    providing: Providing
    consuming: Consuming
    component_version: ComponentVersion
    application_version: ApplicationVersion
    comp_attrs: CompAttrs
    component_version_details: ComponentVersionDetails
    application_version_details: ApplicationVersionDetails
    environment: Environment
    deployment: Deployment
    deployment_details: DeploymentDetails


def validate_user(request: Request):
    try:
        validateuser_url = os.getenv('VALIDATEUSER_URL', None)

        if (validateuser_url is None):
            validateuser_host = os.getenv('MS_VALIDATE_USER_SERVICE_HOST', '127.0.0.1')
            host = socket.gethostbyaddr(validateuser_host)[0]
            validateuser_url = 'http://' + host + ':' + str(os.getenv('MS_VALIDATE_USER_SERVICE_PORT', 80))

        result = requests.get(validateuser_url + "/msapi/validateuser", cookies=request.cookies)
        if (result is None):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization Failed")

        if (result.status_code != status.HTTP_200_OK):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization Failed status_code=" + str(result.status_code))
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization Failed:" + str(err)) from None

def hash_dict(d):
    return hashlib.sha1(json.dumps(d, sort_keys=True).encode('utf-8')).hexdigest()


def revnest(objlist, unnested):

    for inp in objlist:
        for name, obj in inp.items():
            if (unnested.get(name, None) is None):
                unnested.update({ name: {} })

            for k, v in obj.items():
                if (type(v) == dict):
                    objtype = k
                    if (k in ['owner', 'creator', 'serviceowner']):
                        objtype = 'user'
                    v['_type'] = objtype

                    if (v.get('_key', None) is not None):
                        del v['_key']
                        nft_key  = hashlib.sha1(json.dumps(v, sort_keys=True).encode('utf-8')).hexdigest()
                    else:
                        nft_key = hashlib.sha1(json.dumps(v, sort_keys=True).encode('utf-8')).hexdigest()

                    for def_key, def_val in unnested.items():
                        if (type(def_val) == dict and hash_dict(def_val) == hash_dict(v)):
                            nft_key = def_key
                            break

                    unnested[nft_key] = v
                    unnested[name].update({k: nft_key})
                else:
                    unnested[name].update({k: v})

            updated_obj = unnested[name]
            objtype = name.lower()
            if (k in ['owner', 'creator', 'serviceowner']):
                objtype = 'user'
            updated_obj['_type'] = objtype

            if (updated_obj.get('_key', None) is not None):
                del updated_obj['_key']
                nft_key  = hashlib.sha1(json.dumps(v, sort_keys=True).encode('utf-8')).hexdigest()
            else:
                nft_key = hashlib.sha1(json.dumps(v, sort_keys=True).encode('utf-8')).hexdigest()

            unnested[nft_key] = updated_obj
            del unnested[name]


def resolve_hashes(unnested):
    denorm = copy.deepcopy(unnested)

    for k, v in unnested.items():
        if (not is_hex(k)):
            if (v.get('_key', None) is not None):
                del v['_key']

            v['_type'] = k.lower()

            nft_key = hashlib.sha1(json.dumps(v, sort_keys=True).encode('utf-8')).hexdigest()
            denorm[nft_key] = v
            del denorm[k]

    return denorm

def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False

def invert(jsonfile):
     with open(jsonfile) as jfile:
        objlist = json.load(jfile)
        unnested = {}
        revnest(objlist,unnested)
        # denorm = resolve_hashes(unnested)
        print(json.dumps(unnested, sort_keys=True))

def normalize(sbom):
    return normalize_api.normalize(sbom)

def de_normalize(sbom):
    return normalize_api.de_normalize(sbom)

if __name__ == "__main__":
    # print(AllModels.schema_json())
    invert('denormalized.json')

