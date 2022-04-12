#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 The Pegasus Team.

import datetime
import os
import requests
import yaml

from string import Template
import logging
import logging.config
from schema import Schema, SchemaError

from jsonschema import validate, Draft7Validator
from jsonschema.exceptions import ValidationError

logging.basicConfig(filename="logs/logs.txt", format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

workflows = []
headers = {
    'Accept': 'application/vnd.github.mercy-preview+json',
    'Authorization': 'token {}'.format(os.environ['PEGASUSHUB_TOKEN'])
}
# headers = {}

config_schema = Schema({
    "organization": str,
    "repo_name": str,
    # "training": bool
})

schema = {
  "type": "array",
  "items": {
    "type" : "object",
    "properties": {
        "repo_name": { "type": "string" },
        "organization": { "type": "string" },
        "highlight": { "type": "boolean" },
        "training": { "type": "boolean" },
        "priority": {"type": "number", "minimum": 0, "maximum": 5 },
        "execution_sites": { 
            "type": "array",
            "items": {
                "type": "string",
                "enum": ["CONDORPOOL", "SLURM", "SUMMIT_GLITE", "LSF", "SUMMIT_KUBERNETES"] 
            }
        }
    },
    "additionalProperties": False,
    "required": ["repo_name", "organization"],
    # "if": {
    #     "properties": {"highlight": {"const": True}}
    # }, 
    # "then": {"required": ["priority"]}
    "anyOf": [
        {
            "not": {
                "properties": { "highlight": { "const": True }},
                "required": ["highlight"]
            }
        },
        { "required": ["priority"] }
    ]
  }
}

# read list of workflow repositories
with open('_data/workflows.yml') as f:
    workflows = yaml.safe_load(f)

if not os.path.exists('./logs'):
    os.makedirs('./logs')
if not os.path.exists('./logs/logs.txt'):
    with open("logs/logs.txt", 'w') as f:
        f.write("")


validator = Draft7Validator(schema)
errors = sorted(validator.iter_errors(workflows), key=lambda e: e.path)
for error in errors:
    # print(error.validator, error.context, "\n\n")
    if error.validator == "anyOf":
        print(error.context[-1])
    elif error.validator in ["type", "maximum", "minimum"] :
        print(error.message, " in ", error.schema_path[-2])
    else:
        print(error.message)

for w in workflows:    
    url = 'https://api.github.com/repos/{}/{}'.format(w['organization'], w['repo_name'])
    r = requests.get(url, headers=headers)
    if r.status_code == 404:
        #repo has been deleted / not found / is private
        dt = datetime.datetime.now()
        curr_time = dt.strftime("%d/%m/%Y %H:%M:%S")
        logger.warning(f"{w['repo_name']} has been deleted or made private from {w['organization']}")
        continue

    response = r.json()
    logger.info(f"{w['repo_name']} is being populated\n")
    # repo general information
    w['title'] = response['name']
    w['default_branch'] = response['default_branch']
    w['subtitle'] = response['description']
    w['license'] = response['license']['name'] if response['license'] else 'No licence available'
    w['issues'] = response['open_issues']
    w['forks'] = response['forks']
    w['stargazers'] = response['stargazers_count']

    # date
    date = datetime.datetime.strptime(response['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
    w['year'] = date.strftime('%Y')
    w['month'] = date.strftime('%b')
    w['monthn'] = date.strftime('%m')
    w['day'] = date.strftime('%d')

    # topics
    w['topics'] = 'No topics available'
    w['tags'] = ''
    topics = response['topics']
    if len(topics) > 0:
        w['topics'] = ''
        for topic in topics:
            w['topics'] += '<span class="topic">{}</span>&nbsp;&nbsp;'.format(topic);
            w['tags'] += '{} '.format(topic)

    # releases
    url = response['releases_url']
    r = requests.get(url[:-5], headers=headers)
    data = r.json()
    w['release'] = 'No release available'
    w['releases'] = len(data)
    if len(data) > 0:
        date = datetime.datetime.strptime(data[0]['published_at'], '%Y-%m-%dT%H:%M:%SZ')
        release_date = date.strftime('%d %b %Y')
        w['release'] = '<a href="{}" target="_blank">{}</a> <span class="release-date">({})</span>'.format(data[0]['html_url'], data[0]['name'], release_date)

    # contributors
    r = requests.get(response['contributors_url'], headers=headers)
    data = r.json()
    w['contributors'] = len(data)
    w['contributors_list'] = ''
    for c in data:
        w['contributors_list'] += '<a href="{}" target="_blank"><img src="{}" width="32" height="32"/></a>&nbsp;&nbsp;'.format(c['html_url'], c['avatar_url'])

    # metadata file
    r = requests.get('https://raw.githubusercontent.com/{}/{}/master/.pegasushub.yml'.format(w['organization'], w['repo_name']))
    w['pegasus_version'] = 'No version information available'
    w['dependencies'] = 'No dependencies information available'
    if r.ok:
        data = yaml.safe_load(r.text)
        try:
            w['pegasus_version'] = data['pegasus']['version']['min'] 
            if data['pegasus']['version']['min'] != data['pegasus']['version']['max']:
                w['pegasus_version'] = '[{}, {}]'.format(data['pegasus']['version']['min'], data['pegasus']['version']['max'])
        except:
            pass

        try:
            w['dependencies'] = ''
            for dep in data['dependencies']:
                if w['dependencies']:
                    w['dependencies'] += ', '
                w['dependencies'] += dep
        except:
            w['dependencies'] = 'No dependencies information available'

    # metadata information
    if 'training' not in w:
        w['training'] = 'False'
    if 'highlight' not in w:
        w['highlight'] = 'False'
    if 'priority' not in w:
        w['priority'] = 0
    if 'execution_sites' not in w:
        w['execution_sites'] = []

    with open('scripts/workflow.html.in') as f:
        template = Template(f.read())
        contents = template.substitute(w)

        # write workflows data
        with open('_workflows/{}-{}.html'.format(w['organization'], w['repo_name']), 'w') as f:
            f.write(contents)
