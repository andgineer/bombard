# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/andgineer/bombard/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                          |    Stmts |     Miss |   Cover |   Missing |
|------------------------------ | -------: | -------: | ------: | --------: |
| bombard/\_\_main\_\_.py       |        2 |        2 |      0% |       1-3 |
| bombard/args.py               |       32 |       19 |     41% |    26-149 |
| bombard/attr\_dict.py         |       18 |        8 |     56% |41-42, 48, 53-55, 61-63 |
| bombard/bombardier.py         |      162 |       33 |     80% |27, 30-32, 89, 109-110, 114, 128, 131, 137-139, 143-159, 171, 187-189, 205, 211, 221, 232-233, 257, 271 |
| bombard/campaign\_yaml.py     |       28 |        8 |     71% |29, 45-46, 49-53 |
| bombard/expand\_file\_name.py |       33 |        7 |     79% |19, 25, 31, 35, 44-46 |
| bombard/http\_request.py      |       18 |        3 |     83% | 32, 41-42 |
| bombard/main.py               |       94 |       20 |     79% |27-35, 44-47, 80-81, 129, 131, 145, 151, 155 |
| bombard/mock\_globals.py      |       29 |       29 |      0% |     10-58 |
| bombard/pretty\_ns.py         |       35 |       14 |     60% |45, 50-56, 61, 64-65, 68, 72, 76, 80-82 |
| bombard/pretty\_sz.py         |       10 |        1 |     90% |        18 |
| bombard/report.py             |       91 |        4 |     96% |72, 92, 145, 185 |
| bombard/request\_logging.py   |       49 |        4 |     92% |     79-82 |
| bombard/show\_descr.py        |        5 |        0 |    100% |           |
| bombard/terminal\_colours.py  |       27 |        8 |     70% |42, 46, 50, 54, 58-62 |
| bombard/version.py            |        1 |        0 |    100% |           |
| bombard/weaver\_mill.py       |       35 |        0 |    100% |           |
|                     **TOTAL** |  **669** |  **160** | **76%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/andgineer/bombard/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/andgineer/bombard/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/andgineer/bombard/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/andgineer/bombard/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fandgineer%2Fbombard%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/andgineer/bombard/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.