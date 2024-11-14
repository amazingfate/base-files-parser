#!/usr/bin/python3
import requests
from lxml import etree
import json

def get_basefiles_info_from_upstream(debian_url):
    # Step 1: Fetch HTML content from the URL
    response = requests.get(debian_url)
    html_content = response.content  # Use .content for lxml to handle byte data

    # Step 2: Parse HTML with lxml
    parser = etree.HTMLParser()
    tree = etree.fromstring(html_content, parser)

    # Step 3: Extract data
    for h3 in tree.xpath('//h3'):
        section_title = h3.text

        ul = h3.xpath('./following-sibling::ul[1]')
        debian_all_basefiles_info = {}
        if ul:
            list_items = ul[0].xpath('.//li')
            for li in list_items:
                debian_basefiles_info = {}
                item_text = li.xpath('.//text()[not(parent::a)]')
                item_class = li.get("class")
                base_file_release = item_class
                base_file_version = item_text[1].split(":")[0]
                if "arm64" in item_text[1].split(":")[1]:
                    base_file_arm64_full_name = "/pool/main/b/base-files/base-files_" + base_file_version + "_arm64.deb"
                    debian_basefiles_info["arm64"] = base_file_arm64_full_name
                if "armhf" in item_text[1].split(":")[1]:
                    base_file_armhf_full_name = "/pool/main/b/base-files/base-files_" + base_file_version + "_armhf.deb"
                    debian_basefiles_info["armhf"] = base_file_armhf_full_name
                if "amd64" in item_text[1].split(":")[1]:
                    base_file_amd64_full_name = "/pool/main/b/base-files/base-files_" + base_file_version + "_amd64.deb"
                    debian_basefiles_info["amd64"] = base_file_amd64_full_name
                if "riscv64" in item_text[1].split(":")[1]:
                    base_file_riscv64_full_name = "/pool/main/b/base-files/base-files_" + base_file_version + "_riscv64.deb"
                    debian_basefiles_info["riscv64"] = base_file_riscv64_full_name
                debian_all_basefiles_info[item_class] = debian_basefiles_info
        return debian_all_basefiles_info

debian_url = "https://packages.debian.org/search?keywords=base-file&searchon=names&suite=all&section=all"
debian_info = get_basefiles_info_from_upstream(debian_url)
ubuntu_url = "https://packages.ubuntu.com/search?keywords=base-file&searchon=names&suite=all&section=all"
ubuntu_info = get_basefiles_info_from_upstream(ubuntu_url)
if debian_url and debian_url:
    all_info_result = {**debian_info, **ubuntu_info}
    with open("result.json", "w") as outfile:
        json.dump(all_info_result, outfile)
else:
    print("failed")
