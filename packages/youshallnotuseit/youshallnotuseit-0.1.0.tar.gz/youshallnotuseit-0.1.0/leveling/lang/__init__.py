from .zh_cn import TEXT


__all__ = [
    "lang",
    "useLang"
]

lang = TEXT


def useLang(new_lang: dict[str, str]) -> None:
    global lang
    lang = new_lang
