# dirscan
简单介绍：随机UA+随机XFF+IP代理+限时次 目录扫描

工具借用了以下2位师傅@M0ge和@pingc0y的产品，两位大佬🐮。

    （1）字典：https://github.com/M0ge/dirsearch_dicc

    （2）代理池：https://github.com/pingc0y/go_proxy_pool

## 脚本简单介绍：

    dirscan_d.py 随机UA+随机XFF+IP代理+限时次

    dirscan_s.py 随机UA+随机XFF+IP代理+多线程

    add_slash.sh 梳理字典，给字典文件每行内容前加/


## 具体使用：

1、根据自己的电脑自行下载https://github.com/pingc0y/go_proxy_pool 对应的版本，并启动过

    ./goProxyPool-macos-amd64
    
  <img width="556" alt="图片" src="https://github.com/bingtangbanli/dirscan/assets/77956516/0b698b99-fe9b-4faa-af0d-d45a0f7efdf9">

抓取代理

    http://127.0.0.1:8080/spider

验证代理

    http://127.0.0.1:8080/verify

等待抓代理和验证代理结束

2、配置环境

    pip install -r requirements.txt

3、指定脚本进行扫描

（1）dirscan_d.py 随机UA+随机XFF+IP代理+限时次

### 不使用代理，直接扫描

    python3 dirscan_d.py -h

<img width="510" alt="图片" src="https://github.com/bingtangbanli/dirscan/assets/77956516/b62d0989-37f1-4eaa-8545-44a4cb863492">

-s 是指10秒内工具可以扫描多少个目录，该需求只要是防止批量扫描被waf封禁，此项可以不选。默认为10秒中扫描10个目录。
-d 是指扫描的目录字典，不选，则默认为/dic/dir.txt

使用示例

    python3 dirscan_d.py -u http://172.16.70.129:80 -d dic/test.txt
    python3 dirscan_d.py -u http://172.16.70.129:80
    python3 dirscan_d.py -u http://172.16.70.129:80 -d dic/test.txt -s 50
    python3 dirscan_d.py -u http://172.16.70.129:80  -s 50
    python3 dirscan_d.py -f urllist.txt -d dic/test.txt
    python3 dirscan_d.py -f urllist.txt
    .........
    

<img width="632" alt="图片" src="https://github.com/bingtangbanli/dirscan/assets/77956516/8630fbca-470d-433a-a97e-1fd746ce38ba">

服务器后台记录为

<img width="658" alt="图片" src="https://github.com/bingtangbanli/dirscan/assets/77956516/c26e78e0-42ae-4007-92dd-0e43a2796877">

### 增加代理扫描-使用示例

使用代理扫描速度会受到go_proxy_pool工具代理的影响

    python3 dirscan_d.py -u http://172.16.70.129:80 -d dic/test.txt -p http://127.0.0.1:8111
    python3 dirscan_d.py -u http://172.16.70.129:80
    python3 dirscan_d.py -u http://172.16.70.129:80 -d dic/test.txt -s 50
    python3 dirscan_d.py -u http://172.16.70.129:80  -s 50
    python3 dirscan_d.py -f urllist.txt -d dic/test.txt
    python3 dirscan_d.py -f urllist.txt
    .........

    
