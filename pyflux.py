print("\npython influx test")

import os;
import time
import datetime;
import random;
import influxdb_client;
from influxdb_client.client.write_api import SYNCHRONOUS;

mybucket = "pyflux"
myorg = "zorg"
myurl="http://localhost:8086"
mytoken = os.getenv('INFLUX_TOKEN')
#print(mytoken)
client = influxdb_client.InfluxDBClient(
    url=myurl,
    token=mytoken,
    org=myorg
)

data =[] #list
temperature = 00.00
lower_bound = 10
upper_bound = 30
point_count = 7

query = "no"

# Write script
print("\ngenerate & write")
write_api = client.write_api(write_options=SYNCHRONOUS)

for i in range(point_count):
        temperature = round(random.uniform(lower_bound, upper_bound), 2)
        relative_humidity = round(random.uniform(lower_bound, upper_bound), 2)
        point = influxdb_client\
                .Point("weather")\
                .tag("location", "Prague")\
                .field("temperature", temperature)\
                .field("relative_humidity", relative_humidity)\
                .time(time.time_ns())
        data.append(point)
        #write_api.write(bucket=mybucket, org=myorg, record=point)
        #time.sleep(10)

for element in data:
        print(element)

write_api.write(bucket=mybucket, record=data)
write_api.close

# Query script

if query == "yes":
        print("\nquery")
        query_api = client.query_api()
        query = 'from(bucket:"pyflux")\
        |> range(start: -10m)\
        |> filter(fn:(r) => r._measurement == "weather")\
        |> filter(fn:(r) => r.location == "Prague")\
        |> filter(fn:(r) => r._field == "temperature")'

        result = query_api.query(org=myorg, query=query)
        results = []

        for table in result:
            for record in table.records:
                results.append((record.get_field(), record.get_value()))

        print(results)
# end if query == "yes"

client.close()
