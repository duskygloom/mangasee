import os

import scraper.info as info
import scraper.helper as helper
import scraper.metadata as metadata

def get_mangasee_icon() -> str:
    '''
        downloads mangasee icon
        returns the filepath if downloaded
        else returns empty string
    '''
    iconurl = info.homepage_url + "/media/favicon.png"
    filepath = "assets/mangasee_icon.png"
    downloaded = helper.download_file(iconurl, filepath)
    if downloaded == "" and os.path.isfile(filepath):
        return filepath
    return downloaded

def get_manga_info(indexname: str):
    '''
        downloads manga cover and metadata
        returns the save path of cover and metadata
        returns empty string if not downloaded
    '''
    coverfile = "cache/" + indexname + "/cover.jpg"
    metafile = "cache/" + indexname + "/metadata.txt"
    if helper.internet_exists():
        if not os.path.isfile(coverfile):
            rssfeed = info.homepage_url + "/rss/" + indexname + ".xml"
            imagetag = helper.get_element_from_url(rssfeed, "image")
            imageurl = helper.get_element_from_tag(imagetag, "url").text
            coverfile = helper.download_file(imageurl, coverfile)
        manganame = helper.get_manga_name(indexname)
        link = ""
        if indexname != "":
            link = info.homepage_url + "/manga/" + indexname
        if not os.path.isdir(os.path.dirname(coverfile)):
            os.mkdir(os.path.dirname(coverfile))
        metadata.set_metadata(indexname, coverfile, manganame, link)
        return metafile
    elif os.path.isfile(coverfile) and os.path.isfile(metafile):
        return metafile
    else:
        return ""
