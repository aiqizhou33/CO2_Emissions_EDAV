import quandl
import csv

quandl.ApiConfig.api_key = "dyhrKPXojNdZxDeYganv"


def retrieve_data(url):
    series_data = {}
    t = quandl.get_table("WB/DATA", series_id=url)
    for _, row in t.iterrows():
        country = row["country_name"]
        year = row["year"]
        value = row["value"]
        if country not in series_data:
            series_data[country] = {}
        if year not in series_data[country]:
            series_data[country][year] = int(value)
    return series_data


series = {
    "Electricity": [
        ("EG.ELC.PETR.ZS", "Oil"),
        ("EG.ELC.NUCL.ZS", "Nuclear"),
        ("EG.ELC.NGAS.ZS", "Natural Gas"),
        ("EG.ELC.HYRO.ZS", "Hydro"),
        ("EG.ELC.COAL.ZS", "Coal"),
    ],
    "CO2 Emissions": [
        ("EN.CO2.TRAN.ZS", "Transportation"),
        ("EN.CO2.MANF.ZS", "Manufacturing"),
        ("EN.CO2.ETOT.ZS", "Electricity"),
        ("EN.CO2.BLDG.ZS", "Buildings"),
        ("EN.CO2.OTHX.ZS", "Others"),
    ],
}

data = {}
valid_countries = []
valid_years = []
for series_name, slist in series.items():
    data[series_name] = {}
    for series_url, key_name in slist:
        print(series_name, key_name)
        series_data = retrieve_data(series_url)
        if not valid_countries:
            valid_countries = list(series_data.keys())
        if not valid_years:
            valid_years = list(range(1971, 2015))

        for country in series_data:
            if country in valid_countries:
                country_years = list(series_data[country].keys())
                if not set(country_years).issuperset(valid_years):
                    valid_countries.remove(country)
        data[series_name][key_name] = series_data

outlines = [["series", "country", "year", "key", "value"]]

for series_name, sd in data.items():
    for key_name, kd in sd.items():
        for vc in valid_countries:
            for vy in valid_years:
                value = data[series_name][key_name][vc][vy]
                outlines.append([series_name, vc, vy, key_name, value])

with open("data.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(outlines)