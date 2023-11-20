# Scraper for Kansas Appeals Court (unpublished)
# CourtID: kanctapp_u

from juriscraper.opinions.united_states.state import kan_p


class Site(kan_p.Site):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.court_id = self.__module__
        self.status = "Unpublished"
        self.court = "Court of Appeals"
