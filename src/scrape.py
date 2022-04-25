import re

import pandas as pd
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import urllib

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}

regions = {
    "na": "north-america",
    "eu": "europe",
    "ap": "asia-pacific",
    "la": "latin-america",
    "la-s": "la-s",
    "la-n": "la-n",
    "oce": "oceania",
    "kr": "korea",
    "mn": "mena",
    "gc": "game-changers",
    "br": "Brazil",
    "ch": "china",
}

agents = ["astra", "breach", "brimstone", "chamber", "cypher", "jett", "kayo", "killjoy", "neon", "omen", "phoenix",
              "raze", "reyna", "sage", "skye", "sova", "viper", "yoru"]

class Vlr:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
        }

    def get_soup(self, url):
        response = requests.get(url, headers=self.headers)
        html, status_code = response.text, response.status_code
        return BeautifulSoup(html, "lxml"), status_code

    @staticmethod
    def vlr_stats_region():
        url = f"https://www.vlr.gg/stats/?event_group_id=all&event_id=all&region=all&country=all&min_rounds=200" \
              f"&min_rating=1400&agent=all&map_id=all&timespan=30"
        html = requests.get(url, headers=headers)
        soup = BeautifulSoup(html.content, "lxml")
        status = html.status_code

        tbody = soup.find("tbody")
        containers = tbody.find_all("tr")

        result = []
        for container in containers:
            # name of player
            player_container = container.find("td", {"class": "mod-player mod-a"})
            player = player_container.a.div.text.replace("\n", " ").strip()
            player = player.split(" ")[0]

            # org name for player
            org_container = container.find("td", {"class": "mod-player mod-a"})
            org = org_container.a.div.text.replace("\n", " ").strip()
            org = org.split(" ")[-1]

            # agent name for player
            left_split = '/img/vlr/game/agents/'
            right_split = '.png'
            agents_container = container.find("td", {"class": "mod-agents"})
            agents_div = agents_container.find("div")
            agents_imgs = agents_div.findAll('img')
            imgs = ",".join(set(img['src'] for img in agents_imgs))
            agents_str = imgs.replace(left_split, "").replace(right_split, "")
            agents = agents_str
            # agents = agents_str.split(",")

            # stats for player
            player_rounds = container.find("td", {"class": "mod-rnd"})
            raw_rounds = player_rounds.renderContents()
            rounds = raw_rounds.strip().decode("utf-8")
            stats_container = container.findAll("td", {"class": "mod-color-sq"})
            acs = stats_container[0].div.text.strip()
            kd = stats_container[1].div.text.strip()
            kast = stats_container[2].div.text.replace("%", "").strip()
            adr = stats_container[3].div.text.strip()
            kpr = stats_container[4].div.text.strip()
            apr = stats_container[5].div.text.strip()
            fkpr = stats_container[6].div.text.strip()
            fdpr = stats_container[7].div.text.strip()
            hs = stats_container[8].div.text.replace("%", "").strip()
            cl = stats_container[9].div.text.replace("%", "").strip()

            result.append(
                {
                    "player": player,
                    "org": org,
                    "agents": agents,
                    "rounds": rounds,
                    "average_combat_score": acs,
                    "kill_deaths": kd,
                    "kast": kast,
                    "average_damage_per_round": adr,
                    "kills_per_round": kpr,
                    "assists_per_round": apr,
                    "first_kills_per_round": fkpr,
                    "first_deaths_per_round": fdpr,
                    "headshot_percentage": hs,
                    "clutch_success_percentage": cl,
                }
            )

        df = pd.DataFrame(result)
        filepath = Path('stats.csv')
        df.to_csv(filepath, index=False)

        if status != 200:
            raise Exception("Err" + status)
        return df


if __name__ == '__main__':
    print(Vlr.vlr_stats_region())
