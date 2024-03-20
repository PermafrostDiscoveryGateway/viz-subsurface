from pathlib import Path
from datetime import datetime
from typing import Union
from pyproj import CRS
from logging import getLogger

def timer(time: Union[datetime, bool]=False) -> Union[datetime, int, float]:
    """
    Start a timer if no argument is supplied, otherwise stop it and report the seconds and minutes elapsed.

    :param time: The directory to create
    :type time: bool or datetime.datetime
    :return: If no time is supplied, return start time; else return elapsed time in seconds and decimal minutes
    :rtype: datetime.datetime or (int, float)
    """
    if not time:
        return datetime.now()
    else:
        time = (datetime.now() - time).seconds
        return time, time/60

def make_dirs(d: Path, exist_ok: bool=True):
    """
    Simple wrapper to create directory using os.makedirs().
    Included is a logging command.

    :param pathlib.Path d: The directory to create
    :param bool exist_ok: Whether to gracefully accept an existing directory (default: True)
    """
    d.mkdir(exist_ok=exist_ok)

def rm_files(files: list[Path]=[]):
    """
    Remove a list of intermediate processing files.

    :param list files: A list `pathlib.Path`s to remove
    """
    for f in files:
        if f.is_file():
            f.unlink()

def write_wkt_to_file(f: Path, wkt: str):
    """
    Write well-known text (WKT) string to file. Will overwrite existing file.

    :param f: File path to write to (wil)
    :type f: pathlib.Path
    :param str wkt: String to write
    """
    if f.is_file():
        f.unlink()
    with open(f, 'w') as fw:
        fw.write(str(wkt))

def read_wkt_from_file(f: Path) -> str:
    """
    Read the WKT string from a file

    :param f: The file to read
    :type f: pathlib.Path
    :return: The well-known text of the CRS in use
    :rtype: str
    """
    with open(f, 'r') as fr:
        return fr.read()

def get_epsgs_from_wkt(wkt: str) -> tuple:
    """
    Use pyproj to parse a well-known text string to CRS. Returns a tuple of
    `[CRS, horizontal EPSG, vertical EPSG, horizontal CRS name, vertical CRS name]`
    where the EPSG fields could be an integer representing an EPSG code or `None`.

    :param str wkt: The well-known text string to parse to pyproj.crs.CRS
    :return: CRS object, horizontal EPSG, vertical EPSG, horizontal name, vertical name
    :rtype: tuple
    """
    L = getLogger(__name__)
    epsg_h, epsg_v = None, None
    h_name, v_name = None, None
    crs = CRS.from_wkt(wkt)
    if crs.is_compound:
        L.info('Found compound coordinate system (COMPD_CS): %s entries' % (len(crs.sub_crs_list)))
        if len(crs.sub_crs_list) > 2: # not sure if this case exists, but should be warned anyway
            L.warning('More than 2 entries in a compound coordinate system may cause an unwanted override!')
        for c in crs.sub_crs_list:
            if c.is_vertical:
                epsg_v = c.to_epsg()
                v_name = c.name
            else:
                epsg_h = c.to_epsg()
                h_name = c.name
    else:
        if crs.is_vertical:
            epsg_v = crs.to_epsg()
            v_name = crs.name
        else:
            epsg_h = crs.to_epsg()
            h_name = crs.name
    if epsg_h:
        L.info('Found horizontal EPSG: %s (%s)' % (epsg_h, h_name))
    if epsg_v:
        L.info('Found vertical EPSG: %s (%s)' % (epsg_v, v_name))
    return crs, epsg_h, epsg_v, h_name, v_name


