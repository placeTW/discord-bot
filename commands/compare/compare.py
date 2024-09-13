# import discord
# from discord import app_commands
# from bot import TWPlaceClient
from bs4 import BeautifulSoup
import sys
import os
from modules.async_utils import _async_get_html
import asyncio

SUMMARIES_OF_INTEREST_LIST = set([
    "Cost of Living in",
    "Groceries Prices in",
    "Restaurants Prices in"
])

COSTS_OF_INTEREST_LIST = set([
    "Coke/Pepsi",
    "Milk",
    "Rice",
    "Apples",
    "Onion"
    "Potato",
])

def _extract_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    return soup

def _htmlsoup_is_valid(soup: BeautifulSoup) -> bool:
    # checks to see if <div style="error_message"> is present
    search = soup.find("div", style="error_message")
    return search is None

def _startswith_in_set(text: str, list_of_interest: set[str]) -> bool:
    for item in list_of_interest:
        if text.startswith(item):
            return True
    return False

def _extract_summary_table(soup: BeautifulSoup):
    # get table with class table_indices_diff 
    table_indices_diff = soup.find("table", class_="table_indices_diff")
    # get all td in the table
    tds = table_indices_diff.find_all("td")
    # collect all relevant lines
    summaries_to_return = []
    for td in tds:
        text = td.text
        if text and _startswith_in_set(text, SUMMARIES_OF_INTEREST_LIST):
            summaries_to_return.append(text)
    # postprocessing
    summaries_to_return = [f"* {summary}" for summary in summaries_to_return]
    summary = "\n".join(summaries_to_return)
    return summary

def _extract_cost_comparision_table(soup):
    # get table with class cost_comparison_table 
    table = soup.find("table", class_="cost_comparison_table")
    # get all its trs
    costs_to_return = []
    trs = table.find_all("tr")
    for tr in trs:
        # get all tds in the tr
        if tds := tr.find_all("td"):
            num_tds = len(tds)
            # get the first td
            if (td := tds[0]) and (num_tds > 3): # probably an awful way to write this
                item_name = td.text
                if _startswith_in_set(item_name, COSTS_OF_INTEREST_LIST):
                    costs_to_return.append([
                        item_name,
                        tds[1].get_text(strip=True).replace("\xa0", " "),
                        tds[2].get_text(strip=True).replace("\xa0", " "),
                    ])
    # postprocessing goes here

    return costs_to_return
        

if __name__ == "__main__":
    url = "https://www.numbeo.com/cost-of-living/compare_cities.jsp?country1=Taiwan&country2=Taiwan&city1=Taipei&city2=Kaohsiung"
    # url = "https://www.numbeo.com/cost-of-living/compare_cities.jsp?country1=Canada&city1=Ottawa&country2=Germany&city2=Basdadserlin&displayCurrency=EUR"
    html = asyncio.run(_async_get_html(url))
    soup = _extract_html(html)
    if _htmlsoup_is_valid(soup):
        summary = _extract_summary_table(soup)
        costs = _extract_cost_comparision_table(soup)
        print(summary)
        print(costs)
    else:
        print("Error: invalid html")
        sys.exit(1)