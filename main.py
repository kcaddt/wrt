#!/usr/bin/python

import argparse
import uuid
import time 
import shutil
import os 
from jinja2 import Environment, FileSystemLoader


_TS = str(int(time.time()))
_internal = '_data' + os.sep

def generate(NAME, FILE,  HOST, PORT):
    file_name = FILE.split('.')[0]
    methods_dict = open(FILE, 'r').read()

    methods_content = [
                        'def' + e.replace('\t', '    ') 
                        for e in methods_dict.split('def')
                        if len(e) > 1
                    ]
    methods_name    = [
                        e.split(':')[0].strip().split('(')[0]
                        for e in methods_dict.replace('\n', '').split('def')
                        if len(e) > 1
                    ]

    methods = [
                {
                    'name' : methods_name[i],
                    'content' : methods_content[i]
                }

                for i in range(len(methods_name))
            ]

    env = Environment(
            loader = FileSystemLoader(searchpath = _internal)
        )

    template = env.get_template('template.py')
    generated_output = template.render(
        method_file=file_name,
        methods_list=','.join(methods_name),
        methods=methods,
        host=HOST,
        port=PORT
    )

    os.mkdir(
        os.path.join('generated', NAME.upper()  +  _TS)
    )
    shutil.copyfile(
        FILE, 
        os.path.join('generated', NAME.upper() + _TS, FILE)
    )

    with open(os.path.join('generated', NAME.upper() + _TS, 'main.py'),'w') as f:
        f.write(generated_output)

    return 1

if __name__ == '__main__':

    _NAME, _HOST, _PORT = "TEST", "0.0.0.0","8888"
    generate(_NAME, 'methods.py', _HOST, _PORT)




