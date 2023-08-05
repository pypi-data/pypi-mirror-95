#"""PRODUCTION
from translatepy.models.languages import Language
from translatepy.translators.google import GoogleTranslate
from translatepy.translators.bing import BingTranslate
from translatepy.translators.yandex import YandexTranslate
from translatepy.translators.reverso import ReversoTranslate
from translatepy.translators.unselected import Unselected
#"""
"""DEBUG
from models.languages import Language
from translators.google import GoogleTranslate
from translators.bing import BingTranslate
from translators.yandex import YandexTranslate
from translators.reverso import ReversoTranslate
"""

TRANSLATION_CACHES = {}
TRANSLITERATION_CACHES = {}
SPELLCHECK_CACHES = {}
LANGUAGE_CACHES = {}
EXAMPLE_CACHES = {}
AUTOMATIC = Language("auto")

class TranslationResult():
    def __init__(self, source, result, source_language, destination_language, service) -> None:
        self.source = str(source)
        self.result = str(result)
        self.source_language = source_language
        self.destination_language = destination_language
        self.service = service

    def __repr__(self) -> str:
        return "Source (" + (self.source_language.name if isinstance(self.source_language, Language) else str(self.source_language)) + "): " + self.source + "\nResult (" + (self.destination_language.name if isinstance(self.destination_language, Language) else str(self.destination_language)) + "): " + self.result

    def __str__(self) -> str:
        return self.result

    def __call__(self, *args, **kwds):
        return self.result

    def __eq__(self, o: object) -> bool:
        return str(o) == self.result

    def __ne__(self, o: object) -> bool:
        return str(o) != self.result
            

class Translator():
    """
    A class which groups all of the APIs
    """
    def __init__(self, use_google=True, use_yandex=True, use_bing=True, use_reverso=True, yandex_sid_refresh=False) -> None:
        self.google_translate = (GoogleTranslate() if use_google else Unselected())
        self.yandex_translate = (YandexTranslate(sid_refresh=yandex_sid_refresh) if use_yandex else Unselected())
        self.bing_translate = (BingTranslate() if use_bing else Unselected())
        self.reverso_translate = (ReversoTranslate() if use_reverso else Unselected())

    def translate(self, text, destination_language, source_language=None):
        global TRANSLATION_CACHES

        if str(text).replace(" ", "").replace("\n", "") == "":
            return None

        ## language handling
        if not isinstance(destination_language, Language):
            destination_language = Language(destination_language)
        if source_language is not None and not isinstance(source_language, Language):
            source_language = Language(source_language)

        ## caches handling
        _cache_key = str({"t": str(text), "d": str(destination_language), "s": str(source_language)})
        if _cache_key in TRANSLATION_CACHES:
            return TRANSLATION_CACHES[_cache_key]

        lang, response = self.google_translate.translate(text, destination_language, source_language)
        if response is None:
            lang, response = self.bing_translate.translate(text, destination_language, source_language)
            if response is None:
                lang, response = self.reverso_translate.translate(text, destination_language, source_language)
                if response is None:
                    lang, response = self.yandex_translate.translate(text, destination_language, source_language)
                    if response is None and isinstance(self.yandex_translate, Unselected):
                        return None
                    try:
                        lang = Language(lang)
                    except: pass
                    result = TranslationResult(source=text, result=response, source_language=lang, destination_language=destination_language, service=self.yandex_translate)
                    TRANSLATION_CACHES[str({"t": str(text), "d": str(destination_language), "s": str(source_language)})] = result
                    TRANSLATION_CACHES[str({"t": str(text), "d": str(destination_language), "s": str(lang)})] = result
                    return result
                else:
                    try:
                        lang = Language(lang)
                    except: pass
                    result = TranslationResult(source=text, result=response, source_language=lang, destination_language=destination_language, service=self.reverso_translate)
                    TRANSLATION_CACHES[str({"t": str(text), "d": str(destination_language), "s": str(source_language)})] = result
                    TRANSLATION_CACHES[str({"t": str(text), "d": str(destination_language), "s": str(lang)})] = result
                    return result
            else:
                try:
                    lang = Language(lang)
                except: pass
                result = TranslationResult(source=text, result=response, source_language=lang, destination_language=destination_language, service=self.bing_translate)
                TRANSLATION_CACHES[str({"t": str(text), "d": str(destination_language), "s": str(source_language)})] = result
                TRANSLATION_CACHES[str({"t": str(text), "d": str(destination_language), "s": str(lang)})] = result
                return result
        else:
            try:
                lang = Language(lang)
            except: pass
            result = TranslationResult(source=text, result=response, source_language=lang, destination_language=destination_language, service=self.google_translate)
            TRANSLATION_CACHES[str({"t": str(text), "d": str(destination_language), "s": str(source_language)})] = result
            TRANSLATION_CACHES[str({"t": str(text), "d": str(destination_language), "s": str(lang)})] = result
            return result

    def transliterate(self, text, source_language=None):
        global TRANSLITERATION_CACHES
        if source_language is not None and not isinstance(source_language, Language):
            source_language = Language(source_language)

        _cache_key = str({"t": str(text), "s": str(source_language)})
        if _cache_key in TRANSLITERATION_CACHES:
            return TRANSLITERATION_CACHES[_cache_key]

        lang, response = self.yandex_translate.transliterate(text, source_language)
        
        if response is None and isinstance(self.yandex_translate, Unselected):
            return None

        try:
            lang = Language(lang)
        except: pass

        TRANSLITERATION_CACHES[str({"t": str(text), "s": str(source_language)})] = response
        TRANSLITERATION_CACHES[str({"t": str(text), "s": str(lang)})] = response
        return response

    def spellcheck(self, text, source_language=None):
        global SPELLCHECK_CACHES

        _cache_key = str({"t": str(text), "s": str(source_language)})
        if _cache_key in SPELLCHECK_CACHES:
            return SPELLCHECK_CACHES[_cache_key]

        if source_language is not None and not isinstance(source_language, Language):
            source_language = Language(source_language)


        lang, response = self.bing_translate.spellcheck(text, source_language)
        if response is None:
            lang, response = self.reverso_translate.spellcheck(text, source_language)
            if response is None:
                lang, response = self.yandex_translate.spellcheck(text, source_language)
                try:
                    lang = Language(lang)
                except: pass
                if response is None and isinstance(self.yandex_translate, Unselected):
                    return None

                SPELLCHECK_CACHES[str({"t": str(text), "s": str(source_language)})] = response
                SPELLCHECK_CACHES[str({"t": str(text), "s": str(lang)})] = response
                return response
            else:
                try:
                    lang = Language(lang)
                except: pass

                SPELLCHECK_CACHES[str({"t": str(text), "s": str(source_language)})] = response
                SPELLCHECK_CACHES[str({"t": str(text), "s": str(lang)})] = response
                return response
        else:
            try:
                lang = Language(lang)
            except: pass

            SPELLCHECK_CACHES[str({"t": str(text), "s": str(source_language)})] = response
            SPELLCHECK_CACHES[str({"t": str(text), "s": str(lang)})] = response
            return response

    def language(self, text):
        global LANGUAGE_CACHES
        text = str(text)
        
        if text in LANGUAGE_CACHES:
            return LANGUAGE_CACHES[text]

        response = self.google_translate.language(text)
        if response is None:
            response = self.bing_translate.language(text)
            if response is None:
                response = self.reverso_translate.language(text)
                if response is None:
                    response = self.yandex_translate.language(text)
                    if response is None and isinstance(self.yandex_translate, Unselected):
                        return None
                    else:
                        try:
                            response = Language(response)
                        except: pass

                        LANGUAGE_CACHES[text] = response
                        return response
                else:
                    try:
                        response = Language(response)
                    except: pass

                    LANGUAGE_CACHES[text] = response
                    return response
            else:
                try:
                    response = Language(response)
                except: pass

                LANGUAGE_CACHES[text] = response
                return response
        else:
            try:
                response = Language(response)
            except: pass

            LANGUAGE_CACHES[text] = response
            return response

    def example(self, text, destination_language, source_language=None):
        global EXAMPLE_CACHES
        
        if not isinstance(destination_language, Language):
            destination_language = Language(destination_language)
        if source_language is not None and not isinstance(source_language, Language):
            source_language = Language(source_language)

        ## caches handling
        _cache_key = str({"t": str(text), "d": str(destination_language), "s": str(source_language)})
        if _cache_key in EXAMPLE_CACHES:
            return EXAMPLE_CACHES[_cache_key]

        lang, response = self.bing_translate.example(text, destination_language, source_language)
        if response is None and isinstance(self.bing_translate, Unselected):
            return None

        try:
            lang = Language(lang)
        except: pass
        
        EXAMPLE_CACHES[str({"t": str(text), "d": str(destination_language), "s": str(source_language)})] = response
        EXAMPLE_CACHES[str({"t": str(text), "d": str(destination_language), "s": str(lang)})] = response
        return response

#translator = Translator()