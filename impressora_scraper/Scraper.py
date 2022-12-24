from bs4 import BeautifulSoup
import logging
from impressora_scraper.Requisicao_threads import Requisicao_threads
from beartype import beartype
logging.basicConfig()
logger = logging.getLogger("Scraper")
logger.setLevel(logging.DEBUG)


class Scraper():
    @beartype
    def __init__(self, url_impressora: str) -> None:
        """Gera objeto BeautifulSoup a partir do conteúdo de página

        Args:
            url_impressora (str): Conteúdo obtido da página
        """
        self._url_impressora = url_impressora
        self._lista_bandejas = []

    @beartype
    def parse_pagina(self, conteudo: str) -> BeautifulSoup:
        soup = BeautifulSoup(conteudo, 'html.parser')
        return soup

    def obter_pagina(self, url):
        pass

    class ScraperErrors():
        class ElementoAusente(Exception):
            pass

        class ModeloIncompativel(Exception):
            pass

        class FalhaRequisicao(Exception):
            pass


class ScraperLexmarkMX611dhe(Scraper):
    def __init__(self, url_impressora: str) -> None:
        super().__init__(url_impressora)


class ScraperM4206MarkII(Scraper):
    def __init__(self, url_impressora: str) -> None:
        super().__init__(url_impressora)


