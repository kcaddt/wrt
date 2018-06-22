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

    if not os.path.exists( os.path.join('generated', NAME.upper()) ):
        os.mkdir(
            os.path.join('generated', NAME.upper())
        )

    os.mkdir(
        os.path.join('generated', NAME.upper(), _TS)
    )
    shutil.copyfile(
        FILE, 
        os.path.join('generated', NAME.upper(), _TS, FILE)
    )

    with open(os.path.join('generated', NAME.upper(), _TS, 'main.py'),'w') as f:
        f.write(generated_output)

    return 1

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Launch wrt')
    parser.add_argument('instruction',  type=str)     

    parser.add_argument('-n', '--name', help = "name of the project", type=str)
    parser.add_argument('-m', '--methods', default=None, type=str)           
    parser.add_argument('--host', default="0.0.0.0", type=str)
    parser.add_argument('--port', default="8888", type=int) 

    args = parser.parse_args()

    if args.instruction not in ['create', 'ls']:
        parser.error("%s : unknown instruction" % args.instruction)
    
    if args.instruction == "create":
        if (args.name is None) or (args.methods is None):
            parser.error("create requires a name and a methods file")
        if not os.path.isfile(args.methods):
            parser.error("%s : can not open methods file" % args.methods)

        generate(args.name, args.methods , args.host, args.port)

    # Add timestamp creation, number of version, number of route of last version 
    if args.instruction == "ls":
        projects = [e for e in os.listdir('generated') if e[0] != '.']
        neg = 's' if len(projects) > 1 else ''

        print("{0} project{1} found : \n".format(len(projects), neg))
        for el in projects:
            print("    - " + el)

