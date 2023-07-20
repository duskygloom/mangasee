import socket
import requests, bs4, os, json
import scraper.info as info

class ErrorMessage:
    @staticmethod
    def could_not_get(url: str, status_code: int):
        return f"Could not send GET request to {url} - {status_code}"
    @staticmethod
    def directory_not_found(dir: str):
        return f"Could not find the directory - {dir}"

def internet_exists() -> bool:
    # try:
    #     requests.get(info.homepage_url)
    #     return True
    # except requests.ConnectionError as e:
    #     print("Device is not connected to internet.")
    #     return False
    htmlport = 80
    try:
        socket.create_connection(("1.1.1.1", htmlport))
        return True
    except OSError as e:
        print("Device is not connected to internet.")
        return False

def download_file(url: str, savepath: str) -> str:
    '''
        downloads the file in the url and saves it in savepath
        returns the path of the downloaded file
        if not downloaded returns empty string
    '''
    if internet_exists():
        r = requests.get(url)
    else:
        return ""
    if not r.ok:
        print(ErrorMessage.could_not_get(url, r.status_code))
        return ""
    savedir = os.path.dirname(savepath)
    if not os.path.isdir(savedir):
        os.mkdir(savedir)
    with open(savepath, "wb") as f:
        f.write(r.content)
        f.flush()
        return savepath
    
def check_url(url: str) -> tuple:
    '''
        checks if the url is ok
        returns bool status, status code
    '''
    if internet_exists():
        r = requests.get(url)
    else:
        return False, 0
    return r.ok, r.status_code

def get_soup(url: str) -> bs4.BeautifulSoup | None:
    '''returns bs4 soup of the webpage'''
    if internet_exists():
        r = requests.get(url)
    else:
        return None
    if not r.ok:
        print(ErrorMessage.could_not_get(url, r.status_code))
    return bs4.BeautifulSoup(r.text, "lxml")

def get_element_from_url(url: str, tag: str, selector: dict = {}) -> bs4.Tag | None:
    '''returns element from the soup matching the tag and selectors'''
    soup = get_soup(url)
    if soup == None:
        return None
    return soup.find(tag, selector)

def get_element_from_tag(tag: bs4.Tag, subtag: str, selector: dict = {}) -> bs4.Tag | None:
    '''returns element from the soup matching the tag and selectors'''
    if tag == None:
        return None
    return tag.find(subtag, selector)

def get_elements_from_url(url: str, tag: str, selector: dict = {}) -> list:
    '''returns list of elements from the soup matching the tag and selectors'''
    if soup == None:
        return []
    soup = get_soup(url)
    return soup.find_all(tag, selector)

def get_script(url: str, query: str):
    '''
        returns script from the soup containing query
        if no such script is found, returns empty string
    '''
    scripts = get_elements_from_url(url, "script")
    content = ""
    for i in scripts:
        content = i.get_text().strip()
        if query in content:
            break
        content = ""
    return content

def get_list_json(script: str, listname: str) -> list:
    '''
        parses js script and returns the list of jsons
        returns empty list if listname not found
    '''
    start = script.find(listname)
    if start == -1:
        return []
    end = script.find("}];", start) + 3
    list_js_form = script[start:end]
    list_json_form = list_js_form.lstrip(listname + " = ")
    list_json_form = list_json_form.rstrip(";")
    return json.loads(list_json_form)
 
def get_string(script: str, stringname: str) -> list:
    '''
        parses js script and returns a string variable
        returns empty string if listname not found
    '''
    start = script.find(stringname)
    if start == -1:
        return ""
    end = script.find("\";", start) + 2
    string_js_form = script[start:end]
    string_js_form = string_js_form.lstrip(stringname + " = \"")
    string = string_js_form.rstrip("\";")
    # if string_js_form == "\"":
    #     return ""
    # string = ""
    # for i in range(len(string_js_form)):
    #     if string_js_form[i] == "\"" and string_js_form[i-1] != "\\":
    #         break
    #     string += string_js_form[i]
    return string

def get_all_manga(use_internet: bool = True):
    '''
        returns list of all manga in mangasee
        returns empty list if the list is not found
    '''
    all_manga_url = info.homepage_url + "/_search.php"
    local_json = "cache/_search.json"
    if internet_exists() and use_internet:
        r = requests.get(all_manga_url)
    elif os.path.isfile(local_json):
        with open(local_json) as f:
            return json.load(f)
    else:
        return []
    if not r.ok:
        print("Encountered problem while sending request -", all_manga_url)
        return []
    with open(local_json, "w") as f:
        f.write(r.text)
    return json.loads(r.text)

def search_manga(query: str, all_manga: list | None = None):
    if query.isspace() or query == "":
        return []
    if all_manga == None:
        all_manga = get_all_manga()
    selected_manga = []
    for i in all_manga:
        if query.lower() in i["s"].lower():
            selected_manga.append(i["i"])
            continue
        if len(i["a"]) == 0:
            continue
        for j in i["a"]:
            if query.lower() in j.lower():
                selected_manga.append(i["i"])
                continue
    return selected_manga

def get_manga_name(indexname: str):
    '''returns manga name from index name'''
    all_manga = get_all_manga(use_internet=False)
    for i in all_manga:
        if i["i"] == indexname:
            return i["s"]
    all_manga = get_all_manga(use_internet=True)
    for i in all_manga:
        if i["i"] == indexname:
            return i["s"]
    return ""
