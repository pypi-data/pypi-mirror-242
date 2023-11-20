# Author: William E. Palin
# Date created: 2023-01-04
# Notes: See Alabama

from juriscraper.opinions.united_states.state import ala


class Site(ala.Site):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.court_str = "1da1a297-c391-4e4f-9480-1bc68b46f21a"
