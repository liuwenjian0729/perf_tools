# sys_tools

## perf_tools

### bcc_parser
convert trace file collect by bcc profile to svg

#### how to use
```bash
# clone this repo
git clone git@github.com:liuwenjian0729/sys_tools.git
cd sys_tools/perf_tools

# clone FlameGraph repo
git clone https://github.com/brendangregg/FlameGraph.git

# use
python bcc_parser.py --dir <log_dir>
```

## mem_tools

### mem_sentry
capture pid's memory usage while system memory usage above given threshold

#### how to use
```bash
python mem_sentry.py -out_path <log_to_save> &
```
