#!/usr/bin/env python3
from DeBooxUpx import boox_strings
import re
model_width = 10

with open('README.md') as readme:
    readme_text = readme.read()
models = sorted(boox_strings.items(), key=lambda x: x[0])
table_header = f"""|{'': ^{model_width}}|{'MODEL': ^{model_width+2}}|{'STRING_SETTINGS': ^46}|{'STRING_UPGRADE': ^46}|{'STRING_LOCAL': ^42}|
|{'-'*(model_width)}|{'-'*(model_width+2)}|{'-'*46}|{'-'*46}|{'-'*42}|
"""
table = table_header + '\n'.join(
    f"|{name: ^{model_width}}|{'`'+string['MODEL']+'`': ^{model_width+2}}|`{string['STRING_SETTINGS']}`|`{string['STRING_UPGRADE']}`|`{string.get('STRING_LOCAL') or ' '*40}`|"
    for name, string in models)
with open('README.md', 'w') as readme:
    readme.write(
        re.sub(
            r'<!--\(strings table begin\)-->.*<!--\(strings table end\)-->',
            f'<!--(strings table begin)-->\n{table}\n<!--(strings table end)-->',
            readme_text,
            1,
            flags=re.S))
