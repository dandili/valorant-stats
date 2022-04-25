import json

import bs4
import pandas as pd
import requests
import csv


def append_dict_as_row(file_name, dict_of_elem, field_names):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        dict_writer = DictWriter(write_obj, fieldnames=field_names)
        # Add dictionary as wor in the csv
        dict_writer.writerow(dict_of_elem)


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}

region = {
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

stats_head = {"player",
              "org",
              "agent",
              "average_combat_score",
              "kill_deaths",
              "kast",
              "average_damage_per_round",
              "kills_per_round",
              "assists_per_round",
              "first_kills_per_round",
              "first_deaths_per_round",
              "headshot_percentage",
              "clutch_success_percentage"}


def vlr_stats(agent):
    url = f"https://www.vlr.gg/stats/?event_group_id=all&event_id=all&region=all&country=all&min_rounds=200" \
          f"&min_rating=1400&agent={agent}&map_id=all&timespan=all"
    html = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(html.content, "lxml")

    tbody = soup.find("tbody")
    containers = tbody.find_all("tr")

    result = {}

    for container in containers:
        # name of player
        player_container = container.find("td", {"class": "mod-player mod-a"})
        player = player_container.a.div.text.replace("\n", " ").strip()
        player = player.split(" ")[0]

        # org name for player
        org_container = container.find("td", {"class": "mod-player mod-a"})
        org = org_container.a.div.text.replace("\n", " ").strip()
        org = org.split(" ")[-1]

        # stats for player
        stats_container = container.findAll("td", {"class": "mod-color-sq"})
        acs = stats_container[0].div.text.strip()
        kd = stats_container[1].div.text.strip()
        kast = stats_container[2].div.text.strip()
        adr = stats_container[3].div.text.strip()
        kpr = stats_container[4].div.text.strip()
        apr = stats_container[5].div.text.strip()
        fkpr = stats_container[6].div.text.strip()
        fdpr = stats_container[7].div.text.strip()
        hs = stats_container[8].div.text.strip()
        cl = stats_container[9].div.text.strip()

        player_stats = [player, org, agent, acs, kd, kast, adr, kpr, apr, fkpr, fdpr, hs, cl]

        result.update(
            {
                "player": player,
                "org": org,
                "agent": agent,
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
        df = pd.DataFrame.from_dict(result)
        df.to_csv(r'allstats.csv', index=False, header=True)


print(vlr_stats("all"))
