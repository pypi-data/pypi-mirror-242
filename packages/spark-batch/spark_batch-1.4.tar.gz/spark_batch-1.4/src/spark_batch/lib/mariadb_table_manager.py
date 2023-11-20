from pyspark.sql import SparkSession
from .pxlogger import CustomLogger
from .util import parseSourceObject
from .util import toCustomSchema

"""
MariaDB  테이블을 로드하고 저장하는 클래스.

사용 예시)
    # MariaDB database connection settings
    connection_url = "jdbc:mariadb://<host>:<port>/<database_name>"
    mariadb_properties = {
        "user": "<username>",
        "password": "<password>",
        "driver": "org.mariadb.jdbc.Driver"
    }
    
    # MariaDBTableManager 초기화
    manager = MariaDBTableManager(spark, connection_url, mariadb_properties)
"""

class MariadbTableManager:
    def __init__(self, spark, connection_url, connection_properties, dbname=None):
        self.spark = spark
        self.connection_url = connection_url
        self.connection_properties = connection_properties
        self.dbname = dbname
        self.logger = CustomLogger("MariaDBTableManager")
    
    def getType(self) :
        return "mariadb"
    
    def getTablePath(self, tableName):
        return tableName if self.dbname is None else self.dbname + "." + tableName
  
    def loadTable(self, tableName, offset=None, chunk_size=100000, dpath=None, customSchema=None):
        self.logger.debug(("loadTable = ", tableName, offset, chunk_size))
        
        target_table = self.getTablePath(tableName)
        self.logger.debug(("target_table = ", target_table))
        
        if offset is None:
            query = f"(SELECT * FROM {target_table}) tbl"
        else:
            query = f"(SELECT * FROM {target_table} LIMIT {chunk_size} OFFSET {offset}) tbl"
        self.logger.debug(("query = ", query))
          
        df = self.spark.read \
            .format("jdbc") \
            .option("url", self.connection_url) \
            .option("dbtable", query) \
            .option("fetchsize", chunk_size) 

        for key, value in self.connection_properties.items():
            df = df.option(key, value)

        if customSchema:
            df = df.schema(toCustomSchema(customSchema)) 

        df = df.load()

        return df
        
    # def saveTable(self, data_frame, mode="append"):
    #     data_frame.write.jdbc(url=self.connection_properties['url'],
    #                           table=self.tableName,
    #                           mode=mode,
    #                           properties=self.connection_properties)

    def loadTables(self, tableNames, dpath=None, customSchemas=None):
        tableNames = parseSourceObject(tableNames)

        if customSchemas is None:
            customSchemas = [None] * len(tableNames)  # 기본적으로 None 스키마를 사용

        dataframes = {}

        for tableName, customSchema in zip(tableNames, customSchemas):
            target_table = self.getTablePath(tableName)

            # JDBC 연결 속성 설정
            properties = self.properties
            if customSchema:
                properties["customSchema"] = customSchema

            # Spark DataFrame 로딩 및 등록
            df = self.spark.read.jdbc(self.connection_url, table=target_table, properties=properties)
            df.createOrReplaceTempView(tableName)
            dataframes[tableName] = df

        return dataframes    

    
    def queryTable(self, query, tableNames=None, dpath=None, customSchemas=None):
        self.logger.debug(("queryTable = ", query, tableNames))

        df = self.spark.read \
            .format("jdbc") \
            .option("url", self.connection_url) \
            .option("query", query) 
        
        for key, value in self.connection_properties.items():
            df = df.option(key, value)

        if customSchemas:
            df = df.schema(toCustomSchema(customSchemas)) 

        df = df.load()

        return df
    