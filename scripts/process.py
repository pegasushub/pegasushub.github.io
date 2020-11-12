#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 The Pegasus Team.

import datetime
import os
import requests
import yaml

from string import Template


workflows = []
headers = {
    'Accept': 'application/vnd.github.mercy-preview+json'
}

# read list of workflow repositories
with open('_data/workflows.yml') as f:
    workflows = yaml.load(f, Loader=yaml.FullLoader)

for w in workflows:
    print(w)
    url = 'https://api.github.com/repos/{}/{}'.format(w['organization'], w['repo_name'])
    r = requests.get(url, headers=headers)
    response = r.json()

    #print(response)

    # repo general information
    w['title'] = response['name']
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
        data = yaml.load(r.text, Loader=yaml.FullLoader)
        print(data)
        try:
            w['pegasus_version'] = data['pegasus']['version']['min'] 
            if data['pegasus']['version']['min'] ! data['pegasus']['version']['max']:
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
            pass

    with open('scripts/workflow.html.in') as f:
        template = Template(f.read())
        contents = template.substitute(w)

        # write workflows data
        with open('_workflows/{}-{}.html'.format(w['organization'], w['repo_name']), 'w') as f:
            f.write(contents)
