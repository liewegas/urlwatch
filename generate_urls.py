#!/usr/bin/python3

import subprocess
import json
import yaml

with open('conf.yaml', 'r') as f:
    conf = yaml.load(f.read())

def foo(url, what):
    r = []
    out = subprocess.check_output(
        ['curl', url])
    j = json.loads(out)
    for s in j['states']:
        if not s['text']:
            continue
        name = s['state'] + '/' + what
        if name not in conf:
#            continue
            pass
        i = conf.get('default', {}).copy()
        i['name'] = name
        i['url'] = s['text']
        if name in conf:
            for k, v in conf[name].items():
                i[k] = v
        r.append(i)
    return r

r = foo('https://api.voteamerica.com/v1/election/field/external_tool_polling_place/',
        'pp')
r += foo('https://api.voteamerica.com/v1/election/field/external_tool_ovr/',
         'ovr')
print(yaml.dump_all(r))
