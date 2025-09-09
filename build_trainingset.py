import urllib.request, json, csv

endpoint = "https://heatpumpmonitor.org/system/list/public.json"

with urllib.request.urlopen(endpoint) as url:
    data = json.loads(url.read().decode())
    #print(data)

vaillant_systems_dict = [x for x in data if x['hp_manufacturer'] == 'Vaillant' 
                        and x['hp_model'] == 'Arotherm+' 
                        and x['hp_output'] == 5]

print(len(vaillant_systems_dict))

with open('trainingset.csv', 'w', newline='') as csvfile:

    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    writer.writerow(['Input', 'TargetTemperature', 'OutsideTemperature'])

    for system in vaillant_systems_dict: #[:1]:

        time_series_endpoint = "https://heatpumpmonitor.org/timeseries/data?id={id}&start=22-01-2023&end=06-09-2025&feeds=heatpump_elec,heatpump_roomT,heatpump_outsideT&interval=1800&average=1&timeformat=notime"

        try:
            with urllib.request.urlopen(time_series_endpoint.format(id = system['id'])) as url:
                time_series_data = json.loads(url.read().decode())

                for i in range(len(time_series_data['heatpump_elec'])):

                    elec = time_series_data['heatpump_elec'][i]
                    roomT = time_series_data['heatpump_roomT'][i]
                    outsideT = time_series_data['heatpump_outsideT'][i]

                    if elec is not None and roomT is not None and outsideT is not None:
                        writer.writerow([elec, roomT, outsideT])    

        except Exception as e:
            print("An exception occurred: %s", repr(e))