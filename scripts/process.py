#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 The Pegasus Team.

import datetime
import os
import requests
import yaml
import sys

from string import Template
import logging
import logging.config

from jsonschema import validate, Draft7Validator
from jsonschema.exceptions import ValidationError

HEADERS = {
    "Accept": "application/vnd.github.mercy-preview+json",
    "Authorization": "token {}".format(os.environ.get("PEGASUSHUB_TOKEN", "")),
}
# HEADERS = {}

SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "repo_name": {"type": "string", "minLength": 1},
            "organization": {"type": "string", "minLength": 1},
            "highlight": {"type": "boolean"},
            "training": {"type": "boolean"},
            "priority": {"type": "integer", "minimum": 0, "maximum": 5},
            "execution_sites": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "string",
                    "enum": [
                        "CONDORPOOL",
                        "SLURM",
                        "SUMMIT_GLITE",
                        "LSF",
                        "SGE",
                        "SUMMIT_KUBERNETES",
                    ],
                },
            },
        },
        "additionalProperties": False,
        "required": ["repo_name", "organization"],
        "anyOf": [
            {
                "not": {
                    "properties": {"highlight": {"const": True}},
                    "required": ["highlight"],
                }
            },
            {"required": ["priority"]},
        ],
    },
}


def validate_yaml(data):
    validator = Draft7Validator(SCHEMA)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
    is_error = False
    # print(error.path)
    for error in errors:
        if error.validator == "anyOf":
            print(error.context[-1])
            logger.error(error.context[-1])
        elif error.validator in ["type", "maximum", "minimum"]:
            print(
                error.message,
                " in ",
                error.schema_path[-2],
                " at index ",
                error.json_path.split("]")[0][2:],
            )
            logger.error(
                f"{error.message} in {error.schema_path[-2]} at index {error.json_path.split(']')[0][2:]}"
            )
        else:
            print(error.message)
            logger.error(error.message)
        is_error = True
    return is_error


def get_repo_info(w, response):
    logger.info(f"{w['repo_name']} is being populated\n")
    # repo general information
    w["title"] = response["name"]
    w["stargazers"] = response["stargazers_count"]
    w["default_branch"] = response["default_branch"]
    w["subtitle"] = (
        response["description"]
        if response["description"]
        else "No description provided"
    )
    w["license"] = (
        response["license"]["name"] if response["license"] else "No license available"
    )
    w["issues"] = response["open_issues"]
    w["forks"] = response["forks"]

    # date
    date = datetime.datetime.strptime(response["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
    w["year"] = date.strftime("%Y")
    w["month"] = date.strftime("%b")
    w["monthn"] = date.strftime("%m")
    w["day"] = date.strftime("%d")

    # topics
    w["topics"] = "No topics available"
    w["tags"] = ""
    topics = response["topics"]
    if len(topics) > 0:
        w["topics"] = ""
        for topic in topics:
            w["topics"] += '<span class="topic">{}</span>&nbsp;&nbsp;'.format(topic)
            w["tags"] += "{} ".format(topic)

    # releases
    url = response["releases_url"]
    r = requests.get(url[:-5], headers=HEADERS)
    data = r.json()
    w["release"] = "No release available"
    w["releases"] = len(data)
    if len(data) > 0:
        date = datetime.datetime.strptime(data[0]["published_at"], "%Y-%m-%dT%H:%M:%SZ")
        release_date = date.strftime("%d %b %Y")
        w[
            "release"
        ] = '<a href="{}" target="_blank">{}</a> <span class="release-date">({})</span>'.format(
            data[0]["html_url"], data[0]["name"], release_date
        )

    # contributors
    r = requests.get(response["contributors_url"], headers=HEADERS)
    data = r.json()
    w["contributors"] = len(data)
    w["contributors_list"] = ""
    for c in data:
        w[
            "contributors_list"
        ] += '<a href="{}" target="_blank"><img src="{}" width="32" height="32"/></a>&nbsp;&nbsp;'.format(
            c["html_url"], c["avatar_url"]
        )

    return w


def get_metadata(w, branch):
    # try:
    r = requests.get(
        "https://raw.githubusercontent.com/{}/{}/{}/.pegasushub.yml".format(
            w["organization"], w["repo_name"], branch
        )
    )
    w["pegasus_version"] = "No version information available"
    w["dependencies"] = "No dependencies information available"
    r.raise_for_status()
    if r.ok:
        data = yaml.safe_load(r.text)

        try:
            w["pegasus_version"] = ">= " + data["pegasus"]["version"]["min"]
            if (
                data["pegasus"]["version"]["min"] == None
                and data["pegasus"]["version"]["max"]
            ):
                w["pegasus_version"] = "<= " + data["pegasus"]["version"]["max"]
            elif (
                data["pegasus"]["version"]["min"] != data["pegasus"]["version"]["max"]
                and data["pegasus"]["version"]["max"]
            ):
                w["pegasus_version"] = (
                    "["
                    + data["pegasus"]["version"]["min"]
                    + ", "
                    + data["pegasus"]["version"]["max"]
                    + "]"
                )
        except:
            pass

        try:
            w["dependencies"] = ""
            for dep in data["dependencies"]:
                if w["dependencies"]:
                    w["dependencies"] += ", "
                w["dependencies"] += dep
        except:
            w["dependencies"] = "No dependencies information available"

    # metadata information
    if "training" not in w:
        w["training"] = "False"
    if "highlight" not in w:
        w["highlight"] = "False"
    if "priority" not in w:
        w["priority"] = 0
    if "execution_sites" not in w:
        w["execution_sites"] = []

    return w

    # except Exception as e:
    #     print(e)
    #     logger.error(e)
    #     return w


def write_to_file(w):
    with open("scripts/workflow.html.in") as f:
        template = Template(f.read())
        contents = template.substitute(w)

        # write workflows data
        with open(
            "_workflows/{}-{}.html".format(w["organization"], w["repo_name"]), "w"
        ) as f:
            f.write(contents)


def initiliaze_logger():
    if not os.path.exists("./_workflows"):
        os.makedirs("./_workflows")
    if not os.path.exists("./logs"):
        os.makedirs("./logs")
    if not os.path.exists("./logs/logs.txt"):
        with open("logs/logs.txt", "w") as f:
            f.write("")
    logging.basicConfig(
        filename="logs/logs.txt",
        format="%(asctime)s %(levelname)s %(message)s",
        level=logging.DEBUG,
    )
    return logging.getLogger(__name__)


if __name__ == "__main__":
    logger = initiliaze_logger()

    workflows = []
    # read list of workflow repositories
    with open("_data/workflows.yml") as f:
        workflows = yaml.safe_load(f)

    if validate_yaml(workflows):
        sys.exit()

    for w in workflows:
        try:
            url = "https://api.github.com/repos/{}/{}".format(
                w["organization"], w["repo_name"]
            )
            r = requests.get(url, headers=HEADERS)
            r.raise_for_status()
            logger.info("Looking up repository %s", url)
            if r.status_code == 404:
                # repo has been deleted / not found / is private
                dt = datetime.datetime.now()
                curr_time = dt.strftime("%d/%m/%Y %H:%M:%S")
                logger.warning(
                    f"{w['repo_name']} has been deleted or made private from {w['organization']}"
                )
                continue

            response = r.json()
            w = get_repo_info(w, response)
            w = get_metadata(w, response["default_branch"])
            write_to_file(w)
        except Exception as e:
            print(e)
            logger.error(e)
