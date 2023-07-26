import geocoder
import geopandas as gpd
import numpy as np
import pandas as pd
from pathlib import Path


def read_data():
    print("Reading files...")
    path = '../dataFiles'
    files = Path(path).glob('*.json')
    dfs = list()
    for f in files:
        file = open(f, "r")
        # if the file has not been read
        if file.readline() != 'read\n':
            data = pd.read_json(f)
            data['file'] = f.stem
            dfs.append(data)
            # line_prepender(f)

    if len(dfs) < 1:
        return pd.DataFrame(dfs)
    else:
        return clean_df(pd.concat(dfs, ignore_index=True))


def line_prepender(filename):
    # Adds 'read' to the first name of a file
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write('read' + '\n' + content)


def clean_df(data: pd.DataFrame) -> gpd.GeoDataFrame:
    print("Cleaing Data...")
    relations_list = data.get("relations")
    tweets = data.get("tweet")
    entity_list = data.get("entities")
    entity_relations = entity_list + relations_list

    # creates empty dataframe to append data
    df = pd.DataFrame(
        columns=['place name', 'type of impact', 'impact place relation', 'modifier place relation',
                 'severity impact relation', 'item impact relation', 'tweet text', 'impact category'])
    i = 0

    for items in entity_relations:
        [tweet] = tweets[i]
        for row in get_relations_entities(items, tweet):
            df = pd.concat([df, pd.DataFrame.from_records([row])])
        i += 1
    print(df)
    ''' 
    df['type of impact'] = df['type of impact'].apply(str.title)
    df = get_impact_category(df.reset_index(drop=True))
    df = get_coordinates(df.reset_index(drop=True))
    df.dropna(inplace=True)

    return create_gdf(df)
    '''


def get_relations_entities(items, tweet):
    place, impact, location, sev_impact, item_impact = [], [], [], [], []
    impact_place = ""
    rows = []

    count, impact_relations = count_occurrences(items, "place_impact_rel")

    if len(impact_relations) > 1:
        for relation in impact_relations:
            impact_place = tweet[relation[0]:relation[1]] + ' ' + tweet[relation[2]:relation[3]]
            for item in items:
                if len(item) == 3:
                    if item[2] == 'place name':
                        place.append(tweet[item[0]:item[1]])
                    elif item[2] == 'type of impact':
                        impact.append(tweet[item[0]:item[1]])
                elif len(item) == 5:
                    match item[4]:
                        case 'modifier_place_rel':
                            location.append(tweet[item[0]:item[1]] + ' ' + tweet[item[2]:item[3]])
                        case 'severity_impact_rel':
                            sev_impact.append(tweet[item[0]:item[1]] + ' ' + tweet[item[2]:item[3]])
                        case 'item_impact_rel':
                            item_impact.append(tweet[item[0]:item[1]] + ' ' + tweet[item[2]:item[3]])
            rows.append({'place name': place,
                         'type of impact': impact,
                         'impact place relation': impact_place,
                         'modifier place relation': location,
                         'severity impact relation': sev_impact,
                         'item impact relation': item_impact,
                         'tweet text': tweet})

    return rows

    '''
    for item in items:
        if len(item) == 3:
            if item[2] == 'place name':
                place.append(tweet[item[0]:item[1]])
            elif item[2] == 'type of impact':
                impact.append(tweet[item[0]:item[1]])
        elif len(item) == 5:
            match item[4]:
                case 'modifier_place_rel':
                    location.append(tweet[item[0]:item[1]] + ' ' + tweet[item[2]:item[3]])
                case 'place_impact_rel':
                    impact_place.append(tweet[item[0]:item[1]] + ' ' + tweet[item[2]:item[3]])
                case 'severity_impact_rel':
                    sev_impact.append(tweet[item[0]:item[1]] + ' ' + tweet[item[2]:item[3]])
                case 'item_impact_rel':
                    item_impact.append(tweet[item[0]:item[1]] + ' ' + tweet[item[2]:item[3]])
    '''


def count_occurrences(list_of_lists, target):
    count = 0
    relations = []
    for sublist in list_of_lists:
        for item in sublist:
            if item == target:
                relations.append(sublist)
                count += 1
    return count, relations


def handle_relations(df):
    pass
    '''
    for index, row in df.iterrows():
        if len(row['impact place relation']) > 1:
            for place in row['place name']:
                for impact_rel in row['impact place relation']:
                    if place in impact_rel:
                        if type

                        new_row = pd.DataFrame(
                            {'place name': place,
                             'type of impact': ,
                             'impact place relation': impact_rel,
                             'modifier place relation': location,
                             'severity impact relation': sev_impact,
                             'item impact relation': item_impact,
                             'tweet text': tweet})
                    df2 = pd.concat([new_row, df.loc[:]]).reset_index(drop=True)
                    new_row = []
                    print(place)
                    # print(df['impact place relation'][ind])
                '''


def get_impact_category(data):
    # This could be MUCH improved and not be hard coded. May need to add more words to each category as more data is received
    damage = ['Damage', 'Damages', 'Damaged', 'Collapse', 'Collapsed', 'Down', 'Destroyed', 'Destroy', 'Destroys']
    death = ['Dead', 'Killed', 'Kill', 'Kills', 'Die', 'Dies', 'Died', 'Loss', 'Loss Of Life', 'Death Toll',
             'Claims',
             'Claim', 'Death', 'Deaths', 'Deads', 'Daed']
    fire = ['Fire', 'Fires', 'Flames', 'Flame', 'Blaze', 'Smoke']
    flood = ['Flood', 'Floods', 'Wash Away', 'Sweep Away', 'Submerge', 'Flood Hits']
    injury = ['Injured', 'Injury', 'Injuries', 'Injures', 'Hurt', 'Hurts']
    missing = ['Missing', 'Missing Person', 'Missing People']
    terrorism = ['Bombing', 'Bomb']
    trapped = ['Trap', 'Traps', 'Marooned', 'Maroon', 'Maroons', 'Stranded', 'Strands', 'Strand']

    for index, row in data.iterrows():
        impacts = row["type of impact"]
        impacts = impacts.split(':')
        impacts = [x for x in impacts if x != '']
        for impact in impacts:
            match impact:
                case impact if impact in damage:
                    data.loc[[index], 'impact category'] = 'Damage'
                case impact if impact in death:
                    data.loc[[index], 'impact category'] = 'Death'
                case impact if impact in fire:
                    data.loc[[index], 'impact category'] = 'Fire'
                case impact if impact in flood:
                    data.loc[[index], 'impact category'] = 'Flood'
                case impact if impact in injury:
                    data.loc[[index], 'impact category'] = 'Injury'
                case impact if impact in missing:
                    data.loc[[index], 'impact category'] = 'Missing'
                case impact if impact in terrorism:
                    data.loc[[index], 'impact category'] = 'Terrorism'
                case impact if impact in trapped:
                    data.loc[[index], 'impact category'] = 'Trapped'
                case _:
                    data.loc[[index], 'impact category'] = 'Other'

    return data


def get_coordinates(data):
    data["latitude"] = np.nan
    data["longitude"] = np.nan

    for index, row in data.iterrows():
        # Looked at GeoTxt but it is not going to work
        g = geocoder.geonames(row['place name'], key='QuakeText')
        if g.current_result:
            data.loc[[index], 'latitude'] = g.lat
            data.loc[[index], 'longitude'] = g.lng
    # To identify which names are not being found in GeoNames - they are normally unusual/misspelled names
    # else:
    #     print("Unable to find:" + row['place name'] + ' in geonames')
    return data


def create_gdf(data: pd.DataFrame) -> gpd.GeoDataFrame:
    print("Creating GDF...")
    gdf = gpd.GeoDataFrame(
        data, crs='EPSG:4326', geometry=gpd.points_from_xy(data.longitude, data.latitude))
    gdf = gdf.drop(columns=["latitude", "longitude"])
    return gdf


read_data()
