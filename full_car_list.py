from bs4 import BeautifulSoup
import requests
import re
import csv
from unidecode import unidecode


# Finding car names
with open("car_names.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["car_name"])

    # Iterating through each page
    for page_number in range(1, 7):
        base_url = "https://www.igcd.net/"
        url = f"https://www.igcd.net/game.php?id=1000012694&resultsStyle=jouable&page={page_number}"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")
        results = doc.find_all(class_="card card-custom2")

        # Iterating through each car
        for result in results:

            # Checking if it's a real car or not
            i = result.find("i").string
            if i != None:
                i = i.strip()
                i = re.sub(r"^\d+\s*", "", i)
                car_name = i
            else:
                b = result.find("b").string.strip()
                b = re.sub(r"^\d+\s*", "", b)
                car_name = b

            # Checking if teh car is a special edition and adding that annotation
            extra_info_url = base_url + result.find("a")["href"]
            extra_info_page = requests.get(extra_info_url).text
            extra_info_doc = BeautifulSoup(extra_info_page, "html.parser")

            extra_check = str(extra_info_doc.find("u").string)
            if extra_check == "Extra info:":
                extra_info = str(extra_info_doc.find(style="width: 60%;")).split(">")[5][:-4]
                car_name = car_name + extra_info

            # Printing and saving car names
            print(car_name)
            car_name = unidecode(car_name.lower())
            writer.writerow([car_name])