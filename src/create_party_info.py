"""
Creates a dictionary of party information and saves it to a json file.
"""
import json

party_info = {'Social demokratiet': {'party': 'S', 'hashtag': 'socialdemokratiet', 'mention': 'Spolitik', 'leader': {'name': 'Mette Frederiksen', 'twitter': 'MetteFrederiksen'}},
            'Venstre': {'party': 'V', 'hashtag': 'venstre', 'mention': 'venstredk'},
            'Moderaterne': {'party': 'M', 'hashtag': 'moderaterne', 'mention': 'moderaterne_dk'},
            'Socialistisk Folkeparti': {'party': 'SF', 'hashtag': '#socialistiskfolkeparti', 'mention': 'SFpolitik'},
            'Danmarksdemokraterne': {'party': 'DD', 'hashtag': 'danmarksdemokraterne'},
            'Alternativet': {'party': 'ALT', 'hashtag': 'alternativet', 'mention': 'alternativet_'},
            'Dansk folkeparti': {'party': 'DF', 'hashtag': 'danskfolkeparti', 'mention': 'DanskDf1995'},
            'Det Konservative Folkeparti': {'party': 'KF', 'hashtag': 'konservative', 'mention': 'KonservativeDK'},
            'Enhedslisten': {'party': 'EL', 'hashtag': 'enhedslisten', 'mention': 'Enhedslisten'},
            'Liberal Alliance': {'party': 'LA','hashtag':'liberalalliance', 'mention': 'LiberalAlliance'},
            'Nye Borgerlige': {'party': 'NB', 'hashtag': 'nyeborgerlige', 'mention': 'NyeBorgerlige'},
            'Radikale Venstre': {'party': 'RV', 'hashtag': 'radikale', 'mention': 'radikale'}
            
}

with open ('..data/party_info.json', 'w') as f:
    json.dump(party_info, f)