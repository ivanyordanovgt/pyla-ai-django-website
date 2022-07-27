from django.shortcuts import render
from django.views import generic as views
from math import ceil
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import random
from functools import partial

from pyla.betscrapper import models as bet_models
from pyla.betscrapper.filters import MatchesFilter


class GetData:

    def __init__(self, url=None):
        self.matches_list = None
        self.count = 0
        self.col = 0
        self.first_time = False
        self.headers = {}
        self.url = ''
        self.BOOKMAKERS_LIST = []
        self.SPORTS = []

        self.html = ''
        self.soup = ''
        """response = requests.get(url, headers=headers)"""

        self.strips = []

    def get_data(self):
        self.count = 0
        self.col = 0
        self.first_time = False
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 '
                          'Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}
        # link = "https://en.surebet.com/surebets?utf8=&selector%5Border%5D=start_at_asc&selector%5Boutcomes%5D%5B%5D=&selector%5Boutcomes%5D%5B%5D=2&selector%5Bmin_profit%5D=&selector%5Bmax_profit%5D=&selector%5Bmin_roi%5D=&selector%5Bmax_roi%5D=&selector%5Bsettled_in%5D=0&selector%5Bbookies_settings%5D=4%3A67%3A%3A%3B4%3A71%3A%3A%3B4%3A66%3A%3A%3B4%3A74%3A%3A%3B4%3A73%3A%3A%3B4%3A146%3A%3A%3B4%3A70%3A%3A%3B4%3A112%3A%3A%3B4%3A130%3A%3A%3B4%3A124%3A%3A%3B4%3A21%3A%3A%3B4%3A26%3A%3A%3B4%3A137%3A%3A%3B4%3A148%3A%3A%3B4%3A149%3A%3A%3B4%3A23%3A%3A%3B4%3A0%3A%3A%3B4%3A32%3A%3A%3B4%3A159%3A%3A%3B4%3A102%3A%3A%3B4%3A29%3A%3A%3B4%3A10%3A%3A%3B4%3A45%3A%3A%3B4%3A14%3A%3A%3B4%3A11%3A%3A%3B4%3A38%3A%3A%3B4%3A55%3A%3A%3B4%3A33%3A%3A%3B4%3A173%3A%3A%3B4%3A123%3A%3A%3B4%3A49%3A%3A%3B4%3A62%3A%3A%3B4%3A12%3A%3A%3B4%3A46%3A%3A%3B4%3A144%3A%3A%3B4%3A115%3A%3A%3B4%3A133%3A%3A%3B4%3A24%3A%3A%3B4%3A85%3A%3A%3B4%3A72%3A%3A%3B4%3A127%3A%3A%3B4%3A143%3A%3A%3B4%3A134%3A%3A%3B4%3A106%3A%3A%3B4%3A5%3A%3A%3B4%3A6%3A%3A%3B4%3A172%3A%3A%3B4%3A4%3A%3A%3B4%3A30%3A%3A%3B4%3A15%3A%3A%3B4%3A126%3A%3A%3B4%3A50%3A%3A%3B4%3A9%3A%3A%3B4%3A41%3A%3A%3B4%3A128%3A%3A%3B4%3A131%3A%3A%3B4%3A3%3A%3A%3B4%3A8%3A%3A%3B4%3A116%3A%3A%3B4%3A86%3A%3A%3B4%3A163%3A%3A%3B4%3A122%3A%3A%3B4%3A164%3A%3A%3B4%3A160%3A%3A%3B4%3A162%3A%3A%3B4%3A39%3A%3A%3B4%3A171%3A%3A%3B4%3A31%3A%3A%3B4%3A51%3A%3A%3B4%3A2%3A%3A%3B4%3A152%3A%3A%3B4%3A157%3A%3A%3B4%3A141%3A%3A%3B4%3A7%3A%3A%3B4%3A108%3A%3A%3B4%3A142%3A%3A%3B4%3A121%3A%3A%3B4%3A25%3A%3A%3B4%3A69%3A%3A%3B4%3A138%3A%3A%3B4%3A117%3A%3A%3B4%3A161%3A%3A%3B4%3A170%3A%3A%3B4%3A43%3A%3A%3B4%3A18%3A%3A%3B4%3A158%3A%3A%3B4%3A59%3A%3A%3B4%3A83%3A%3A%3B4%3A118%3A%3A%3B4%3A147%3A%3A%3B4%3A125%3A%3A%3B4%3A89%3A%3A%3B4%3A17%3A%3A%3B4%3A107%3A%3A%3B4%3A53%3A%3A%3B4%3A153%3A%3A%3B4%3A28%3A%3A%3B4%3A44%3A%3A%3B4%3A27%3A%3A&selector%5Bexclude_sports_ids_str%5D=56+57+0+43+32+3+55+28+8+44+9+26+34+10+11+12+39+47+46+48+49+59+53+54+58+30+13+52+29+45+19+36+33+31+40+42+41+20+50+51+21+37+23+35+38&selector%5Bextra_filters%5D=&commit=Filter&narrow="

        original_link = "https://en.surebet.com/surebets?utf8=%E2%9C%93&selector%5Border%5D=start_at_asc&selector%5Boutcomes%5D%5B%5D=&selector%5Boutcomes%5D%5B%5D=2&selector%5Bmin_profit%5D=&selector%5Bmax_profit%5D=&selector%5Bmin_roi%5D=&selector%5Bmax_roi%5D=&selector%5Bsettled_in%5D=0&selector%5Bbookies_settings%5D=0%3A67%3A%3A%3B0%3A71%3A%3A%3B0%3A66%3A%3A%3B0%3A74%3A%3A%3B0%3A73%3A%3A%3B0%3A146%3A%3A%3B0%3A70%3A%3A%3B0%3A112%3A%3A%3B0%3A130%3A%3A%3B0%3A124%3A%3A%3B0%3A21%3A%3A%3B4%3A26%3A%3A%3B0%3A137%3A%3A%3B0%3A148%3A%3A%3B0%3A149%3A%3A%3B0%3A23%3A%3A%3B0%3A0%3A%3A%3B0%3A32%3A%3A%3B0%3A159%3A%3A%3B0%3A102%3A%3A%3B0%3A29%3A%3A%3B0%3A10%3A%3A%3B4%3A45%3A%3A%3B0%3A14%3A%3A%3B0%3A11%3A%3A%3B0%3A38%3A%3A%3B0%3A55%3A%3A%3B0%3A33%3A%3A%3B0%3A123%3A%3A%3B0%3A49%3A%3A%3B0%3A62%3A%3A%3B4%3A12%3A%3A%3B0%3A46%3A%3A%3B0%3A144%3A%3A%3B0%3A115%3A%3A%3B0%3A133%3A%3A%3B0%3A24%3A%3A%3B0%3A85%3A%3A%3B0%3A72%3A%3A%3B4%3A127%3A%3A%3B0%3A143%3A%3A%3B0%3A134%3A%3A%3B0%3A106%3A%3A%3B0%3A5%3A%3A%3B0%3A6%3A%3A%3B0%3A172%3A%3A%3B0%3A4%3A%3A%3B0%3A30%3A%3A%3B0%3A15%3A%3A%3B0%3A126%3A%3A%3B4%3A50%3A%3A%3B0%3A9%3A%3A%3B0%3A41%3A%3A%3B0%3A128%3A%3A%3B0%3A131%3A%3A%3B0%3A3%3A%3A%3B0%3A8%3A%3A%3B0%3A116%3A%3A%3B0%3A86%3A%3A%3B0%3A163%3A%3A%3B0%3A122%3A%3A%3B0%3A164%3A%3A%3B0%3A160%3A%3A%3B0%3A162%3A%3A%3B0%3A39%3A%3A%3B0%3A171%3A%3A%3B0%3A31%3A%3A%3B0%3A51%3A%3A%3B0%3A2%3A%3A%3B0%3A152%3A%3A%3B0%3A157%3A%3A%3B0%3A141%3A%3A%3B12%3A7%3A%3A%3B0%3A108%3A%3A%3B0%3A142%3A%3A%3B0%3A121%3A%3A%3B0%3A25%3A%3A%3B0%3A69%3A%3A%3B0%3A138%3A%3A%3B0%3A117%3A%3A%3B0%3A161%3A%3A%3B0%3A170%3A%3A%3B0%3A43%3A%3A%3B0%3A18%3A%3A%3B0%3A158%3A%3A%3B0%3A59%3A%3A%3B0%3A83%3A%3A%3B0%3A118%3A%3A%3B0%3A147%3A%3A%3B0%3A125%3A%3A%3B0%3A89%3A%3A%3B0%3A17%3A%3A%3B0%3A107%3A%3A%3B0%3A53%3A%3A%3B0%3A153%3A%3A%3B4%3A28%3A%3A%3B0%3A44%3A%3A%3B0%3A27%3A%3A&selector%5Bexclude_sports_ids_str%5D=56+57+0+43+32+3+55+28+8+44+9+26+34+10+11+12+39+47+46+48+49+59+53+54+58+30+13+52+29+45+19+36+33+31+40+42+41+20+50+51+21+37+23+35+38&selector%5Bextra_filters%5D=&commit=Filter&narrow="
        if not self.url:
            self.url = "https://en.surebet.com/surebets?utf8=&selector%5Border%5D=start_at_asc&selector%5Boutcomes%5D%5B%5D=&selector%5Boutcomes%5D%5B%5D=2&selector%5Bmin_profit%5D=&selector%5Bmax_profit%5D=&selector%5Bmin_roi%5D=&selector%5Bmax_roi%5D=&selector%5Bsettled_in%5D=0&selector%5Bbookies_settings%5D=0%3A67%3A%3A%3B0%3A71%3A%3A%3B0%3A66%3A%3A%3B0%3A74%3A%3A%3B0%3A73%3A%3A%3B0%3A146%3A%3A%3B0%3A70%3A%3A%3B0%3A112%3A%3A%3B0%3A130%3A%3A%3B0%3A124%3A%3A%3B0%3A21%3A%3A%3B0%3A23%3A%3A%3B4%3A26%3A%3A%3B0%3A137%3A%3A%3B0%3A148%3A%3A%3B0%3A149%3A%3A%3B0%3A123%3A%3A%3B0%3A%3A%3A%3B0%3A32%3A%3A%3B0%3A159%3A%3A%3B0%3A102%3A%3A%3B0%3A29%3A%3A%3B0%3A10%3A%3A%3B4%3A45%3A%3A%3B0%3A14%3A%3A%3B0%3A11%3A%3A%3B0%3A38%3A%3A%3B0%3A55%3A%3A%3B0%3A33%3A%3A%3B4%3A173%3A%3A%3B0%3A49%3A%3A%3B0%3A62%3A%3A%3B4%3A12%3A%3A%3B0%3A46%3A%3A%3B0%3A144%3A%3A%3B0%3A115%3A%3A%3B0%3A133%3A%3A%3B0%3A24%3A%3A%3B0%3A85%3A%3A%3B0%3A72%3A%3A%3B4%3A127%3A%3A%3B0%3A143%3A%3A%3B0%3A134%3A%3A%3B0%3A106%3A%3A%3B0%3A5%3A%3A%3B0%3A6%3A%3A%3B0%3A172%3A%3A%3B0%3A4%3A%3A%3B0%3A30%3A%3A%3B0%3A15%3A%3A%3B0%3A126%3A%3A%3B4%3A50%3A%3A%3B0%3A9%3A%3A%3B0%3A41%3A%3A%3B0%3A128%3A%3A%3B0%3A131%3A%3A%3B4%3A3%3A%3A%3B0%3A8%3A%3A%3B0%3A116%3A%3A%3B0%3A86%3A%3A%3B0%3A163%3A%3A%3B0%3A122%3A%3A%3B0%3A164%3A%3A%3B0%3A160%3A%3A%3B0%3A162%3A%3A%3B0%3A39%3A%3A%3B0%3A171%3A%3A%3B0%3A31%3A%3A%3B0%3A51%3A%3A%3B0%3A2%3A%3A%3B0%3A152%3A%3A%3B0%3A157%3A%3A%3B0%3A141%3A%3A%3B12%3A7%3A%3A%3B0%3A108%3A%3A%3B0%3A142%3A%3A%3B0%3A121%3A%3A%3B0%3A25%3A%3A%3B0%3A69%3A%3A%3B0%3A138%3A%3A%3B0%3A117%3A%3A%3B0%3A161%3A%3A%3B0%3A170%3A%3A%3B0%3A43%3A%3A%3B0%3A18%3A%3A%3B0%3A158%3A%3A%3B0%3A59%3A%3A%3B0%3A83%3A%3A%3B0%3A118%3A%3A%3B0%3A147%3A%3A%3B0%3A125%3A%3A%3B0%3A89%3A%3A%3B0%3A17%3A%3A%3B0%3A107%3A%3A%3B0%3A53%3A%3A%3B0%3A153%3A%3A%3B4%3A28%3A%3A%3B0%3A44%3A%3A%3B0%3A27%3A%3A&selector%5Bexclude_sports_ids_str%5D=56+57+0+43+32+3+55+28+8+44+9+26+34+10+11+12+39+47+46+48+49+59+53+54+58+30+13+52+29+45+19+36+33+31+40+42+41+20+50+51+21+37+23+35+38&selector%5Bextra_filters%5D=&narrow="
        # marathon bet i 1xbet
        self.url = Request(
            f"{self.url}",
            headers=self.headers)

        self.BOOKMAKERS_LIST = ['Bwin', 'Bet365', 'Ladbrokes', 'William Hill', 'Bet​fair SB', 'Ef​bet',
                                r'Bet\u200bfair SB', 'Lad​brokes', 'Wil​liam Hill', 'Bet365', r'Mara\u200bthon',
                                r'Tempo​bet']
        self.SPORTS = ['Basketball', 'Hockey', 'Football', 'Volleyball', 'Handball', 'Tennis', ]

        self.html = urlopen(self.url).read()
        self.soup = BeautifulSoup(self.html)
        """response = requests.get(url, headers=headers)"""

        self.strips = list(self.soup.stripped_strings)
        print(self.strips)
        for _ in self.strips:
            print(f"Data --> {_}")

        self.matches_list = []


class MatchFrame(GetData):
    ROW_MAX_ITEMS = 6
    MATCHES_PER_PAGE = 12

    def __init__(self):
        super().__init__()
        self.frames_dict = {}
        self.matches_dict = {}
        self.matches_pages = {}

        self.pykeys_list = []

        self.time_options_list = ["Last 6 hours", "Last 12 hours", "Last day", "Option 4"]

    def show_data(self):
        print("Ok")
        for i in self.matches_list:
            print(self.matches_list)

    def __remove_useless_data(self):
        while True:

            pop = self.strips.pop(0)
            print(f"POP--> {pop}")
            if pop == 'Odds':
                break

        while True:
            pop = self.strips.pop(-1)
            print(f"BACK POP --> {pop}")
            if pop == 'Testimonials':
                break

    @staticmethod
    def __check_pinnacle(value):
        if value == 'Pin​nacle':
            return True

    def get_text_data(self):

        match_details = []

        self.__remove_useless_data()

        pass_check = False
        count = 0
        for detail in self.strips:
            if pass_check:

                if detail in self.BOOKMAKERS_LIST:
                    pass_check = False
                else:
                    continue

            if detail in self.BOOKMAKERS_LIST:
                print("///////////////////////////////////////////")
                pykey = random.randint(1, 100000)
                data = self.__list_to_text(match_details, pykey)
                match_details.clear()

                self.count += 1

            if self.__check_pinnacle(detail):
                pass_check = True
                continue

            # if '%' in set(detail):
            #     continue
            match_details.append(f'{detail}')

    def __list_to_text(self, value, pykey):
        if True:
            count = 0
            liga_found = False
            bookmaker = 'None'
            sport = 'None'
            date = 'None'
            time = None
            match_one = None
            match_two = None
            disable_match = True
            bet_type = None
            odds = None
            liga = None
        for item in value:

            print(f"ITEM --> {item}")

            if "%" in item:
                print(f"FOUND PROFIT --> {item}")
            if item in self.BOOKMAKERS_LIST:
                bookmaker = item
            if item in self.SPORTS:
                sport = item
            if len(item.split("/")) == 2:
                try:
                    date = re.search('[0-9]{1,2}/[0-9]{2}', str(item)).group(0)
                except AttributeError:
                    pass
            elif len(item.split(":")) == 2:
                try:
                    time = re.search('[0-9]{1,2}:[0-9]{2}', str(item)).group(0)
                except AttributeError:
                    pass
            elif time and disable_match:
                item_matches = item.split('–')
                if len(item_matches) == 2:
                    match_one = item_matches[0]
                    match_two = item_matches[1]
                disable_match = False

            elif not disable_match and not liga_found:
                liga = item
                liga_found = True

            if item.split()[0] in ['Under', 'Over']:
                bet_type = item.split('-')
                bet_type = bet_type[0]
            if re.search('H[0-9]\(\s*\+?(-?\d+)\s*\)', str(item)):
                bet_type = item
            else:
                if item[0] == 'H':
                    if item[1].isnumeric():
                        bet_type = item
                elif re.search('X[0-9]', str(item)):
                    bet_type = item

                else:
                    if item in ['1', '2']:
                        bet_type = item
            bet_item = item.strip()
            bet_item = bet_item.split("/")

            if len(item.split("/")) > 1:
                if item.split("/")[1].strip() in ['DNB']:
                    bet_type = item

            if len(item.split(".")) == 2:
                try:
                    odds = re.search("[0-9]{1,2}.[0-9]{2}", str(item)).group(0)
                except AttributeError:
                    for _ in item.split("."):
                        if _ == '%':
                            profit = item
                            print(f"PROFIT --> {profit}")

        if not bookmaker and not sport:
            return None

        bookmaker = bookmaker
        data = {'bookmaker': bookmaker,
                'sport': sport,
                'date': date,
                'time': time,
                'match_one': match_one,
                'match_two': match_two,
                'bet_type': bet_type,
                'odds': odds,
                'liga': liga}
        if not None in data.values():
            bet_models.BetMatch.objects.create(**data)
        return data


class BetsView(views.ListView):
    template_name = 'betscrapper/bets-list.html'
    model = bet_models.BetMatch

    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BetsView, self).get_context_data()
        context['filter'] = MatchesFilter(self.request.GET, queryset=self.get_queryset())
        return context


class RefreshDataView(views.TemplateView):
    template_name = 'betscrapper/data-refreshed.html'

    def get_context_data(self, **kwargs):
        bet_models.BetMatch.objects.all().delete()
        app = MatchFrame()
        app.get_data()
        app.get_text_data()

        super(RefreshDataView, self).get_context_data(**kwargs)


class MatchDetailView(views.DetailView):
    model = bet_models.BetMatch
    template_name = 'betscrapper/match-detail.html'
