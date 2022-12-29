import json
import validators
import requests
import tabulate
from bs4 import BeautifulSoup as bs4
import sys
import re
from difflib import *


table_dict =list()


def print_table(data,conf_name):
    print("="*30)
    print(conf_name)
    print("="*30+"\n")
    header = data[0].keys()
    rows =  [x.values() for x in data]
    print(tabulate.tabulate(rows, header))


def most_common_str(names):
    substring_counts={}

    for i in range(0, len(names)):
        for j in range(i+1,len(names)):
            string1 = names[i]
            string2 = names[j]
            match = SequenceMatcher(None, string1, string2).find_longest_match(0, len(string1), 0, len(string2))
            matching_substring=string1[match.a:match.a+match.size]
            if(matching_substring not in substring_counts):
                substring_counts[matching_substring]=1
            else:
                substring_counts[matching_substring]+=1
    # print(substring_counts)
    sorted_dict = sorted(substring_counts.items(), key=lambda x:x[1],reverse=True)
    conf_name = list(dict(sorted_dict).keys())[0]
    return conf_name

def main (url):
    global table_dict
    valid=validators.url(url)
    # print(valid)
    if valid==True and 'hotcrp.com' in url:
        print("\n URL is valid")
        domain=url.split(".")[0].replace("https://","")
        # print(domain)
        for ele in domain:
            if ele.isdigit():
                domain = domain.replace(ele, "")
        # print(domain)
        final_url = f"https://{domain}.hotcrp.com"
        resp = requests.get(final_url)
        # print(resp.text)
        soup = bs4(resp.text, "html.parser")
        list_links = [link for link in soup.find_all('a') if final_url not in link['href'] and link['href']!="https://hotcrp.com/"]
        links = set(list_links)
        # print(links)
        unique_links = set()
        conf_names =[]
        # print(links)
        for link in links:
            if link['href'] not in unique_links and 'hotcrp.com' not in link.text:
                print(link.text)
                res = requests.get(link['href'])
                soup = bs4(res.text, "html.parser")
                result = soup.find('div', {'class': 'homegrp'}).find('ul').find_all("li")
                all_matches = [item.text.lower() for item in result if "papers accepted" in item.text.lower()]
                if len(all_matches)!=0:
                    numbers = [int(num) for num in re.findall(r"\d+", all_matches[0])]
                    # print(numbers)
                    year = [int(num) for num in re.findall(r"\d+", link.text)][0]
                    if len(str(year))==2: year+=2000
                    conf_name= link.text.replace(str(year),"").strip()
                    conf_name="".join(list([val for val in conf_name if val.isalpha() or val.isnumeric()]))
                    table_dict.append({"Conference/Workshop":conf_name,"Year":year,"Accepted":numbers[0],"Submissions":numbers[1],"Acceptance Rate":str(round(numbers[0]/numbers[1]*100,2))+" %","Link":link["href"]})
                    conf_names.append(conf_name)
                # print(all_matches)
                unique_links.add(link['href'])
        print("\n")
        conf_name = most_common_str(conf_names)
        table_dict= sorted(table_dict, key= lambda x: (x["Year"]))
        print_table(table_dict,conf_name)
    else:
        print("Invalid URL")




main(sys.argv[1])