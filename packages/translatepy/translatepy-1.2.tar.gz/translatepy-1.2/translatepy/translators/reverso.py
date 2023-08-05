from json import loads
from translatepy.models.languages import Language
from requests import post

HEADERS = {
    "Host": "api.reverso.net",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Referer": "https://www.reverso.net/translationresults.aspx?lang=EN",
    "Content-Type": "application/json",
    "Connection": "keep-alive"
}

class ReversoTranslate():
    """
    A Python implementation of Reverso's API
    """
    def __init__(self) -> None:
        pass

    def translate(self, text, destination_language, source_language=None):
        """
        Translates the given text to the given language
        """
        try:
            if source_language is None or str(source_language) == "auto":
                source_language = self.language(text)
                if source_language is None:
                    return None, None
            if isinstance(source_language, Language):
                source_language = source_language.reverso_translate
            if isinstance(destination_language, Language):
                destination_language = destination_language.reverso_translate
            source_language = str(source_language)
            destination_language = str(destination_language)
            request = post("https://api.reverso.net/translate/v1/translation", headers=HEADERS, json={
                "input": str(text),
                "from": source_language,
                "to": destination_language,
                "format": "text",
                "options": {
                    "origin": "reversodesktop",
                    "sentenceSplitter": False,
                    "contextResults": False,
                    "languageDetection": True
                }
            })
            if request.status_code < 400:
                data = loads(request.text)
                return data["languageDetection"]["detectedLanguage"], data["translation"][0]
            else:
                return None, None
        except:
            return None, None


    def spellcheck(self, text, source_language=None):
        """
        Checks the spelling of the given text
        """
        try:
            if source_language is None:
                source_language = self.language(text)
                if source_language is None:
                    return None
            request = post("https://api.reverso.net/translate/v1/translation", headers=HEADERS, json={
                "input": str(text),
                "from": str(source_language),
                "to": "eng",
                "format": "text",
                "options": {
                    "origin": "reversodesktop",
                    "sentenceSplitter": False,
                    "contextResults": False,
                    "languageDetection": False
                }
            })
            if request.status_code < 400:
                result = loads(request.text)["correctedText"]
                if result is None:
                    return text
                return result
            else:
                return None
        except:
            return None

    def language(self, text):
        """
        Gives back the language of the given text
        """
        try:
            request = post("https://api.reverso.net/translate/v1/translation", headers=HEADERS, json={
                "input": str(text),
                "from": "eng",
                "to": "fra",
                "format": "text",
                "options": {
                    "origin": "reversodesktop",
                    "sentenceSplitter": False,
                    "contextResults": False,
                    "languageDetection": True
                }
            })
            if request.status_code < 400:
                return loads(request.text)["languageDetection"]["detectedLanguage"]
            else:
                return None
        except:
            return None

    def __repr__(self) -> str:
        return "Reverso"