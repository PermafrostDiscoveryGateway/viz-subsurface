from pathlib import Path
import argparse
from pyegt.defs import MODEL_LIST, REGIONS

import logging as L
from .pipeline import Pipeline

def cli():
    """
    Parse the command options and arguments.
    """
    parser = argparse.ArgumentParser(prog='pdgsubsurface', description='Convert radar files (currently only GSSI DZT format) to Cesium tilesets.')
    parser.add_argument('-a', '--archive', action='store_true', help='Whether to archive the input dataset')
    parser.add_argument('-z', '--translate_z', type=float, default=0.0, help='Float translation for z values')
    parser.add_argument('-g', '--from_geoid', choices=MODEL_LIST, default=None, help='The geoid, tidal, or geopotential model to translate from')
    parser.add_argument('-r', '--geoid_region', choices=REGIONS, default=REGIONS[0], help='The NGS region (https://vdatum.noaa.gov/docs/services.html#step140)')
    parser.add_argument('-f', '--file', type=str, required=True, help='The file to process')

    args = parser.parse_args()
    p = Path(args.file)
    if not p.is_file():
        L.error('No file at %s' % (p))
        exit(1)

    p = Pipeline(f=args.file,
                 archive=args.archive,
                 translate_z=args.translate_z,
                 from_geoid=args.from_geoid,
                 geoid_region=args.geoid_region)
    p.run()