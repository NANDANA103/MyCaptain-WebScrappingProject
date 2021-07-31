import requests
from bs4 import BeautifulSoup
import pandas
import connect


oyo_url = "https://www.oyorooms.com/hotels-in-bangalore/?page="
page_num_MAX = 5
scrapped_info_list = []

connect.connect("OYO_HOTELS")

for page_num in range(1, page_num_MAX + 1):
    url = oyo_url + str(page_num)
    print("GET Request for: " + url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    req = requests.get(url, headers=headers)
    content = req.content.decode()
    soup = BeautifulSoup(content, "html.parser")
    all_hotels = soup.find_all("div", {"class": "hotelCardListing"})
    for hotel in all_hotels:
        hotel_dict = {"name": hotel.find("h3", {"class": "listingHotelDescription__hotelName"}).text,
                      "address": hotel.find("span", {"itemprop": "streetAddress"}).text,
                      "price": hotel.find("span", {"class": "listingPrice__finalPrice"}).text}

        try:
            hotel_dict["rating"] = hotel.find("span", {"class": "hotelRating__ratingSummary"}).text
        except AttributeError:
            hotel_dict["rating"] = None

        scrapped_info_list.append(hotel_dict)
        connect.insert_into_table("OYO_HOTELS", tuple(hotel_dict.values()))

dataFrame = pandas.DataFrame(scrapped_info_list)
print("Creating csv file...")
dataFrame.to_csv("Oyo.csv")
connect.get_hotel_info("OYO_HOTELS")
