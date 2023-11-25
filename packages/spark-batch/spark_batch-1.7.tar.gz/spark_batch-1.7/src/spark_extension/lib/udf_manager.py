from pyspark.sql import SparkSession
from pyspark.sql.types import StringType
from pyspark.sql.functions import udf
from pyspark.sql import functions as F

class UDFManager:
    def __init__(self, spark):
        self.spark = spark
        self.registered_udfs = {}

    def register(self, name, func, return_type):
        udf = F.udf(func, return_type)
        self.registered_udfs[name] = udf
        self.spark.udf.register(name, udf)
        return udf

    def get_udf(self, name):
        return self.registered_udfs.get(name, None)

    
    def test():
        from spark_extension.lib.udf_manager import UDFManager
        from spark_extension.lib.aes_cipher import AESCipher
        from pyspark.sql.types import StringType

        # Initialize Spark session
        spark = SparkSession.builder.appName("udf").getOrCreate()

        # Create an instance of the AESCipher class
        aes_cipher = AESCipher("BCParkingWeb2022BCParkingWeb2022", "BCParkingWeb2022")

        # Create an instance of the UDFManager
        udf_manager = UDFManager(spark)

        # Register UDFs for AESCipher
        udf_manager.register("udf_encrypt", aes_cipher.encrypt, StringType())
        udf_manager.register("udf_decrypt", aes_cipher.decrypt, StringType())
        udf_manager.register("toCarNumber", aes_cipher.decrypt_nopading, StringType())


        # Sample DataFrame with a 'data' column
        data = [("Hello, World!",)]
        columns = ["data"]
        df = spark.createDataFrame(data, columns)
        df.createOrReplaceTempView("tmp_table")

        # Use the registered UDFs in a Spark SQL query
        result = spark.sql("SELECT data, udf_encrypt(data) AS encrypted_data, udf_decrypt(udf_encrypt(data)) AS decrypted_data FROM tmp_table")
        result.show()


        # Sample DataFrame with a 'data' column
        data = [("30AN2+xpbvqAktXEEiY00Q==",)]
        columns = ["data"]
        df = spark.createDataFrame(data, columns)
        df.createOrReplaceTempView("tmp_table")

        # Use the registered UDFs in a Spark SQL query
        result = spark.sql("SELECT data, toCarNumber(data) AS car_no FROM tmp_table")
        result.show()
