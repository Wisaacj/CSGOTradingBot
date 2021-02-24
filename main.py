import requests
from bs4 import BeautifulSoup
import pandas as pd
from prettytable import PrettyTable

""" To do list

1. Parse data from skinport
2. Check for discounts
3. Add data to a dictionary
4. Filter the data

"""
        
#################### Getting skinport data #########################

def gatherData(pageNum):
    
    # Declaring the skinport_data dictionary
    bitskins_data = {"Item": [],
                     "Wear": [],
                     "Price on Bitskins": [],
                     "Discount": []}

    for i in range(pageNum):
        
        # Printing page number
        print(f"Getting data for page: {i}")
        
        # Url for steam csgo skin market
        url = "https://bitskins.com/?appid=730&page=" + str(i) + "&advanced=1&pattern=1&is_stattrak=0&has_stickers=0&is_souvenir=0&show_trade_delayed_items=-1&sort_by=bumped_at&order=desc"
        
        # Getting page data
        page = requests.get(url)
        
        # Getting the page content
        page_content = page.content
        
        # Parsing the content
        soup = BeautifulSoup(page_content, "html.parser")
        
        # Finding each item on the page
        tabl = soup.find_all("div", {"class": "col-lg-3 col-md-4 col-sm-5 col-xs-12 item-solo"})
        
        # Iterating through the items
        for t in tabl:
            bitskins_data["Item"].append(t.find("div", {"class": "panel-heading item-title"}).get_text())
            bitskins_data["Wear"].append(t.find("div", {"class": "item-sub-info"}).get_text().split("/")[0])
            bitskins_data["Price on Bitskins"].append(t.find("span", {"class": "item-price-display"}).get_text())
            
            try:
                bitskins_data["Discount"].append(int(t.find("span", {"class": "badge badge-info"}).get_text().split("%")[0]))
            except:
                bitskins_data["Discount"].append(0)
                
    return bitskins_data

####################### Filtering the data ##############################

def filterData(df):
    DF = df.copy()
    
    for i in range(len(DF)):
        if ((DF["Discount"][i]) < 40):
            DF.drop(index=i, axis=0, inplace=True)
    
    DF.reset_index()
    DF.sort_values(by=["Discount"], ascending=False, inplace=True)
    return DF

######################### Main function ################################

raw_data = gatherData(20)
data_df = pd.DataFrame(raw_data)
processed_data_df = filterData(data_df)

output_table = PrettyTable()
output_table.add_column("Item", processed_data_df["Item"].tolist())
output_table.add_column("Wear", processed_data_df["Wear"].tolist())
output_table.add_column("Price on Bitskins", processed_data_df["Price on Bitskins"].tolist())
output_table.add_column("Discount", processed_data_df["Discount"].tolist())

print(output_table)