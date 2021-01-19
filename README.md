
# Web automation DSL 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 

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
    - Element indexes
- Extracting data through getters by using
    - Attribute getters
    - Text getters
    - Inner HTML getters
- Page interactions
    - Data input 
    - Mouse events *(Click, Scroll, Point, Hover)*
    - Timed operations with timeout *(Wait, Navigate)*
- Comments

## Example

**Input HTML**

```html
<html>
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
    </head>
    <body class="front-page">
        <div class="content">
            <div id="top-ten-table" class="styled-table">
                <div class="table-entry">
                    <a class="title" href="http://www.google.com/">First item title</a>
                    <span class="source-link">
                        <a href="#">Link</a>
                    </span>
                    <span class="item-rank">1</span>
                    <div class="score hidden">100</div>
                    <p class="info">
                        <time datetime="Fri Jan 01 09:15:42 2021 UTC">01.01.2021.</time>
                        <p class="description" data-somecustomattr="custom attribute value 1">First item description</p>
                    </p>
                </div>
                <div class="table-entry">
                    <a class="title" href="http://www.google.com/">Second item title</a>
                    <span class="source-link">
                        <a href="#">Link</a>
                    </span>
                    <span class="item-rank">2</span>
                    <div class="score hidden">42</div>
                    <p class="info">
                        <time datetime="Sat Jan 16 17:31:33 2021 UTC">16.01.2021.</time>
                        <p class="description" data-somecustomattr="custom attribute value 2">Second item description</p>
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

open "http://www.my-website.com/top-ten"    

?c #top-ten-table .table-entry {
    [{
        ?c a.title : text -> title
        ?c .source-link a {
            : text -> link_text
            : @href -> link_url
        } -> link
        ?c .item-rank : text -> rank
        ?c .score.hidden : text -> page_rank_score
        ?c .info {
            ?c time {
                : @datetime -> exact_time
                : text -> short_date
                : html -> inner_html
            } -> publishing_date
            ?x //*[contains(@style, 'background-color: #4caf50;')] {
                : @data-somecustomattr -> custom_attribute
                : text -> description_text
            } -> description
        }
    }] -> topten
}
```

**Extracted data**

```json
{
    "topten" : [
        {
            "title" : "First item title",
            "link" : {
                "link_text" : "Link",
                "link_url" : "#"
            },
            "rank" : "1",
            "page_rank_score" : "100",
            "publishing_date" : {
                "exact_time" : "Fri Jan 01 09:15:42 2021 UTC",
                "short_date" : "01.01.2021.",
                "inner_html" : "<time datetime='Fri Jan 01 09:15:42 2021 UTC'>01.01.2021.</time>"
            },
            "description" : {
                "custom_attribute" : "custom attribute value 1",
                "description_text" : "First item description"
            }
        },
        {
            "title" : "Second item title",
            "link" : {
                "link_text" : "Link",
                "link_url" : "#"
            },
            "rank" : "2",
            "page_rank_score" : "42",
            "publishing_date" : {
                "exact_time" : "Sat Jan 16 17:31:33 2021 UTC",
                "short_date" : "16.01.2021.",
                "inner_html" : "<time datetime='Sat Jan 16 17:31:33 2021 UTC'>16.01.2021.</time>"
            },
            "description" : {
                "custom_attribute" : "custom attribute value 2",
                "description_text" : "Second item description"
            }
        }
    ]
}
```

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




