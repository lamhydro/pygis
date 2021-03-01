from osgeo import ogr
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


def createPolygon(coords):          
    """
    Create a ogr geometry
    """
    ring = ogr.Geometry(ogr.wkbLinearRing)
    for coord in coords:
        ring.AddPoint(coord[0], coord[1])

    # Create polygon
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)
    return poly.ExportToWkt()

def writeShapefile(poly, out_shp):
    """
    Write the polygon into a shpfile and save the file.
    """
    # Now convert it to a shapefile with OGR    
    driver = ogr.GetDriverByName('Esri Shapefile')
    ds = driver.CreateDataSource(out_shp)
    layer = ds.CreateLayer('', None, ogr.wkbPolygon)
    # Add one attribute
    layer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
    defn = layer.GetLayerDefn()

    ## If there are multiple geometries, put the "for" loop here

    # Create a new feature (attribute and geometry)
    feat = ogr.Feature(defn)
    feat.SetField('id', 123)

    # Make a geometry, from Shapely object
    geom = ogr.CreateGeometryFromWkt(poly)
    feat.SetGeometry(geom)

    layer.CreateFeature(feat)
    feat = geom = None  # destroy these

    # Save and close everything
    ds = layer = feat = geom = None

def plotPolygon(coords):
    """
    Plot polygon location
    """

    # setup Lambert Conformal basemap.
    # set resolution=None to skip processing of boundary datasets.
    m = Basemap(width=12000000,height=9000000,projection='lcc',
            resolution=None,lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)
    m.bluemarble()
    plt.show()

def main(coords, out_shp):
    poly = createPolygon(coords)
    plotPolygon(coords)
    writeShapefile(poly, out_shp)

if __name__ == "__main__":
    coords = [(-123.11, 49.25), (-123.10,49.25), (-123.10,49.26), (-123.11,49.26), (-123.11, 49.25)]
    out_shp = 'polygon.shp'
    main(coords, out_shp)
