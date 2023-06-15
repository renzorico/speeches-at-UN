states = 'United States of America'
england = 'United Kingdom'
to_drop = ['the Member States','States', 'Geneva', 'New York',
           'Paris', 'Washington', 'Jerusalem','Vienna',
           'London', 'San Francisco', 'Moscow', 'Gaza',
           'Pretoria', 'the West Bank', 'Berlin','the Gaza Strip',
           'the Arab States', 'Kingdom','West Africa', 'Belgrade',
           'North Africa', 'Rome', 'Nairobi', 'Addis Ababa', 'Madrid',
           'Central Africa', 'Arab States', 'the States of the','Koreas',
           'the African States', 'Jammu', 'East Jerusalem','Havana',
           'Brussels', 'Territory', 'Copenhagen', 'African States',
           'Eritrea', 'New Delhi', 'Lusaka', 'Rio de Janeiro', 'Baghdad',
           'Lisbon', 'Beijing', 'Czechoslovakia', 'Yugoslavia']
def exact_check(column_input, check_string, change):
    if column_input == check_string:
        country = column_input.replace(column_input,change)
        return country
    return column_input


def clean_country(country:str)->str:
    country = exact_check(country, 'the United States', states)
    country = exact_check(country, 'the United States', states)
    country = exact_check(country, 'United States', states)
    country = exact_check(country, 'the United States of America', states)
    country = exact_check(country, 'America', states)
    country = exact_check(country, 'The United States', states)
    country = exact_check(country, 'the United Kingdom', england)
    country = exact_check(country, 'the Soviet Union', 'Russia')
    country = exact_check(country, 'Britain', england)
    country = exact_check(country, 'USSR', 'Russia')
    country = exact_check(country, 'the Republic of Korea', 'South Korea')
    country = exact_check(country, "the People's Republic of China", 'China')
    country = exact_check(country, "the Federal Republic of Germany", 'Germany')
    country = exact_check(country, "The Soviet Union", 'Russia')
    country = exact_check(country, "Northern Ireland", 'Ireland')
    country = exact_check(country, "the Republic of China", 'China')
    country = exact_check(country, "the Islamic Republic of Iran", 'Iran')
    country = exact_check(country, "the State of Israel", 'Israel')
    country = exact_check(country, "Great Britain", england)
    country = exact_check(country, "South Africa's", 'South Africa')
    country = exact_check(country, "Saint Vincent", 'Saint Vincent and the Grenadines')
    country = exact_check(country, "the United Arab Emirates", 'United Arab Emirates')
    country = exact_check(country, "Viet Nam", 'Vietnam')
    country = exact_check(country, "Viet-Nam", 'Vietnam')
    country = exact_check(country, "Soviet Union", 'Russia')
    country = exact_check(country, "the People’s Republic of China", 'China')
    country = exact_check(country, "the Democratic Republic of the Congo", 'Congo')
    country = exact_check(country, "the Republic of Cyprus", 'Cyprus')
    country = exact_check(country, "the Kingdom of Morocco", 'Cyprus')
    country = exact_check(country, "The United Kingdom", england)
    country = exact_check(country, "the Republic of South Africa", 'South Africa')
    country = exact_check(country, "Algiers", 'Algeria')
    country = exact_check(country, "the Republic of Cuba", 'Cuba')
    country = exact_check(country, "the Republic of Guinea", 'Guinea')
    country = exact_check(country, "the Dominican Republic", 'Dominican Republic')

    return country
