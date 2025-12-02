# 创建SparkSession
import json
import sys
from pyspark.sql import SparkSession
from hdfs import InsecureClient
from pyspark import SparkConf, SparkContext

# 获取通过命令行传递的参数
if len(sys.argv) > 1:
    args = sys.argv[1]
else:
    args = None

table_name = args.split("--")[0].strip()
x_name = args.split("--")[1].strip()
y_name = args.split("--")[2].strip()
date = args.split("--")[3].strip()
conf = SparkConf().setAppName(f"{table_name}_{x_name}_{y_name}_value").setMaster("spark://localhost:7077").set("spark.eventLog.enabled", "false")
sc = SparkContext(conf=conf)

# 读取HDFS上的CSV文件
data_rdd = sc.textFile(f"hdfs://localhost:9000/input/{table_name}.csv")


# 获取表头并提取列索引
header = data_rdd.first()
header_columns = header.split(",")
x_index = header_columns.index(x_name)
y_index = header_columns.index(y_name)
status_index = header_columns.index("status") if table_name == "orders" else None

# 过滤数据
if table_name == "orders":
    filtered_rdd = data_rdd.filter(lambda row: row != header and row.split(",")[status_index] in ["已支付", "已发货", "已完成"])
else:
    filtered_rdd = data_rdd.filter(lambda row: row != header)

print(filtered_rdd.collect())  # 查看过滤后的数据
# 处理日期分组
def extract_date(row, date_type):
    cols = row.split(",")
    date_value = cols[x_index]
    if date_type == "date":
        return date_value.split(" ")[0]  # 只取日期部分
    elif date_type == "month":
        return date_value[:7]  # 年-月
    elif date_type == "quarter":
        date_part = date_value.split(" ")[0]  # 提取日期部分（如 "2023-05-15"）
        month = int(date_part[5:7])           # 提取月份并转为整数
        quarter = (month - 1) // 3 + 1        # 计算季度（1-4）
        return f"{date_part[:4]}-Q{quarter}" # 格式化为 "年-Q季"
    elif date_type == "year":
        return date_value[:4]  # 年
    return cols[x_index]

# 生成键值对 (日期值, y值)
result_rdd = (
    filtered_rdd
    .map(lambda row: (extract_date(row, date), float(row.split(",")[y_index]) if row.split(",")[y_index] else 0))
)
print(result_rdd.collect())  # 查看键值对生成结果
# 按键聚合总和
aggregated_rdd = result_rdd.reduceByKey(lambda a, b: a + b)

print(aggregated_rdd.collect())  # 查看聚合结果
# 将结果转换为字典格式


result_dict_rdd = aggregated_rdd.map(lambda x: json.dumps({x_name: x[0], "total": round(x[1], 2)}))

output_path = f"/output/{table_name}/value{x_name}{y_name}{date}"

try:
# 保存结果为 JSON 格式到 HDFS
    hadoop_client = InsecureClient('http://localhost:9870',user="hadoop")
    if hadoop_client.status(output_path, strict=False):
        hadoop_client.delete(output_path, recursive=True)
    result_dict_rdd.saveAsTextFile("hdfs://localhost:9000"+output_path)
except Exception as e:
    print(f"An error occurred: {e}")

sc.stop()
