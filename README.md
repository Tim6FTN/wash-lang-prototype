
# Web automation DSL 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![GitHub release](https://img.shields.io/github/v/release/Tim6FTN/wash-lang-prototype?include_prereleases)](https://gitHub.com/Tim6FTN/wash-lang-prototype/releases/) [![Visitors Count](https://visitor-badge.glitch.me/badge?page_id=Tim6FTN.wash-lang-prototype)](https://github.com/Tim6FTN/wash-lang-prototype)

## Introduction

WASH (Web Automation and Scraping Helper) is a domain-specific language (DSL) for web automation.

This project was created and developed during the Domain-Specific Languages course as part of the master degree program at the Faculty of Technical Sciences, University of Novi Sad.

## Description

WASH aims to make data extraction from web pages and web automation easier by enabling declarative scraping of data from web pages and simulating real-user interactions.

WASH is a:
- **High-level language** - it abstracts away all technical details and complexity of underlying technologies and libraries, thus reducing boilerplate code.
- **Declarative language** - it enables you to focus on what you want to achieve instead of describing how you want to achieve it.
- **Interpreted language** - it saves you from the hassle with re-compiling, re-configuring and re-deploying - you only need to update the scripts and you're ready to go.

The language can be used in different usage areas, various domains or for differrent purposes - by QA specialists for test automation, data scientists or machine learning researchers for creating various datasets, or anyone else in search of a tool to automate some boring, every day stuff.

## Features
- Support for both static and dynamic web pages
- Loading pages from
    - URL
    - HTML string
    - File
- Retrieving elements through queries by using
    - CSS selectors
    - XPath selectors
    - Element ID
    - Element tag name
    - Element name
    - Class name
    - Element indexes
- Extracting data through getters by using
    - Attribute getters
    - Text getters
    - Inner HTML getters
    - Outer HTML getters
- Page interactions
    - Data input 
    - Mouse events *(Click, Scroll, Point, Hover)*
    - Timed operations with timeout *(Wait, Navigate)*
    - DOM manipulation through JavaScript code execution
- Comments

## Example

**Input HTML**

```html
<html lang="en">
    <head>
        <style>
            .description {
                color: #ffffff;
                background-color: #4caf50;
                border-color: #4caf50
            }
            .hidden {
                display: none;
            }
        </style>
        <title>WASH Example</title>
    </head>
    <body class="front-page">
        <div class="content">
            <div id="top-ten-table" class="styled-table">
                <div class="table-entry">
                    <a class="title" href="https://www.google.com/">First item title</a>
                    <span class="source-link">
                        <a href="#">Link</a>
                    </span>
                    <span class="item-rank">1</span>
                    <div class="score hidden">100</div>
                    <p class="info">
                        <time datetime="Fri Jan 01 09:15:42 2021 UTC">01.01.2021.</time>
                        <span class="description" data-somecustomattr="custom attribute value 1">First item description</span>
                    </p>
                </div>
                <div class="table-entry">
                    <a class="title" href="https://www.google.com/">Second item title</a>
                    <span class="source-link">
                        <a href="#">Link</a>
                    </span>
                    <span class="item-rank">2</span>
                    <div class="score hidden">42</div>
                    <p class="info">
                        <time datetime="Sat Jan 16 17:31:33 2021 UTC">16.01.2021.</time>
                        <span class="description" data-somecustomattr="custom attribute value 2">Second item description</span>
                    </p>
                </div>
            </div>
        </div>
    </body>
</html>
```

**Input script**

```cpp

** A simple example script with an example comment
** that beautifully spans over multiple lines :)

import "custom_chrome_configuration.wash"
import "custom_firefox_configuration.wash"

use configuration custom_chrome_configuration

open "https://fivkovic.github.io/chisel-prototype/"          ** A partially commented line

?c #top-ten-table .table-entry {
    ?c a.title : text -> title
    ?c .source-link a {
        : text -> link_text
        : @href -> link_url
    } -> link
    ?c .item-rank : text -> rank
    ?c .score.hidden : inner_html -> page_rank_score
    ?c .info {
        ?c time {
            : @datetime -> exact_time
            : text -> short_date
            : html -> inner_html
        } -> publishing_date
        ?x ./*[contains(@class, 'description')] {
            : @data-somecustomattr -> custom_attribute
            : text -> description_text
        } -> description
    } -> info
} -> top_ten
```

**Extracted data**

```json
{
   "top_ten": [{
            "title": "First item title",
            "link": {
                "link_text": "Link",
                "link_url": "https://fivkovic.github.io/chisel-prototype/#"
            },
            "rank": "1",
            "page_rank_score": "100",
            "info": {
                "publishing_date": {
                    "exact_time": "Fri Jan 01 09:15:42 2021 UTC",
                    "short_date": "01.01.2021.",
                    "inner_html": "<time datetime='Fri Jan 01 09:15:42 2021 UTC'>01.01.2021.</time>"
                },
                "description": {
                    "custom_attribute": "custom attribute value 1",
                    "description_text": "First item description"
                }
            }
        }, {
            "title": "Second item title",
            "link": {
                "link_text": "Link",
                "link_url": "https://fivkovic.github.io/chisel-prototype/#"
            },
            "rank": "2",
            "page_rank_score": "42",
            "info": {
                "publishing_date": {
                    "exact_time": "Sat Jan 16 17:31:33 2021 UTC",
                    "short_date": "16.01.2021.",
                    "inner_html": "<time datetime='Sat Jan 16 17:31:33 2021 UTC'>16.01.2021.</time>"
                },
                "description": {
                    "custom_attribute": "custom attribute value 2",
                    "description_text": "Second item description"
                }
            }
        }]
}
```

## Dev Environment setup

The following instructions will get you a copy of the project up 
and running on your local machine for development and testing purposes.

### Prerequisites

- [Python >= 3.9](https://www.python.org/downloads/)

### Instructions
  1. Install Python 3.9
  2. Create a virtual environment (e.g. venv) and run `pip install requirements.txt`
  3. To install in development mode, run `python setup.py develop`. 
  4. To uninstall, run `python setup.py develop --uninstall`.

## Usage & Instructions

*TBA Soon*

## Technology stack

*TBA Soon*

## Contributors

- [R2 7/2020 Milan Milovanović](https://github.com/m-milovanovic)
- [R2 8/2020 Marko Stanić](https://github.com/Marko131)
- [R2 9/2020 Mihailo Đokić](https://github.com/mdjokic)
- [R2 23/2020 Katarina Tukelić](https://github.com/ktukelic)
- [R2 25/2020 Filip Ivković](https://github.com/fivkovic)

## License
WASH is a free and open-source project licensed under the MIT License.

## Credits

Initial project layout generated with `textx startproject`.