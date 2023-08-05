from json import loads
from random import randint
from os.path import dirname, abspath

from safeIO import TextFile
from requests import get, post

from translatepy.models.languages import Language
from translatepy.models.userAgents import USER_AGENTS

FILE_LOCATION = dirname(abspath(__file__))

HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "https://translate.yandex.com/",
    "User-Agent": "Mozilla: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.3 Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/43.4"
}

TRANSLIT_LANGS = ['am', 'bn', 'el', 'gu', 'he', 'hi', 'hy', 'ja', 'ka', 'kn', 'ko', 'ml', 'mr', 'ne', 'pa', 'si', 'ta', 'te', 'th', 'yi', 'zh']

class YandexTranslate():
    """
    A Python implementation of Yandex Translation's APIs
    """
    def __init__(self, sid_refresh=False) -> None:
        self._base_url = "https://translate.yandex.net/api/v1/tr.json/"
        self._sid_cache = TextFile(FILE_LOCATION + "/_yandex_sid.translatepy")
        self._sid = self._sid_cache.read()
        self._headers = self._header()
        if sid_refresh:
            self.refreshSID()
        
    def refreshSID(self):
        data = get("https://translate.yandex.com/", headers=self._headers).text
        sid_position = data.find("Ya.reqid = '")
        if sid_position == -1:
            return
        data = data[sid_position + 12:]
        self._sid = data[:data.find("';")]
        self._sid_cache.write(self._sid)

    def _header(self):
        """
        Creates a new header
        """
        _dict = HEADERS
        randomChoice = randint(0, 7499)
        _dict.update({"User-Agent": USER_AGENTS[randomChoice]})
        return _dict

    def translate(self, text, destination_language, source_language="auto"):
        """
        Translates the given text to the given language
        """
        try:
            if source_language is None or str(source_language) == "auto":
                source_language = self.language(text)
                if source_language is None:
                    return None, None
            if isinstance(source_language, Language):
                source_language = source_language.yandex_translate
            if self._sid.replace(" ", "") == "":
                self.refreshSID()
            url = self._base_url + "translate?id=" + self._sid + "-0-0&srv=tr-text&lang=" + str(source_language) +"-" + str(destination_language)  + "&reason=auto&format=text"
            request = get(url, headers=self._headers, data={'text': str(text), 'options': '4'})
            data = loads(request.text)
            if request.status_code < 400 and data["code"] == 200:
                data = loads(request.text)
                return str(data["lang"]).split("-")[0], data["text"][0]
            else:
                self.refreshSID()
                # redo everything with the new sid
                url = self._base_url + "translate?id=" + self._sid + "-0-0&srv=tr-text&lang=" + str(source_language) +"-" + str(destination_language)  + "&reason=auto&format=text"
                request = get(url, headers=self._headers, data={'text': str(text), 'options': '4'})
                data = loads(request.text)
                if request.status_code < 400 and data["code"] == 200:
                    data = loads(request.text)
                    return str(data["lang"]).split("-")[0], data["text"][0]
                else:
                    return None, None
        except:
            return None, None

    def transliterate(self, text, source_language=None):
        """
        Transliterates the given text
        """
        try:
            if source_language is None:
                source_language = self.language(text)
                if source_language is None or source_language not in TRANSLIT_LANGS:
                    return None, None
            if self._sid.replace(" ", "") == "":
                self.refreshSID()
            request = post("https://translate.yandex.net/translit/translit?sid=" + self._sid + "&srv=tr-text", headers=self._headers, data={'text': str(text), 'lang': source_language})
            if request.status_code < 400:
                return source_language, request.text[1:-1]
            else:
                self.refreshSID()
                request = post("https://translate.yandex.net/translit/translit?sid=" + self._sid + "&srv=tr-text", headers=self._headers, data={'text': str(text), 'lang': source_language})
                if request.status_code < 400:
                    return source_language, request.text[1:-1]
                else:
                    return None, None
        except:
            return None, None

    def spellcheck(self, text, source_language=None):
        """
        Spell checks the given text
        """
        try:
            if source_language is None:
                source_language = self.language(text)
                if source_language is None:
                    return None
            if self._sid.replace(" ", "") == "":
                self.refreshSID()
            request = post("https://speller.yandex.net/services/spellservice.json/checkText?sid=" + self._sid + "&srv=tr-text", headers=self._headers, data={'text': str(text), 'lang': source_language, 'options': 516})
            if request.status_code < 400:
                data = loads(request.text)
                for correction in data:
                    text = text[:correction.get("pos", 0)] + correction.get("s", [""])[0] + text[correction.get("pos", 0) + correction.get("len", 0):]
                return source_language, text
            else:
                self.refreshSID()
                request = post("https://speller.yandex.net/services/spellservice.json/checkText?sid=" + self._sid + "&srv=tr-text", headers=self._headers, data={'text': str(text), 'lang': source_language, 'options': 516})
                if request.status_code < 400:
                    data = loads(request.text)
                    for correction in data:
                        text = text[:correction.get("pos", 0)] + correction.get("s", [""])[0] + text[correction.get("pos", 0) + correction.get("len", 0):]
                    return source_language, text
                else:
                    return None, None
        except:
            return None, None

    def language(self, text, hint=None):
        """
        Gives back the language of the given text
        """
        try:
            if hint is None:
                hint = "en,ja"
            if self._sid.replace(" ", "") == "":
                self.refreshSID()
            url = self._base_url + "detect?sid=" + self._sid + "&srv=tr-text&text=" + str(text) + "&options=1&hint=" + str(hint)
            request = get(url, headers=self._headers)
            if request.status_code < 400 and request.json()["code"] == 200:
                return loads(request.text)["lang"]
            else:
                self.refreshSID()
                url = self._base_url + "detect?sid=" + self._sid + "&srv=tr-text&text=" + str(text) + "&options=1&hint=" + str(hint)
                request = get(url, headers=self._headers)
                if request.status_code < 400 and request.json()["code"] == 200:
                    return loads(request.text)["lang"]
                else:
                    return None
        except:
            return None

    def __repr__(self) -> str:
        return "Yandex Translate"