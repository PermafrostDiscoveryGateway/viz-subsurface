from typing import Union, Literal
from pyproj import CRS, Transformer
from logging import getLogger

from pyegt.height import HeightModel
from pyegt.utils import model_search

def use_model(user_vrs: Union[str, Literal[None]]=None,
               las_vrs: Union[str, Literal[None]]=None, # overrides user_vrs.
               # consequently implies we trust file headers;
               # this is done to support projects with multiple CRS
               # and to enforce correct CRS info in database
               ) -> str:
    """
    Get the geoid, tidal, or geopotential model
    in order to calculate ellipsoid height.
    The following figure demonstrates the difference between geoid, ellipsoid,
    and topographic ground surface:

    .. figure:: https://user-images.githubusercontent.com/18689918/239385604-5b5dd0df-e2fb-4ea9-90e7-575287a069e6.png
        :align: center

        Diagram showing conceptual model of ellipsoid height ``h``, geoid
        height ``H``, and height of geoid relative to ellipsoid ``N``
        along with topographic surface (grey).

    Ellipsoidal height (``h``) is generally used in global projections such as
    Cesium due to its small digital footprint and ease of calculation relative
    to systems based on gravity or geopotential height. However, the earth and
    tides are influenced by local differences in gravitational pull and other
    factors. Therefore some engineering projects and local reference systems
    use height referenced to a geoid or tidal model (``H``) which provides a much
    easier framework to understand height relative to, for example, modeled
    mean sea level or sea level potential. Converting from ``H`` to ``h``
    requires knowing the height difference between the geoid and the ellipsoid
    (``N``).
    Conversion is then a simple addition of these values (``H + N = h``).

    .. note::

        ``las_vrs`` is set by file headers and overrides ``user_vrs``.
        This implicitly means we trust file headers over user input.
        We do this to support projects with multiple VRS (i.e. `user_vrs`
        values are used solely to fill in gaps where headers do not explicitly
        specify a vertical reference system). It is also meant to enforce the
        accuracy of VRS information in file headers.

        If a project should need to set or change VRS information prior to
        uploading to the database, they are encouraged to do so through the
        use of third-party software such as
        `LASTools <https://github.com/LAStools/LAStools>`_.

        The 9 possible input scenarios and their outcomes::

            # 1. matched las_vrs / matched user_vrs -> las_vrs
            # 2. matched las_vrs / unmatched user_vrs -> las_vrs
            # 3. matched las_vrs / empty user_vrs -> las_vrs
            # 4. empty las_vrs / empty user_vrs -> 0
            # 5. empty las_vrs / matched user_vrs -> user_vrs
            # 6. empty las_vrs / unmatched user_vrs -> exit(1)
            # 7. unmatched las_vrs / empty user_vrs -> exit(1)
            # 8. unmatched las_vrs / matched user_vrs -> exit(1) # maybe in the future we have a geoid_override setting where this will execute
            # 9. unmatched las_vrs / unmatched user_vrs -> exit(1)


    :param user_vrs: The user-specified geoid model to convert from if none is found in the file header
    :return: The model name to use for lookup
    :rtype: str
    """
    L = getLogger(__name__)
    vrs = None
    L.debug(f'user_vrs={user_vrs}, las_vrs={las_vrs}')
    if las_vrs:
        # override user value with detected VRS
        vrs = model_search(las_vrs)
        L.debug(f'after model_search(las_vrs): vrs={vrs}')
        if user_vrs and vrs:
            # scenarios 1 and 2
            L.info('User value of "%s" will be overridden by detected VRS "%s"' % (user_vrs, vrs))
        if user_vrs and (not vrs):
            # scenarios 8 and 9
            L.error('No vertical reference system matching "%s" found' % (user_vrs))
            exit(1)
        if not user_vrs:
            # scenario 3
            pass
        if (not user_vrs) and (not vrs):
            # scenario 7
            L.error('No vertical reference system matching "%s" found' % (las_vrs))
    else:
        if not user_vrs:
            # scenario 4
            return 0
        else:
            vrs = model_search(user_vrs)
            L.debug(f'after model_search(user_vrs): vrs={vrs}')
            if vrs:
                # scenario 5
                L.info('VRS found: %s (user-specified)' % (vrs))
            else:
                # scenario 6
                L.error('Could not find VRS matching value "%s"' % (user_vrs))
                exit(1)
    return vrs

def crs_to_wgs84(x: Union[str, int, float], y: Union[str, int, float], from_crs: Union[CRS, int, str]):
    """
    Convert grid coordinates to cartographic (lat/lon) in order to use the
    :py:class:`pyegt.height.HeightModel` API lookup.

    :param x: The X-coordinate to convert to longitude
    :type x: str or int or float
    :param y: The Y-coordinate to convert to latitude
    :type y: str or int or float
    :param from_crs: The projected coordinate reference system to convert from
    :type from_crs: pyproj.crs.CRS or int or str
    :return: The lat and long position equivalent to the X and Y position in the input CRS
    :rtype: tuple(float, float)
    """
    if type(from_crs) == int:
        crs = CRS.from_epsg(from_crs)
    elif type(from_crs) == CRS:
        crs = from_crs
    elif type(from_crs) == str:
        if "AUTHORITY" in from_crs:
            crs = CRS.from_wkt(from_crs)
        else:
            crs = CRS.from_string(from_crs)
    wgs84 = CRS.from_epsg(4326)
    t = Transformer.from_crs(crs_from=crs, crs_to=wgs84)
    return t.transform(xx=float(x), yy=float(y))

def get_adjustment(lat: float, lon: float, model=str, region=str):
    """
    Get the modeled height of a specified location and a specified geoid or
    tidal model from :py:class:`pyegt.height.HeightModel`.

    :param float lat: Decimal latitude
    :param float lon: Decimal longitude
    :param str model: The geoid or tidal model to query the height of
    :param str region: The geoid or tidal region (for options, see :py:data:`pyegt.defs.REGION`)
    :return: The ellipsoid height of the given geoid model at the given location
    :rtype: pyegt.height.HeightModel
    """
    return HeightModel(lat=lat, lon=lon, from_model=model, region=region)
