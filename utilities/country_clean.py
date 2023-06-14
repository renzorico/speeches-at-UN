#more countries need to be cleaned!
#these were the ones most mentioned for war
#last line is to eliminate all mentioned to "States"
from utilities.plot_map import load_geo
import numpy as np
import ast
from difflib import SequenceMatcher
geo = load_geo().ADMIN.values
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()



def clean_country_name(country_name):

    countries_mentioned = [mention.replace('the United States of America', 'United States')
                            .replace('United States', 'United States')
                            .replace('the United States', 'United States')
                            .replace('the Soviet Union', 'Soviet Union')
                            .replace('The Soviet Union', 'Soviet Union')

                            .replace('USSR', 'Soviet Union')
                            .replace('the Federal Republic of Germany', 'Germany')
                            .replace('West Bank', 'Palestine')
                            .replace('South Korea', 'Korea')
                            .replace('Hanoi', 'Vietnam')
                            .replace('Washington', 'United States')
                            .replace('Paris', 'France')
                            .replace('Viet-Nam', 'Vietnam')
                            .replace('Viet Nam', 'Vietnam')
                            .replace('South Viet-Nam', 'Vietnam')
                            .replace('North Viet-Nam', 'Vietnam')

                            .replace('South Viet Nam', 'Vietnam')
                            .replace('the Vietnam', 'Vietnam')
                            .replace('the United Kingdom', 'United Kingdom')
                            .replace('The United States', 'United States')
                            .replace('America', 'United States')
                            .replace('Berlin', 'Germany')
                            .replace('the Palestine', 'Palestine')
                            .replace('Peking', 'China')
                            .replace('Bosnia and Herzegovina', 'Bosnia')
                            .replace('the German Democratic Republic', 'Germany')
                            .replace('Moscow', 'Rusia')
                            .replace('Gaza', 'Palestine')
                            .replace('West Germany', 'Germany')
                            .replace('Saigon', 'Vietnam')
                            .replace('the Islamic Republic of Iran', 'Iran')
                            .replace('Phnom Penh', 'Cambodia')
                            .replace('the Socialist Republic of Vietnam', 'Vietnam')
                            .replace('the Republic of Viet-Nam', 'Vietnam')
                            .replace('the People\'s Republic of China', 'China')
                            .replace('the Republic of Korea', 'Korea')
                            .replace('the Democratic Republic of Vietnam', 'Vietnam')
                            .replace('South Vietnam', 'Vietnam')
                            .replace('the Republic of Vietnam', 'Vietnam')
                            .replace('Rusia' ,'Russia')
                            .replace('the Palestine Strip' ,'Palestine')
                            .replace('the Republic of Cyprus' ,'Cyprus')
                            .replace('Tel Aviv' ,'Israel')
                            .replace('Koreas' ,'Korea')
                            .replace('Cairo' ,'Egypt')
                            .replace('Western Germany' ,'Germany')
                            .replace('the People’s Republic of China' ,'China')
                            .replace('Beirut' ,'Lebanon')
                            .replace('VietNam' ,'Vietnam')
                            .replace('Pretoria' ,'South Africa')
                            .replace('North Vietnam' ,'Vietnam')
                            .replace('the Arab States' ,'Arab States')

                            .replace('the Democratic Republic of Afghanistan', 'Afghanistan')
                            .replace('the Republic of', '')
                            .replace("the", "")

                            # Add more recoding patterns as needed
                            for mention in countries_mentioned if mention !='States']
    return countries_mentioned

def clen_country_v2(country:str):
    similarities = []



    country = country.replace("The", "").replace("Kingdom", "").replace("Islamic", "").replace("Democratic", "").replace("Republic", "")
    country = country.replace("of", "").replace("the", "").replace("United", "").replace("Federal", "").replace("Socialist", "").replace("People's", "").replace("union", "")
    country = country.replace("USA", "United States of America").replace("States", "United States of America").replace("America", "United States of America")
    #for every in geo:
        #similarities.append(similar(country.lower(), every.lower()))

    #new_name = geo[np.argmax(np.array(similarities))]

    #print(country,new_name)

    return country

