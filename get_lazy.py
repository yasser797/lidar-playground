import argparse
import subprocess
import json
import geopandas as gpd
from urllib.request import urlopen
import pyproj
import tempfile

CA_PLACE_GPKG = 'data/ca_place.gpkg'

def run_pdal(pipeline):
    with tempfile.NamedTemporaryFile('w', delete=False) as f:
        json.dump({"pipeline": pipeline}, f)
    print(f.name)
    subprocess.run(['pdal', 'pipeline', f.name])

def get_args():
    parser = argparse.ArgumentParser(description='Extract LAZ from EPT')
    parser.add_argument('--uri', required=True, help='path to EPT')

    bounds_group = parser.add_mutually_exclusive_group(required=True)
    bounds_group.add_argument('--bounds', help='bounds for EPT in format '
                              '"([{minx},{maxx}],[{miny},{maxy}])"')
    bounds_group.add_argument('--area',
                              help='shp/gpkg containing area polygons')
    parser.add_argument('--index', help='(optional) index of polygon to use '
                        '(if not provided, all polygons will be used)',
                        type=int)
    bounds_group.add_argument('--city', help='city to get bounds for')

    parser.add_argument('--out', required=True, help='output LAZ path')

    args = parser.parse_args()
    return args

def get_bounds(args):
    if args.bounds:
        bounds = args.bounds
    elif args.area:
        # determine bounds from file
        gdf = gpd.read_file(args.area)
        lidar_crs = get_crs_from_ept(args.uri)
        gdf = gdf.to_crs(lidar_crs)

        if args.index is not None:
            minx, miny, maxx, maxy = gdf.iloc[args.index]['geometry'].bounds
        else:
            minx, miny, maxx, maxy = gdf.total_bounds
        bounds = f'([{minx},{maxx}],[{miny},{maxy}])'
    elif args.city:
        places_gdf = gpd.read_file(CA_PLACE_GPKG).set_index('place_name')
        lidar_crs = get_crs_from_ept(args.uri)
        places_gdf = places_gdf.to_crs(lidar_crs)
        minx, miny, maxx, maxy = \
            places_gdf.loc[args.city.title()]['geometry'].bounds
        bounds = f'([{minx},{maxx}],[{miny},{maxy}])'

    print("bounds:", bounds)
    return bounds

def get_crs_from_ept(uri):
    with urlopen(uri) as f:
        ept = json.loads(f.read().decode('utf-8'))
        return pyproj.CRS(ept['srs']['wkt'])

def main(args):
    bounds = get_bounds(args)
    pipeline = []
    pipeline.append(
        {
            "type": "readers.ept",
            "filename": args.uri, #"https://s3-us-west-2.amazonaws.com/usgs-lidar-public/USGS_LPC_CA_LosAngeles_2016_LAS_2018/ept.json",
            "bounds": bounds, #"([-13194674.4781,-13184336.3701],[4028154.9536,4037117.1952])",
            "tag": "readdata"
        })
    pipeline.append(
        {
            "type": "writers.las",
            "filename": args.out,
            "compression":"lazperf"
        })
    
    print('running pipeline...')

    run_pdal(pipeline)
    
    print('done.') 

if __name__ == '__main__':
    args = get_args()
    main(args)
