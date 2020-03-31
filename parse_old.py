# For the old json info, not using atm
stateMapping = {
    'Hamburg': 'HH',
    'Niedersachsen': 'NI',
    'Bremen': 'HB',
    'Nordrhein-Westfalen': 'NRW',
    'Hessen': 'HE',
    'Rheinland-Pfalz': 'RP',
    'Baden-Württemberg': 'BW',
    'Bayern': 'BY',
    'Saarland': 'SL',
    'Berlin': 'BE',
    'Brandenburg': 'BB',
    'Mecklenburg-Vorpommern': 'MV',
    'Sachsen': 'SN',
    'Sachsen-Anhalt': 'ST',
    'Thüringen': 'TH',
    'Schleswig-Holstein': 'SH'
}
keyMapping = [
    ('COVID-19 aktuell', 'COVID-19 aktuell in Behandlung'),
    ('COVID-19 beatmet', 'COVID-19 beatmet'),
    ('COVID-19 verstorben', 'COVID-19 verstorben'),
    ('ICU ECMO (belegt)', 'ICU ECMO (belegt)'),
    ('ICU ECMO (frei)', 'ICU ECMO (frei)'),
    ('ICU ECMO care in 24 h (Anzahl)', 'ICU ECMO care in 24 h (Anzahl)'),
    ('ICU high care (belegt)', 'ICU high care (belegt)'),
    ('ICU high care (frei)', 'ICU high care (frei)'),
    ('ICU high care in 24 h (Anzahl)', 'ICU high care in 24 h (Anzahl)'),
    ('ICU low care (belegt)', 'ICU low care (belegt)'),
    ('ICU low care (frei)', 'ICU low care (frei)'),
    ('ICU low care in 24 h (Anzahl)', 'ICU low care in 24 h (Anzahl)')
]

for filename in sorted(glob('report_*.json')):
    time = filename[7:17]
    with open(filename, 'r') as f:
        j = json.load(f)
    for dataset in j["datasets"].values():
        for data in dataset:
            if "bundesland" in data:
                name = stateMapping[data["bundesland"]]
            elif "Bundesland" in data:
                name = stateMapping[data["Bundesland"]]
            else:
                continue
            for key, newKey in keyMapping:
                result.setdefault(name, {}).setdefault(newKey, []).append({"date": time, "value": int(data[key])})

