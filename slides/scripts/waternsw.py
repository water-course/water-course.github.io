"""Minimal client for the WaterNSW Hydstra ("real time data") web service.

WaterNSW publishes continuous river data for every gauge in the New South Wales
part of the Murray-Darling Basin. There is no key and no registration. This
module is deliberately small: one function to call the service, one to pull a
time series.

Two things about this API cost an afternoon if you do not know them.

1. The service wants the WHOLE JSON request as the URL query string. The usual
   ``params=<json>`` form returns ``error_num 120``, "Missing top-level version
   item", which reads like a malformed request but is really the wrong
   transport.
2. Different functions demand different API versions. ``get_ts_traces`` is
   version 2; ``get_site_list`` and ``get_variable_list`` are version 1, and
   sending 2 to them is a hard error.

Useful Hydstra variable numbers:

===========  =====================================================
``100.00``   stream water level (stage), metres
``141.00``   discharge, megalitres per day
``10.00``    rainfall, millimetres
===========  =====================================================

A discharge series is requested as ``varfrom="100.00", varto="141.00"``, which
asks the server to convert stage to discharge through the gauge's own rating
curve. That is the same inference the runoff lecture describes: what the
instrument records is stage, and discharge is derived from it.

Unit note used throughout the course: one megalitre spread over one square
kilometre is exactly one millimetre of depth (1 ML = 1000 m^3, 1 km^2 = 1e6
m^2, so 1000/1e6 m = 1 mm). Discharge in ML/day divided by catchment area in
km^2 is therefore a runoff depth in mm/day, with no conversion factor.
"""

import json
import math
import urllib.parse
import urllib.request
from datetime import datetime

BASE = "https://realtimedata.waternsw.com.au/cgi/webservice.exe?"

# Hydstra quality codes at or above 200 flag data the agency does not stand
# behind (estimated, or beyond the rated range). Missing values additionally
# come back as a large negative sentinel rather than as null.
BAD_QUALITY = 200
MISSING_SENTINEL = -1e5


def call(function, params, version="2", timeout=120):
    """Call one Hydstra function and return its decoded ``return`` payload.

    Parameters
    ----------
    function : str
        Hydstra function name, for example ``"get_ts_traces"``.
    params : dict
        The function's own parameters, passed straight through.
    version : str
        API version. ``"2"`` for ``get_ts_traces``, ``"1"`` for the site and
        variable listing functions.
    timeout : int
        Socket timeout in seconds. Long records over an hourly interval are
        slow, so this is generous.

    Raises
    ------
    RuntimeError
        If the service reports a non-zero ``error_num``. The message is passed
        through unchanged, because Hydstra's errors are specific and worth
        reading.
    """
    request = {"function": function, "version": version, "params": params}
    # The entire JSON document is the query string. See the module docstring.
    url = BASE + urllib.parse.quote(json.dumps(request))
    raw = urllib.request.urlopen(url, timeout=timeout).read().decode()
    document = json.loads(raw)
    if document.get("error_num"):
        raise RuntimeError(f"{function}: {document.get('error_msg')}")
    return document["return"]


def trace(site, start, end, interval="hour", varfrom="100.00", varto="141.00",
          data_type="mean"):
    """Pull one time series as a list of ``(datetime, value)`` pairs.

    Parameters
    ----------
    site : str
        AWRC gauge number, for example ``"410057"``.
    start, end : str
        Dates as ``YYYYMMDD``. Both bounds are inclusive.
    interval : str
        ``"hour"``, ``"day"``, and so on.
    varfrom, varto : str
        Source and target variable. Stage to discharge is the default.
    data_type : str
        ``"mean"`` for a rate such as discharge, ``"tot"`` for an accumulation
        such as rainfall. Using ``"mean"`` on rainfall silently returns an
        average intensity rather than a depth, which is the wrong quantity for
        a storm total.

    Returns
    -------
    list of (datetime, float)
        Values the agency has flagged as missing or unreliable come back as
        ``nan`` rather than being dropped, so that gaps stay visible in a plot
        and cannot be integrated over by accident.
    """
    params = {
        "site_list": site,
        "start_time": start + "000000",
        "end_time": end + "000000",
        "varfrom": varfrom,
        "varto": varto,
        "interval": interval,
        "datasource": "A",          # "A" is the archived, quality-coded record
        "data_type": data_type,
        "multiplier": "1",
    }
    points = call("get_ts_traces", params)["traces"][0].get("trace", [])
    series = []
    for point in points:
        value = float(point["v"])
        if value < MISSING_SENTINEL or int(point["q"]) >= BAD_QUALITY:
            value = math.nan
        series.append((datetime.strptime(str(point["t"]), "%Y%m%d%H%M%S"), value))
    return series
