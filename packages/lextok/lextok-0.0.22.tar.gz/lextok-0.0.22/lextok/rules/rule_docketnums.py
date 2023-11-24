from enum import Enum

from lextok.rules._pattern import Label, Rule, Style


class DocketNum(Enum):
    GR = Style(let="gr")
    AM = Style(
        let="am",
        v=[
            "adm mat",
            "adm. mat",
            "adm mat.",
            "adm. mat.",
            "adm matter",
            "adm. matter",
            "admin. matter",
            "admin matter",
            "administrative matter",
        ],
    )
    AC = Style(
        let="ac",
        v=[
            "adm case",
            "adm. case",
            "admin. case",
            "admin case",
            "administrative case",
        ],
    )
    BM = Style(let="bm", v=["bar mat.", "bar matter"])


docket_nums = Rule(
    label=Label.DocketNum, patterns=[p for mem in DocketNum for p in mem.value.patterns]
)
