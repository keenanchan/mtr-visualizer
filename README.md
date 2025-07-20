# MTR Real Time Map

## Introduction
Real-time dashboard for trains active in the Hong Kong MTR (Mass Transit Railway) system. 

For each station, estimated times of arrivals for the next few trains are polled from the publicly available [MTR Next Train API](https://data.gov.hk/en-data/dataset/mtr-data2-nexttrain-data), using RabbitMQ. At the same time, we use [Overpass Turbo](https://overpass-turbo.eu/) to obtain geoJSON assets of each line, including station / platform locations. These assets are stored using timescaleDB (time-series database), and PostGIS (geographical data).

Assuming each train travels at ~40 kmph and assuming roughly 45 seconds of dwell time per station, using the derived geographical assets we are able to filter station-wise ETAs to those that correspond to trains that are traveling from the immediately preceding station. By doing this, we can gain a rough measure of train locations by converting ETAs, first to remaining travel time and then to line-wise progress. 

Note that delay handling is still a work in progress; any delays or service disruptions will affect the accuracy of this visualization.

This visualization currently only displays three lines (Island Line, Tsuen Wan Line, Kwun Tong Line), but there are plans to add more lines. Another line of improvement is to use MTR's [Train Trip Planner](https://www.mtr.com.hk/en/customer/jp/index.php) for a better measure of travel times between stations.

## Getting Started Locally

Ensure Docker is installed and running. After cloning this repo, run the following command within the root folder:
```
docker compose up --build -d
```

You can then navigate to http://localhost:3000, which houses the exposed Grafana data visualization port. 

To stop the application, run:
```
docker compose down
```

## Contact
Happy to answer any questions! Please contact me at keenanjchan@gmail.com.

Or, visit me at [my website](www.keenanchan.com). Let's talk more!