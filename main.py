from pandas import read_html
from requests import get
from concurrent import futures

from sys import argv, exit
from sys import stderr

WORKERS = 10

if len(argv) > 1:
    try:
        WORKERS = int(argv[1])
        if WORKERS <= 0:
            raise Exception("workers should not be non-positive integer")
    except:
        stderr.write("first argument should be valid positive integer as number of workers!\n")
        exit(1)


def get_name_title(character):
    title = read_html(get(f"https://wiki.biligame.com/ys/{character}").text, match="称号",
                      attrs={"class": "wikitable"})[0][1][0]
    return character + "・" + title


characters = filter(lambda character_name: "旅行者" not in character_name,
                    read_html(get("https://wiki.biligame.com/ys/角色筛选").text)[1]["名称"])

pool = futures.ThreadPoolExecutor(max_workers=WORKERS)
for name in pool.map(get_name_title, characters):
    print(name)
