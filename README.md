# webspider

## Required 
```
> sudo apt-get install python3 python3-pip
> sudo pip3 install Scrapy
```

## Example
```
> cd webspider
> scrapy crawl links -L WARNING \
  -a url_tpl=http://bbs.cnhubei.com/forum-3-{page}.html \
  -a keyword=wuhan
```

## Parameters
- **url_tpl**:
    request url and replace the pagniation number as *{page}*.
    
    For eaxmple: 
    - page 1: http://bbs.cnhubei.com/forum-1.html
    - page 2: http://bbs.cnhubei.com/forum-2.html
    - page 3: http://bbs.cnhubei.com/forum-3.html
    - url_tpl: http://bbs.cnhubei.com/forum-{page}.html

- **keyword**:
    the keyword in the link content

- **page_number**:
    how many pages should be request once
