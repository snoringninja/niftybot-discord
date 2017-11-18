import pymysql
import sqlite3
import os

import json
import urllib
from urllib.request import urlopen
import urllib.parse
import urllib.error
import time

path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../'))
sqlite_database = ('niftybot.db')

# some variables
dump_skills = 1
dump_traits = 0
dump_specs = 0

print(sqlite_database)

database = sqlite3.connect(sqlite_database)
cursor = database.cursor()

#print(data_skills)

def build_id_list(start_int, end_int, data_skills_list):
    cur_string = ""
    print(start_int, end_int)
    for x in range(start_int, end_int + 1):
        cur_id = data_skills_list[x]
        cur_string = cur_string + str(data_skills_list[x]) + ', '

    cur_string = cur_string.replace(' ', '%20')
    return cur_string

def insert_into_db_skills(id_list):
    for x in range(len(id_list)):
        try:
            slot = ""
            slot = id_list[x]['slot']
        except Exception as ex:
            slot = "EMPTY_SLOT"
        cursor.execute("INSERT INTO gw2_skills (skill_id, skill_name, slot) VALUES (?, ?, ?)", (id_list[x]['id'], id_list[x]['name'], slot))
        database.commit()

def insert_into_db_traits(id_list):
    for x in range(len(id_list)):
        try:
            specialization = ""
            specialization = id_list[x]['specialization']
        except Exception as ex:
            specialization = "EMPTY_SLOT"
        cursor.execute("INSERT INTO gw2_traits (trait_id, trait_name, spec_id) VALUES (?, ?, ?)", (id_list[x]['id'], id_list[x]['name'], specialization))
        database.commit()

def insert_into_db_specs(id_list):
    for x in range(len(id_list)):
        cursor.execute("INSERT INTO gw2_specs (spec_id, spec_name) VALUES (?, ?)", (id_list[x]['id'], id_list[x]['name']))
        database.commit()

# for y in range(len(data_skills2)):
#   print("{0}, {1}".format(data_skills2[y]['id'], data_skills2[y]['name']))

#print("Loop one complete.")


if dump_skills == 1:
    counter = 0
    start_int = 0

    id_list = []

    base_url_skills = 'https://api.guildwars2.com/v2/skills'
    response_url_skills = base_url_skills
    response_skills = urlopen(response_url_skills)
    response_skills = response_skills.read()
    response_skills = response_skills.decode("utf-8")
    data_skills = json.loads(response_skills)

    data_skills2 = []
    base_url_skills2 = 'https://api.guildwars2.com/v2/skills?ids=44165,44239,44240,44241,44248,44260,44278,44296,44321,44360,44364,44384,44386,44397,44405,44428,44451,44514,44526,44550,44591,44602,44612,44617,44626,44637,44646,44652,44663,44677,44681,44695,44791,44840,44846,44864,44885,44918,44926,44937,44946,44948,44980,44991,44998,45023,45046,45047,45067,45082,45088,45094,45142,45160,45216,45218,45219,45230,45243,45252,45259,45313,45333,45380,45402,45426,45449,45460,45479,45508,45537,45581,45666,45672,45686,45709,45711,45717,45732,45742,45743,45746,45773,45780,45789,45797,45846,45970,45979,45983,46014,46018,46024,46044,46058,46123,46140,46148,46170,46183,46185,46233,46295,46335,46360,46386,46409,46432,46447,46473,46474,46487,46547,46600,46627,46629,46732,46737,46750,46843,46847,46849,46854,46856,46857'
    response_url_skills2 = base_url_skills2
    response_skills2 = urlopen(response_url_skills2)
    response_skills2 = response_skills2.read()
    response_skills2 = response_skills2.decode("utf-8")
    data_skills2 = json.loads(response_skills2)

    insert_into_db_skills(data_skills2)


    # for x in range(19):
    #     print(x)
    #     if x < 18:
    #         end_int = (counter + 1) * 100
    #         counter = counter + 1

    #         id_list = []
    #         id_list = build_id_list(start_int, end_int, data_skills)

    #         data_skills2 = []
    #         base_url_skills2 = 'https://api.guildwars2.com/v2/skills?ids=' + str(id_list)
    #         response_url_skills2 = base_url_skills2
    #         response_skills2 = urlopen(response_url_skills2)
    #         response_skills2 = response_skills2.read()
    #         response_skills2 = response_skills2.decode("utf-8")
    #         data_skills2 = json.loads(response_skills2)

    #         insert_into_db_skills(data_skills2)

    #         start_int = end_int + 1

    #         time.sleep(10)
    #     elif x == 18:
    #         #id_list = []
    #         #id_list = build_id_list(1802, 1863)

    #         data_skills2 = []
    #         base_url_skills2 = 'https://api.guildwars2.com/v2/skills?ids=39646,%2039648,%2039653,%2039664,%2039667,%2039668,%2039673,%2039674,%2039684,%2039685,%2039686,%2039691,%2039694,%2039701,%2039708,%2039711,%2039713,%2039714,%2039728,%2039734,%2039745,%2039746,%2039748,%2039755,%2039760,%2039765,%2039770,%2039775,%2039782,%2039787,%2039788,%2039790,%2039795,%2039801,%2039816,%2039823,%2039829,%2039830,%2039839,%2039845,%2039847,%2039848,%2039849,%2039853,%2039854,%2039857,%2039863,%2039867,%2039874,%2039875,%2039879,%2039884,%2039886,%2039889,%2039894,%2039895,%2039910,%2039911,%2039915,%2039916,%2039920,%2039924'
    #         response_url_skills2 = base_url_skills2
    #         response_skills2 = urlopen(response_url_skills2)
    #         response_skills2 = response_skills2.read()
    #         response_skills2 = response_skills2.decode("utf-8")
    #         data_skills2 = json.loads(response_skills2)

    #         insert_into_db_skills(data_skills2)

if dump_traits == 1:
    start_int = 0
    counter = 0

    id_list = []

    base_url_skills = 'https://api.guildwars2.com/v2/traits'
    response_url_skills = base_url_skills
    response_skills = urlopen(response_url_skills)
    response_skills = response_skills.read()
    response_skills = response_skills.decode("utf-8")
    data_skills = json.loads(response_skills)

    data_skills2 = []
    base_url_skills2 = 'https://api.guildwars2.com/v2/traits?ids=2059,2060,2061,2062,2063,2064,2066,2067,2069,2070,2071,2072,2073,2074,2075,2076,2077,2078,2079,2080,2081,2082,2084,2085,2086,2087,2088,2089,2090,2091,2092,2093,2094,2095,2096,2097,2098,2099,2100,2101,2102,2103,2105,2106,2107,2108,2109,2110,2111,2112,2113,2114,2115,2116,2117,2118,2119,2120,2121,2122,2123,2124,2125,2126,2127,2128,2129,2130,2131,2133,2134,2135,2136,2137,2138,2140,2141,2142,2143,2144,2145,2146,2147,2148,2149,2150,2151,2152,2153,2154,2155,2156,2157,2158,2159,2160,2161,2162,2163,2164,2165,2166,2167,2168,2169,2170,2171,2172,2173,2174,2175,2177,2178,2179,2180,2181,2182'
    response_url_skills2 = base_url_skills2
    response_skills2 = urlopen(response_url_skills2)
    response_skills2 = response_skills2.read()
    response_skills2 = response_skills2.decode("utf-8")
    data_skills2 = json.loads(response_skills2)

    insert_into_db_traits(data_skills2)

    # for x in range(7):
    #     if x < 6:
    #         end_int = (counter + 1) * 100
    #         counter = counter + 1

    #         id_list = []
    #         id_list = build_id_list(start_int, end_int, data_skills)

    #         #print(id_list)

    #         data_skills2 = []
    #         base_url_skills2 = 'https://api.guildwars2.com/v2/traits?ids=' + str(id_list)
    #         response_url_skills2 = base_url_skills2
    #         response_skills2 = urlopen(response_url_skills2)
    #         response_skills2 = response_skills2.read()
    #         response_skills2 = response_skills2.decode("utf-8")
    #         data_skills2 = json.loads(response_skills2)

    #         insert_into_db_traits(data_skills2)

    #         start_int = end_int + 1

    #         time.sleep(10)
    #     elif x == 6:
    #         data_skills2 = []
    #         base_url_skills2 = 'https://api.guildwars2.com/v2/traits?ids=1981,1983,1984,1985,1986,1987,1988,1992,1993,1994,1995,1997,1999,2000,2001,2002,2004,2005,2006,2008,2009,2011,2013,2014,2015,2016,2017,2018,2020,2021,2022,2023,2025,2026,2028,2030,2031,2032,2033,2035,2036,2037,2038,2039,2042,2043,2046,2047,2049,2050,2052,2053,2055,2056,2057,2058'
    #         response_url_skills2 = base_url_skills2
    #         response_skills2 = urlopen(response_url_skills2)
    #         response_skills2 = response_skills2.read()
    #         response_skills2 = response_skills2.decode("utf-8")
    #         data_skills2 = json.loads(response_skills2)

    #         insert_into_db_traits(data_skills2)

if dump_specs == 1:
    base_url_skills = 'https://api.guildwars2.com/v2/specializations'
    response_url_skills = base_url_skills
    response_skills = urlopen(response_url_skills)
    response_skills = response_skills.read()
    response_skills = response_skills.decode("utf-8")
    data_skills = json.loads(response_skills)

    print(len(data_skills))

    id_list = build_id_list(53, 62, data_skills)

    data_skills2 = []
    base_url_skills2 = 'https://api.guildwars2.com/v2/specializations?ids=' + str(id_list)
    response_url_skills2 = base_url_skills2
    response_skills2 = urlopen(response_url_skills2)
    response_skills2 = response_skills2.read()
    response_skills2 = response_skills2.decode("utf-8")
    data_skills2 = json.loads(response_skills2)

    insert_into_db_specs(data_skills2)

# data_skills2 = []
# base_url_skills2 = 'https://api.guildwars2.com/v2/skills?ids=39646,%2039648,%2039653,%2039664,%2039667,%2039668,%2039673,%2039674,%2039684,%2039685,%2039686,%2039691,%2039694,%2039701,%2039708,%2039711,%2039713,%2039714,%2039728,%2039734,%2039745,%2039746,%2039748,%2039755,%2039760,%2039765,%2039770,%2039775,%2039782,%2039787,%2039788,%2039790,%2039795,%2039801,%2039816,%2039823,%2039829,%2039830,%2039839,%2039845,%2039847,%2039848,%2039849,%2039853,%2039854,%2039857,%2039863,%2039867,%2039874,%2039875,%2039879,%2039884,%2039886,%2039889,%2039894,%2039895,%2039910,%2039911,%2039915,%2039916,%2039920,%2039924'
# response_url_skills2 = base_url_skills2
# response_skills2 = urlopen(response_url_skills2)
# response_skills2 = response_skills2.read()
# response_skills2 = response_skills2.decode("utf-8")
# data_skills2 = json.loads(response_skills2)

# insert_into_db_skills(data_skills2)

# data_skills2 = []
# base_url_skills2 = 'https://api.guildwars2.com/v2/traits?ids=1981,1983,1984,1985,1986,1987,1988,1992,1993,1994,1995,1997,1999,2000,2001,2002,2004,2005,2006,2008,2009,2011,2013,2014,2015,2016,2017,2018,2020,2021,2022,2023,2025,2026,2028,2030,2031,2032,2033,2035,2036,2037,2038,2039,2042,2043,2046,2047,2049,2050,2052,2053,2055,2056,2057,2058'
# response_url_skills2 = base_url_skills2
# response_skills2 = urlopen(response_url_skills2)
# response_skills2 = response_skills2.read()
# response_skills2 = response_skills2.decode("utf-8")
# data_skills2 = json.loads(response_skills2)

# insert_into_db_traits(data_skills2)

# x = build_id_list(401, 500)
# print(x)