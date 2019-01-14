# landsat-footprint-benchmark

Create Landsat8 footprint from data and metadata

[![CircleCI](https://circleci.com/gh/vincentsarago/landsat-footprint.svg?style=svg)](https://circleci.com/gh/vincentsarago/landsat-footprint)

[![codecov](https://codecov.io/gh/vincentsarago/landsat-footprint/branch/master/graph/badge.svg)](https://codecov.io/gh/vincentsarago/landsat-footprint)


```
$ git clone http://github.com/developmentseed/landsat-footprint-benchmark
$ cd landsat-footprint

$ pip install .

$ cd scripts
$ make test
```

![landsat_footprint](https://user-images.githubusercontent.com/10407788/51143691-1495f180-181d-11e9-82cf-e7cd89de434a.png)

# Benchmark

Overview level | 0 | 1 | 2 | 3 | 4
 --- | --- | --- | --- | --- | ---        
**HTTP call** | 243 | 34 | 6 | 5 | 5
**Bytes transfered** (Ko) | 446 030 | 95 374 | 45 430 | 35 621 | 33 925


```
./scripts/main.sh LC08_L1TP_017033_20170516_20170525_01_T1 QA 0
LC08_L1TP_017033_20170516_20170525_01_T1 | band: QA | overview: 0
Bytes transfered: 446030
GET requests:  243

./scripts/main.sh LC08_L1TP_017033_20170516_20170525_01_T1 QA 1
LC08_L1TP_017033_20170516_20170525_01_T1 | band: QA | overview: 1
Bytes transfered: 95374
GET requests:  34

./scripts/main.sh LC08_L1TP_017033_20170516_20170525_01_T1 QA 2
LC08_L1TP_017033_20170516_20170525_01_T1 | band: QA | overview: 2
Bytes transfered: 45430
GET requests:  6

./scripts/main.sh LC08_L1TP_017033_20170516_20170525_01_T1 QA 3
LC08_L1TP_017033_20170516_20170525_01_T1 | band: QA | overview: 3
Bytes transfered: 35621
GET requests:  5

./scripts/main.sh LC08_L1TP_017033_20170516_20170525_01_T1 QA 4
LC08_L1TP_017033_20170516_20170525_01_T1 | band: QA | overview: 4
Bytes transfered: 33925
GET requests:  5
```


# CLI

```
$ l8foot --help
Usage: l8foot [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  data      Create footprint from data
  metadata  Create footprint from metadata
 ```

### footprint from data

```
$ l8foot data --help
Usage: l8foot data [OPTIONS] SCENEID

  Create footprint from data

Options:
  --band TEXT               Landsat band to use (default: QA).
  --overview-level INTEGER  Overview level to use. 0: raw data, 4: highest zoom level.
  --nodata INTEGER          Nodata value (default: 1 for QA band).
  --simplify                Simplify output shape.
  --help                    Show this message and exit.
```

### footprint from metadata

```
$ l8foot metadata --help
Usage: l8foot metadata [OPTIONS] SCENEID

  Create footprint from metadata

Options:
  --help  Show this message and exit.                 Show this message and exit.
```


# Contribution & Devellopement

Issues and pull requests are more than welcome.

**Dev install & Pull-Request**

```
$ git clone https://github.com/vincentsarago/landsat-footprint.git
$ cd lambda-pyskel
$ pip install -e .[dev]
```


*>Python3.6 only*

This repo is set to use `pre-commit` to run *flake8*, *pydocstring* and *black* ("uncompromising Python code formatter") when committing new code.

```
$ pre-commit install
$ git add .
$ git commit -m'my change'
black....................................................................Passed
Flake8...................................................................Passed
Verifying PEP257 Compliance..............................................Passed
$ git push origin
```
