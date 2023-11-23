from spark_extension.lib.pxlogger import CustomLogger
import geopandas as gpd
from shapely.geometry import Point
from pyproj import Transformer
import os

class GeoDataProcessor(object):

    def __init__(self, shp_file_path=None, dbf_file_path=None):
        self.logger = CustomLogger("GeoDataProcessor")

        # 좌표계 정의
        self.epsg5186 = Transformer.from_crs("epsg:5186", "epsg:4326", always_xy=True)
        self.wgs84 = Transformer.from_crs("epsg:4326", "epsg:5186", always_xy=True)

        pwd = os.path.dirname(os.path.abspath(__file__))
        if shp_file_path is None :
            shp_file_path = os.path.join(pwd, "../shp/BML_HADM_AS.shp")
        if dbf_file_path is None : 
            dbf_file_path = os.path.join(pwd, "../shp/BML_HADM_AS.dbf")

        # 데이터 로드
        self.load_data(shp_file_path, dbf_file_path)

    def load_data(self, shp_file_path, dbf_file_path):
        # SHP 파일과 DBF 파일 읽기
        self.gdf = gpd.read_file(shp_file_path)
        df_dbf = gpd.read_file(dbf_file_path)
        self.logger.debug(("Base Geo: ", self.gdf.crs))

        # 동 정보를 가진 DBF 파일과 SHP 파일을 조인
        self.merged_gdf = self.gdf.merge(df_dbf, left_index=True, right_index=True, how='left',
                                         suffixes=('_left', '_right'))
        self.logger.debug(("Columns: ", self.merged_gdf.columns))


    # XY 좌표를 동 이름으로 변환하는 함수
    def epsg5186_to_dong(self, lon, lat):
        point = Point(lon, lat) 
        dong = None
        try: 
        #nearest_row = merged_gdf.iloc[(merged_gdf['geometry_left'].distance(Point(longitude, latitude))).idxmin()]
            nearest_row = self.merged_gdf.iloc[(self.merged_gdf['geometry_left'].apply(lambda geom: point.distance(geom))).idxmin()]
            if not nearest_row['geometry_left'].contains(point):
                raise ValueError("Error: 해당 좌표에 대응하는 지오메트리가 없습니다.")
            dong = nearest_row['HJD_NAM_left']  # 'FTR_CDE_left'는 동 정보를 가리키는 열의 이름으로 수정
        except ValueError:
            dong = None # print("Error: 해당 좌표에 대응하는 지오메트리가 없습니다.") 
        return dong

    def wsg84_to_dong(self, lon, lat):
        x, y = self.wsg84_transform(lon, lat) # WSG84 > 
        self.logger.debug(f"wsg84({lon}, {lat}) > epsg5186({x}, {y})")
        return self.epsg5186_to_dong(x, y)

    def wsg84_transform(self, lon, lat):
        x, y = self.wgs84.transform(lon, lat) 
        return x, y

    def epsg5186_transform(self, lon, lat):
        x, y = self.epsg5186.transform(lon, lat)
        return x, y


    def print_test(self):
        seoul = (126.9784, 37.5665)
        dong = self.wsg84_to_dong(*seoul)
        print(f"The dong is: {dong}")

        dong = self.wsg84_to_dong(126.771, 37.512)
        print(f"The dong is: {dong}")

        dong = self.wsg84_to_dong(126.770701, 37.542777)
        print(f"The dong is: {dong}")     
        

    def print_shp(self):        
        print(f"Coordinate Data: ")
        size = len(self.gdf['geometry'].centroid.x.iloc[:])
        for i in range(0, size):
            lon = self.gdf['geometry'].centroid.x.iloc[i]
            lat = self.gdf['geometry'].centroid.y.iloc[i]
            dong = self.epsg5186_to_dong(lon, lat)

            x, y = self.epsg5186_transform(lon, lat)
            print(f"  {dong} ({lon}, {lat}), ({x}, {y})")

    def test(self):
        # 사용 예제
        shp_file_path = "geodata/shp/BML_HADM_AS.shp"
        dbf_file_path = "geodata/shp/BML_HADM_AS.dbf"

        geo_processor = GeoDataProcessor(shp_file_path, dbf_file_path)
        geo_processor.print_test()
        geo_processor.print_shp()


