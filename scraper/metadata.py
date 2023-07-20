import os

def set_metadata(indexname: str, cover: str, manganame: str, mangaurl: str):
    fpath = f"cache/{indexname}/metadata.txt"
    if not os.path.isdir(os.path.dirname(fpath)):
        os.mkdir(os.path.dirname(fpath))
    with open(fpath, "w") as f:
        f.writelines([
            cover + "\n",
            manganame + "\n",
            mangaurl + "\n",
        ])

def get_metadata(fpath: str) -> tuple:
    if not os.path.isfile(fpath):
        return "", "", ""
    with open(fpath) as f:
        cover = f.readline().rstrip("\n")
        manganame = f.readline().rstrip("\n")
        mangaurl = f.readline().rstrip("\n")
    return cover, manganame, mangaurl
