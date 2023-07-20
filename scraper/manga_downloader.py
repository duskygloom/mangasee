import scraper.helper as helper
import scraper.info as info

# provided manga name, return list of chapters
def get_chapters(indexname: str):
    mangapage = info.homepage_url + "/manga/" + indexname
    mainfunction = helper.get_script(mangapage, "function MainFunction")
    chapters = helper.get_list_json(mainfunction, "vm.Chapters")
    return chapters
