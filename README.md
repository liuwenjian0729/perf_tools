# perf_tools

## bcc_parser
convert trace file collect by bcc profile to svg

### how to use
```bash
# clone this repo
git clone git@github.com:liuwenjian0729/perf_tools.git
cd perf_tools

# clone FlameGraph repo
git clone https://github.com/brendangregg/FlameGraph.git

# use
python bcc_parser.py --dir <log_dir>
```
