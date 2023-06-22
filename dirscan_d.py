import requests
import time
import os
import random
import argparse #argparse 用于解析命令行参数
from fake_useragent import UserAgent #fake_useragent 用于生成随机的User-Agent
#by bingtanghulu

results = []
def banner():
    print('\033[1.34m####################################################\033[0m\n'
          '\033[1.34m###################目录扫描脚本#####################\033[0m\n'
          '\033[1.34m####################################################\033[0m\n'
          )

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers",
    "Upgrade-Insecure-Requests": "1"
}
#生成随机的User-Agent
def get_random_user_agent():
    user_agent = UserAgent()
    random_user_agent = user_agent.random
    return random_user_agent
#生成随机的X-Forwarded-For头部信息
def get_random_xff():
    ip_segments = [str(random.randint(0, 255)) for _ in range(4)]
    xff = '.'.join(ip_segments)
    return xff

def Req(url, proxy=None):
    try:
        headers["User-Agent"] = get_random_user_agent()
        headers["X-Forwarded-For"] = get_random_xff()
        session = requests.Session()

        if proxy:
            session.proxies = {"http": proxy, "https": proxy}

        response = session.get(url, headers=headers)
        status = response.status_code
        content_size = len(response.content)
        results.append({"url": url, "status": status, "size": content_size})
        print_result(results[-1])
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
#用于打印单个扫描结果的信息
def print_result(result):
    url = result["url"]
    status = result["status"]
    size = result["size"]
    print(f"{url} {status} 内容大小：{size} 字节")
#用于扫描单个URL
def scan_single_url(url, dictionary_file, proxy=None):
    if dictionary_file is None:
        dictionary_file = "dic/dir.txt"
    dictionary_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), dictionary_file)

    with open(dictionary_file, "r") as file:
        dictionary = [line.strip() for line in file]

    for word in dictionary:
        new_url = url + word
        Req(new_url, proxy)

def scan_url_file(url_file, dictionary_file, max_urls_per_10s, proxy=None):
    if dictionary_file is None:
        dictionary_file = "dic/dir.txt"
    dictionary_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), dictionary_file)

    with open(url_file, "r") as file:
        urls = [line.strip() for line in file]

    with open(dictionary_file, "r") as file:
        dictionary = [line.strip() for line in file]

    for url in urls:
        count = 0
        for word in dictionary:
            new_url = url + word
            Req(new_url, proxy)
            count += 1
            if count >= max_urls_per_10s:
                time.sleep(10)

def save_results(results, url, dictionary_file, totaltime):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    #创建一个目录用于存储结果文件，并根据URL生成结果文件的名称
    output_dir = os.path.join(script_dir, "result")
    os.makedirs(output_dir, exist_ok=True)

    file_name = url.replace("://", "_").replace("/", "_").replace(".", "_") + "_result.txt"
    output_file = os.path.join(output_dir, file_name)

    with open(output_file, "w") as file:
        file.write(f"URL: {url}\n")
        file.write(f"Dictionary File: {dictionary_file}\n")
        file.write(f"Total Time Taken: {totaltime} seconds\n\n")

        for result in results:
            file.write(f"URL: {result['url']}\n")
            file.write(f"Status: {result['status']}\n")
            file.write(f"Content Size: {result['size']} bytes\n\n")

    print(f"\n结果已保存至 {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="扫描网站状态和内容大小")
    parser.add_argument("-u", dest="single_url", help="单个待扫描的地址")
    parser.add_argument("-f", dest="url_file", help="批量待扫描的地址文件")
    parser.add_argument("-d", dest="dictionary_file", help="批量的地址文件dictionary_file")
    parser.add_argument("-s", dest="max_urls_per_10s", type=int, default=10, help="10秒内扫描的上限")
    parser.add_argument("-p", dest="proxy", help="代理IP", default=None)
    args = parser.parse_args()
    banner()
    if args.single_url:
        scan_single_url(args.single_url, args.dictionary_file, args.proxy)
    elif args.url_file:
        scan_url_file(args.url_file, args.dictionary_file, args.max_urls_per_10s, args.proxy)

    url = args.single_url or args.url_file
    save_results(results, url, args.dictionary_file, 0)