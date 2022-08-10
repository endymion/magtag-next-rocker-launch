# SPDX-FileCopyrightText: 2020 Anne Barela for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# SpaceX Launch Display, by Anne Barela November 2020
# MIT License - for Adafruit Industries LLC
# See https://github.com/r-spacex/SpaceX-API for API info

import time
import terminalio
from adafruit_magtag.magtag import MagTag

months = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
USE_24HR_TIME = False
# in seconds, we can refresh about 100 times on a battery
TIME_BETWEEN_REFRESHES = 24 * 60 * 60  # once a day delay

# https://ll.thespacedevs.com/2.2.0/launch/upcoming/?location__ids=12,27

#from adafruit_magtag.magtag import Graphics, Network
#graphics = Graphics(auto_refresh=False)
#display = graphics.display
#graphics.qrcode("http://taogroup.com", qr_size=2, x=240, y=70)
#graphics.display.show(graphics.splash)
#display.refresh()

# Set up data location and fields
DATA_SOURCE = "https://ll.thespacedevs.com/2.2.0/launch/upcoming/?location__ids=12,27"
NAME_LOCATION = ['results', 0, 'name']
DETAIL_LOCATION = ['results', 0, 'mission', 'description']
DATE_LOCATION = ['results', 0, 'net']

# These functions take the JSON data keys and does checks to determine
#   how to display the data. They're used in the add_text blocks below

def mission_transform(val):
    if val == None:
        val = "Unavailable"
    return val

def time_transform(val2):
    print("time_transform: \"" + val2 + "\"")
    if val2 == None:
        return "When: Unavailable"
    month = int(val2[5:7])
    day = int(val2[8:10])
    hour = int(val2[11:13])
    min = int(val2[14:16])

    if USE_24HR_TIME:
        timestring = "%d:%02d" % (hour, min)
    elif hour > 12:
        timestring = "%d:%02d pm" % (hour-12, min)
    else:
        timestring = "%d:%02d am" % (hour, min)

    return "%s %d, at %s" % (months[month-1], day, timestring)

def details_transform(val3):
    if val3 == None or not len(val3):
        return "Details: To Be Determined"
    return "Details: " + val3[0:166] + "..."

# Set up the MagTag with the JSON data parameters
magtag = MagTag(
    url=DATA_SOURCE,
    json_path=(NAME_LOCATION, DATE_LOCATION, DETAIL_LOCATION)
)

magtag.add_text(
    text_font="/fonts/8BitWonder-16.bdf",
    text_position=(10, 15),
    is_data=False
)
# Display heading text below with formatting above
magtag.set_text("Next rocket launch")

# Formatting for the mission text
magtag.add_text(
    text_font="/fonts/Arial-Bold-12.pcf",
    text_position=(10, 38),
    text_transform=mission_transform
)

print("running time transform...")

# Formatting for the launch time text
magtag.add_text(
    text_font="/fonts/Arial-12.bdf",
    text_position=(10, 60),
    text_transform=time_transform
)

print("done running time transform.")

# Formatting for the details text
magtag.add_text(
    text_font=terminalio.FONT,
    text_position=(10, 94),
    line_spacing=0.8,
    text_wrap=47,     # wrap text at this count
    text_transform=details_transform
)

try:
    # Have the MagTag connect to the internet
    magtag.network.connect()
    # This statement gets the JSON data and displays it automagically
    value = magtag.fetch()
    print("Response is", value)
except (ValueError, RuntimeError, ConnectionError, OSError) as e:
    print("Some error occured, retrying! -", e)

# wait 2 seconds for display to complete
time.sleep(2)
magtag.exit_and_deep_sleep(TIME_BETWEEN_REFRESHES)
