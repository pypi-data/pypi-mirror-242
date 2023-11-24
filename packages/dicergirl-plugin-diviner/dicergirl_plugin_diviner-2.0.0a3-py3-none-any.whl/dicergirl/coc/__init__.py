from .investigator import Investigator
from .nbhandlers import commands
from .coccards import coc_cards, coc_cache_cards, coc_attrs_dict
from .cocutils import coc_at, coc_dam, coc_ra, coc_en, init

init()
coc_cards.load()

__version__ = "1.2.2"

__type__ = "plugin"
__charactor__ = Investigator
__name__ = "coc"
__cname__ = "调查员"
__cards__ = coc_cards
__cache__ = coc_cache_cards
__nbhandler__ = nbhandlers
__nbcommands__ = commands
__commands__ = {
    "at": coc_at,
    "dam": coc_dam,
    "ra": coc_ra,
    "en": coc_en
}
__baseattrs__ = coc_attrs_dict
__description__ = "COC 模式是以H.P.洛夫克拉夫特《克苏鲁的呼唤(Call of Cthulhu)》为背景的 TRPG 跑团模式."