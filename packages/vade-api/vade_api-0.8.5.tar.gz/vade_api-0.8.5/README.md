# Welcome To Vadepark!

Vadepark is a SAAS service that utilizes cameras across the country to capture realtime parking data. This python package is a wrapper for our API to help you get our data into your system as soon as possible. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install vade-api.

```bash
pip install vade-api
```

## Usage

```python
import foobar

from vade_crud_api_src.vade_enums import ProductionLevel
from vade_api_src.realtime import VadeRealtimeAPI

realtime = VadeRealtimeAPI("API_KEY", ProductionLevel.BETA)

#A list of zone_id's can be recived by emailing our support email
zone_id = "dafd0c37-b7bb-4643-a23d-c4f1dc21e875"
zone_spots = realtime.get_zone_occupancy(zone_id=zone_id)
for spot in zone_spots:
    print("spot: {} in zone is occupied: {}".format(spot.uuid, spot.occupied))

# spot: 8ab1fe79-dfd0-41b5-aa04-f2d42a1186c0 in zone is occupied: True
# spot: 12eca230-23da-4145-8caf-3704798f6cb1 in zone is occupied: False
# ...

geo_spots = realtime.get_geo_occupancy(latitude=-78.685396, longitude=35.779223, radius=1000)
for spot in geo_spots:
    print("spot: {} in geo location is occupied: {}".format(spot.uuid, spot.occupied))

# spot: c54f2b8d-ca01-421f-ab94-ea56ee4853ee in geo location is occupied: True
# spot: cf7fce25-7bb7-4b3d-8bfe-0154cac4e5cb in geo location is occupied: False

single_spot = realtime.get_spot_occupancy(spot_id=geo_spots[0].uuid)
print("spot: {} is occupied: {}".format(single_spot.uuid, single_spot.occupied))
# spot: c54f2b8d-ca01-421f-ab94-ea56ee4853ee is occupied: None

```

## Parking Spot Structure
```python

class VadeSpotRealtime:
    uuid: str  # database identifier for spot
    name: str  # easy to read name for spot 
    mdid: str # secondary easy to read name for spot
    location: GeoPoint # geo-location for the parking spot
    occupancy_threshold: float # the raw occupancy confidence threshold
    raw_score: float  # the raw occupancy confidence score
    last_updated: datetime # the last time that parking spot was updated by our system
    occupied: bool  # whether or not the parking spot is occupied

```



## License
[MIT](https://choosealicense.com/licenses/mit/)