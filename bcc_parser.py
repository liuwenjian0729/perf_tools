#!/usr/bin/env python

# convert bcc log to svg, need flamegraph.pl
# 1. git clone this repo
# 2. cd this repo
# 3. git clone https://github.com/brendangregg/FlameGraph.git
# 4. make sure with FLAMEGRAPH_PATH
# 5. python bcc_parser.py --dir <log_dir>

# update:
# 2021-09-20        initial release
import os
import argparse

# setup environment
CUR_PATH = os.environ.get('PATH', '')
FLAMEGRAPH_PATH = './FlameGraph'
if FLAMEGRAPH_PATH not in CUR_PATH:
    os.environ['PATH'] = FLAMEGRAPH_PATH + os.pathsep + CUR_PATH

def parse_bcc_log(file: str):
    base_path = os.path.dirname(file)
    with open(file, 'r') as f:
        contents = f.read().split('bcc_profile')
        for content in contents:
            if len(content) == 0:
                continue
            time, content = content.split('\n',1)
            time = time.split(': ')[1][:10]
            f = open('{}/{}.folded'.format(base_path, time),"a+")
            f.write(content)
            f.close()

def generate_svg_file(log_dir: str):
    svg_path = os.path.join(log_dir, 'svg')
    if not os.path.exists(svg_path):
        os.makedirs(svg_path)
    
    for file in os.listdir(log_dir):
        if not file.endswith('.folded'):
            continue
        folded_file = os.path.join(log_dir, file)
        svg_file = os.path.join(svg_path, file.split('.')[0])
        cmd = "flamegraph.pl {} > {}.svg".format(folded_file, svg_file)
        os.system(cmd)
        os.remove(folded_file)

def get_args():
    help_msg = 'split bcc log.'
    parser = argparse.ArgumentParser(prog='bcc_parser', description=help_msg)
    parser.add_argument("--dir",
        type = str,
        required = True,
        help="the dir of the bcc logs"
    )
    parser.add_argument("-t",
        type = int,
        required = False,
        default = 1,
        help="num of merged files"
    )
    return parser.parse_args()

def main(args):
    for file in os.listdir(args.dir):
        if not file.startswith('bcc_profile.log'):
            continue
        parse_bcc_log(os.path.join(args.dir, file))
    
    generate_svg_file(args.dir)

if __name__ == '__main__':
    args = get_args()
    main(args)
