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
- url_tpl
    request url, replace pagniation number as {page}

- keyword
    the keyword in the link content

- page_number
    how many pages should be request once