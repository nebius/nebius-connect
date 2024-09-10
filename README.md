# Nebius AI connector for Apache Spark™

The [Managed Service for Apache Spark](https://nebius.ai/services/managed-spark), a [Nebius AI](https://nebius.ai/) service, offers access to _sessions:_ managed environments that can handle multiple independent ad-hoc computations at the same time. 

With this connector, you can connect to your Managed Spark sessions using [Spark Connect](https://spark.apache.org/docs/latest/spark-connect-overview.html) and process data with Spark APIs from your machine.

## Installing

```bash
pip install nebius-connect
```

## Example

```py
from pyspark.sql.connect.session import SparkSession
from nebius.spark.connect import create_channel_builder

nebius_spark_cb = create_channel_builder(
    'spsession-example123.nebius.cloud:443',
    password='my-password'
)

spark = SparkSession \
    .builder \
    .channelBuilder(nebius_spark_cb) \
    .getOrCreate()

columns = ["id","name"]
data = [(1,"Sarah"),(2,"Maria")]
df = spark.createDataFrame(data).toDF(*columns)
df.show()
spark.stop()
```

## License

Copyright 2024 Nebius B.V.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

_Apache and [Apache Spark](http://spark.apache.org/) are either registered trademarks or trademarks of the Apache Software Foundation in the United States and/or other countries._
