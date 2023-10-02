print("\npython influx test")

import os;
import time
import random;
import influxdb_client;
from influxdb_client.client.write_api import SYNCHRONOUS;

my_url="http://localhost:8086"
my_token = os.getenv('INFLUX_TOKEN')
#print(mytoken)
my_org = "zorg"
my_bucket = "pyflux"
my_measurement = "weather"
my_location = "xandria"

client = influxdb_client.InfluxDBClient(
    url=my_url,
    token=my_token,
    org=my_org
)

data =[]
temperature = 00.00
lower_bound = 10
upper_bound = 30
point_count = 3

write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()
delete_api = client.delete_api()

write = "yes"
query = "yes"
delete = "no"

# BEGIN Write
if write == "yes":
        print("\ngenerate & write")

        for i in range(point_count):
                temperature = round(random.uniform(lower_bound, upper_bound), 2)
                relative_humidity = round(random.uniform(lower_bound, upper_bound), 2)
                point = influxdb_client\
                        .Point(my_measurement)\
                        .tag("location", my_location)\
                        .field("temperature", temperature)\
                        .field("relative_humidity", relative_humidity)\
                        .time(time.time_ns())
                data.append(point)
                #write_api.write(bucket=mybucket, org=myorg, record=point)
                #time.sleep(10)

        for element in data:
                print(element)

        write_api.write(bucket=my_bucket, record=data)
        write_api.close
# END Write


# BEGIN Query
if query == "yes":
        print("\nquery")
        query = 'from(bucket:"pyflux")\
        |> range(start: -10m)\
        |> filter(fn:(r) => r._measurement == "weather")\
        |> filter(fn:(r) => r.location == "xandria")\
        |> filter(fn:(r) => r._field == "temperature")'

        result = query_api.query(org=my_org, query=query)
        results = []

        for table in result:
            for record in table.records:
                results.append((record.get_field(), record.get_value()))

        print(results)
# end if query == "yes"

#BEGIN Delete
if delete == "yes":
        start = "1970-01-01T00:00:00Z"
        stop = "2023-11-01T00:00:00Z"
        delete_api.delete(start, stop, '_measurement="weather"', bucket=my_bucket, org=my_org)
# END Delete

client.close()
