import urllib.request, json, csv

endpoint = "https://heatpumpmonitor.org/system/list/public.json"

with urllib.request.urlopen(endpoint) as url:
    data = json.loads(url.read().decode())
    # print(data)

# Take only Vaillant Arotherm+ 5kW systems
#
vaillant_systems_dict = [
    x
    for x in data
    if x["hp_manufacturer"] == "Vaillant"
    and x["hp_model"] == "Arotherm+"
    and x["hp_output"] == 5
]

with open("trainingset.csv", "w", newline="") as csvfile:
    writer = csv.writer(
        csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
    )

    writer.writerow(["Input", "FlowTemp", "FlowRate", "OutsideTemp"])

    rowCount = 0

    for system in vaillant_systems_dict:  # [:1]:
        feeds_endpoint = "https://heatpumpmonitor.org/timeseries/available?id={id}"
        time_series_endpoint = "https://heatpumpmonitor.org/timeseries/data?id={id}&start={start}&end={end}&feeds=heatpump_elec,heatpump_outsideT,heatpump_flowrate,heatpump_flowT&interval=3600&average=1&timeformat=notime"

        print("Processing system ID:", system["id"])

        try:
            with urllib.request.urlopen(feeds_endpoint.format(id=system["id"])) as url:
                feeds_data = json.loads(url.read().decode())

                # Use the heatpump_elec feed to determine the time range.
                #
                start = feeds_data["feeds"]["heatpump_elec"]["start_time"]
                end = feeds_data["feeds"]["heatpump_elec"]["end_time"]

                # If this system doesn't have flow rate data, skip it
                #
                if "heatpump_flowrate" not in feeds_data["feeds"]:
                    continue

                flowrate_start = feeds_data["feeds"]["heatpump_flowrate"]["start_time"]
                flowrate_end = feeds_data["feeds"]["heatpump_flowrate"]["end_time"]

                # Ensure the flow rate data covers the same time period as the electricity data
                if start != flowrate_start or end != flowrate_end:
                    continue

                # The unit of flow rate is optional and will vary between systems
                #
                if "unit" not in feeds_data["feeds"]["heatpump_flowrate"]:
                    continue

                flow_rate_unit = feeds_data["feeds"]["heatpump_flowrate"]["unit"]

                with urllib.request.urlopen(
                    time_series_endpoint.format(id=system["id"], start=start, end=end)
                ) as url:
                    time_series_data = json.loads(url.read().decode())

                    for i in range(len(time_series_data["heatpump_elec"])):
                        elec = time_series_data["heatpump_elec"][i]
                        flowT = time_series_data["heatpump_flowT"][i]
                        flowRate = time_series_data["heatpump_flowrate"][i]
                        outsideT = time_series_data["heatpump_outsideT"][i]

                        if (
                            elec is not None
                            and flowT is not None
                            and flowRate is not None
                            and outsideT is not None
                        ):
                            if flowRate < 5:  # skip very low flow rates
                                continue

                            if flow_rate_unit == "m³/h":  # Otherwise assume l/min
                                flowRate = flowRate * 1000 / 60  # convert to l/min

                            writer.writerow([elec, flowT, flowRate, outsideT])
                            rowCount += 1

        except Exception as e:
            print(
                "An exception occurred processing system %d : %s. Skipping to the next system.",
                system["id"],
                repr(e),
            )

    print("Wrote ", rowCount)
