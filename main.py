import time

import numpy as np
import pandas as pd

from driver import driver

BASE_URL = "http://www.estrenarvivienda.com/proyectos-vivienda"

CITY = "bogota"

ZONES = ["centro", "norte", "noroccidente", "occidente", "sur"]

def get_projects(base_url, city, zones):

    property_titles = []
    property_types = []
    property_addresses = []
    property_prices = []
    property_built_areas = []
    property_private_areas = []
    property_status = []
    property_bedrooms = []
    property_bathrooms = []
    property_parking_slots = []
    property_finishes = []
    property_stratum = []
    property_developers = []
    property_country = []
    property_city = []
    property_zone = []
    
    for zone in zones:
        try:
            driver.get(f'{base_url}/{city}/{zone}')
            time.sleep(10)
        except:
            print("Couldn't connect to URL.")

        try:
            agree_button = driver.find_element_by_xpath("//button[@class='agree-button eu-cookie-compliance-default-button']")
            agree_button.click()
            time.sleep(5)
        except:
            print("There aren't any more cookies to agree with.")
        
        try:
            load_more_button = driver.find_element_by_xpath("//a[@class='load-more']")
            while load_more_button:
                load_more_button.click()
                time.sleep(5)
        except:
            print("There aren't any more projects to load.")
        
        try:
            projects_links = driver.find_elements_by_xpath("//a[@class='link-project']")
            projects_urls = [project.get_attribute("href") for project in projects_links]
            projects_urls = projects_urls[::3]
        except Exception as e:
            print(e)

        for url in projects_urls:

            try:
                driver.get(url)
                time.sleep(10)
            except Exception as e:
                print(e)
                continue

            try:
                title = driver.find_element_by_xpath("//h1[@class='title-project']").text.strip().lower()
            except:
                title = np.nan
        
            try:
                types = driver.find_element_by_xpath("//h1[@class='title-project']/span[@class='sector-project']").text.strip().lower()
            except:
                types = np.nan 

            title = title.replace(types, "").replace("\n", "")

            try:
                address = driver.find_element_by_xpath("//div[@class='project-adress']/p").text.replace("Dirección:","").lower()
            except:
                address = np.nan

            try:
                price = int(driver.find_element_by_xpath("//div[@class='field-content card-project-price']").text.replace("$","").replace(".","").strip())
            except:
                price = np.nan

            try:    
                built_area = float(driver.find_element_by_xpath("//div[@class='views-field views-field-field-built-area field-built-area']/div").text.replace("m2","").strip())
            except:
                built_area = np.nan 

            try:
                private_area = float(driver.find_element_by_xpath("//div[@class='views-field views-field-field-private-area field-built-area']/div").text.replace("m2","").strip())
            except:
                private_area = np.nan 

            try:    
                status = driver.find_element_by_xpath("//div[@class='views-field views-field-field-field-status field-status']/div").text.strip().lower()
            except:
                status = np.nan 

            try:
                bedrooms = int(driver.find_element_by_xpath("//div[@class='views-field views-field-field-opt-bedrooms-1 field-bedrooms']/div").text)
            except:
                bedrooms = np.nan 

            try:    
                bathrooms = int(driver.find_element_by_xpath("//div[@class='views-field views-field-field-opt-bathrooms-1 field-bathrooms']/div").text)
            except:
                bathrooms = np.nan 
        
            try:
                parking_slots = driver.find_element_by_xpath("//div[@class='views-field views-field-field-opt-garages-1 field-garages']/div").text.lower()
            except:
                parking_slots = np.nan

            try:    
                finishes = driver.find_element_by_xpath("//div[@class='views-field views-field-field-tipology-acabados']/div").text.lower()
            except:
                finishes = np.nan 
        
            try:
                stratum = driver.find_element_by_xpath("//div[@class='views-field views-field-field-opt-stratum views-field-field-stratum']/div").text.replace("Estrato:", "").replace("!","").strip()
            except:
                stratum = np.nan 
        
            try:
                developer = driver.find_element_by_xpath("//div[@class='views-field views-field-nothing-6']/span/a").text.lower()
            except:
                developer = np.nan

            project_country = "colombia"
            project_city = f'{city}'.replace("/","")
            project_zone = f'{zone}'

            property_titles.append(title)
            property_types.append(types)
            property_addresses.append(address)
            property_prices.append(price)
            property_built_areas.append(built_area)
            property_private_areas.append(private_area)
            property_status.append(status)
            property_bedrooms.append(bedrooms)
            property_bathrooms.append(bathrooms)
            property_parking_slots.append(parking_slots)
            property_finishes.append(finishes)
            property_stratum.append(stratum)
            property_developers.append(developer)
            property_country.append(project_country)
            property_city.append(project_city)
            property_zone.append(project_zone)

    projects_data = {
        "title":property_titles,
        "type":property_types,
        "address":property_addresses,
        "price":property_prices,
        "built_area":property_built_areas,
        "private_area":property_private_areas,
        "status":property_status,
        "bedrooms":property_bedrooms,
        "bathrooms":property_bathrooms,
        "parking_slots": property_parking_slots,
        "finishes": property_finishes,
        "stratum":property_stratum,
        "developers":property_developers,
        "country":property_country,
        "city":property_city,
        "zone":property_zone,
    }

    driver.close()

    return projects_data

def get_data_frame(data):

    df = pd.DataFrame(data)
    df.to_csv("projects.csv")


if __name__ == "__main__":

    data = get_projects(BASE_URL, CITY, ZONES)

    get_data_frame(data=data)