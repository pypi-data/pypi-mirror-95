import collections
import re
import unidecode

Page = collections.namedtuple("Page", ["name", "path", "url"])
ROOT_NAME = "Accueil"

class Nav:
    def __init__(self, name, index=False, children=None):
        self.name = name
        self.index = index
        self.children = children or []

    def page(self, path):
        res = unidecode.unidecode(str(self.name))
        res = re.sub(r"[^\sa-zA-Z0-9]", "", res).lower().strip()
        res = re.sub(r"\s+", "-", res)
        if res == ROOT_NAME.lower():
            res = path
        else:
            res = path + "/" + res
        if not self.children:
            url = res + ".html"
        elif self.index:
            url = res + "/index.html"
        else:
            url = None
        return Page(self.name, res, url)

    def walk(self, path=None, top=None, ante=None, post=None):
        page = self.page(path or "")
        if not self.children or self.index:
            yield (page.path, {"self": page, "top": top, "prev": ante, "next": post})
        if self.index:
            top = page
        for i, child in enumerate(self.children):
            if i > 0:
                ante = self.children[i - 1].page(page.path)
            else:
                ante = None
            if i < len(self.children) - 1:
                post = self.children[i + 1].page(page.path)
            else:
                post = None
            yield from child.walk(path=page.path, top=top, ante=ante, post=post)


STRUCTURE = Nav(
    ROOT_NAME,
    index=True,
    children=[
        Nav(
            "Acte 1",
            index=True,
            children=[
                Nav("Introduction"),
                Nav("Aventure 1"),
                Nav("Aventure 2"),
                Nav("Aventure 3"),
                Nav("Aventure 4"),
                Nav("Aventure 5"),
                Nav("Conclusion"),
            ],
        ),
        Nav(
            "Acte 2",
            index=True,
            children=[
                Nav("Introduction"),
                Nav("Aventure 1"),
                Nav("Aventure 2"),
                Nav("Aventure 3"),
                Nav("Aventure 4"),
                Nav("Aventure 5"),
                Nav("Conclusion"),
            ],
        ),
        Nav(
            "Acte 3",
            index=True,
            children=[
                Nav("Introduction"),
                Nav("Aventure 1"),
                Nav("Aventure 2"),
                Nav("Aventure 3"),
                Nav("Aventure 4"),
                Nav("Aventure 5"),
                Nav("Conclusion"),
            ],
        ),
        Nav(
            "Ressources",
            index=True,
            children=[
				Nav("Background"),
                Nav(
                    "PNJs",
                    index=False,
                    children=[
                        Nav("Rondo Darsa"),
                        Nav("Alexasse Dubrien"),
                    ],
                ),
                Nav(
                    "Artefacts",
                    index=False,
                    children=[
                        Nav("Bracelet des Tempêtes"),
                    ],
                ),
                Nav(
                    "Lore",
                    index=False,
                    children=[
                        Nav("Pièces noires"),
                    ],
                ),
				Nav(
                    "Théorie",
                    index=False,
                    children=[
                        Nav("Donjon en 5 salles"),
                    ],
                ),
            ],
        ),
    ],
)


HELPER = dict(STRUCTURE.walk())
