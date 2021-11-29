"""
This is a simple PySpark3 set-up using a single Spark app
with no cluster. Ideal for POCs and quick implementations of
the PySpark service.
"""
from pyspark import SparkContext
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as f
from pyspark.sql import types as t


def single_node_cluster() -> None:
    """
    Simply gather total monetary sales for the products per line-item
    :return:
    """
    sc: SparkContext = SparkContext.getOrCreate()
    spark: SparkSession = SparkSession(sc)

    data_frame: DataFrame = spark.read.option("mode", "DROPMALFORMED").json("data/MOCK_DATA.json")
    data_frame = data_frame \
        .withColumn("currency", f.col("sale_price").substr(0, 1)) \
        .withColumn("sale_price", f.regexp_replace(f.col("sale_price"), "\\$", "").cast(t.DoubleType()))
    data_frame = data_frame \
        .withColumn("total_sales", f.round(f.col("sale_price") * f.col("sale_quantity"), 2)) \
        .orderBy("sale_date", "product_code")

    data_frame.show()


if __name__ == '__main__':
    single_node_cluster()
