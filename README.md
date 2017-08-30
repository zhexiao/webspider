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