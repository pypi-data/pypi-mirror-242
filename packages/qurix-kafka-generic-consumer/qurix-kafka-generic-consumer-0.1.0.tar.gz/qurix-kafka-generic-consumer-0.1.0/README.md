# Generic Consumer

## What is it?

Qurix Kafka Generic Consumer is a Python package designed to simplify the interaction with  Kafka for data engineers and data scientists. This package offers a versatile solution for effortlessly consuming messages from Confluent Kafka within Python applications. At its core is the GenericConsumer class, designed to streamline the process of fetching messages from a specified Kafka topic. This package provides essential features such as offset management, allowing users to set positions within the topic, and seamless integration with the popular pandas library, enabling easy structuring and manipulation of Kafka messages into DataFrames.

## Main Features

Key features of the package include:

1. Flexible Kafka Consumer:
The GenericConsumer class provides a flexible and reusable Kafka consumer for fetching messages from a subscribed topic.

2. Offset Management:
Supports setting offsets for different partitions based on options like earliest, latest, last, or a specific timestamp.

3. Message Reading:
Fetches messages from the subscribed topic, allowing users to specify the number of messages to read.

4. Extended DataFrame:
Provides functionality to extend the DataFrame with header information, making it easier to analyze and work with the data.

5. JSON Data Processing:
Includes a method for processing JSON data within the messages, allowing users to extract and normalize the JSON values into a DataFrame.

6. Clean Resource Management:
Implements proper resource management by closing the Kafka consumer when done, ensuring efficient resource utilization.

7. Configurability:
Users can configure the Kafka consumer by providing a ConsumerConfig object, allowing customization of consumer settings.

8. Logging Support:
Includes logging support at different levels (e.g., INFO, DEBUG) to facilitate debugging and monitoring.

9. PyPI Package Ready:
Designed for easy packaging and distribution on PyPI, making it accessible for others to install and use in their projects.

10. Compatibility:
Compatible with popular Python libraries such as pandas and confluent-kafka.

## Usage Scenarios:
1. Data Ingestion:
Suitable for scenarios where real-time or batch data needs to be ingested from Kafka topics into a DataFrame for analysis.

2. Streaming Data Processing:
Ideal for applications dealing with streaming data, enabling efficient processing and analysis of messages from Kafka.

3.  Event-driven Applications:
Useful in event-driven architectures, where consuming messages from Kafka is a fundamental part of the application's workflow.

4. Data Exploration and Analysis:
Facilitates easy exploration and analysis of Kafka messages using the power of pandas DataFrames.

5. Customization:
Easily adaptable to specific project requirements, allowing users to extend or modify the class according to their needs.

## Requirements

- `confluent-kafka`
- `openpyxl`

You can install these dependencies manually or use the provided `requirement.txt` file in the repository.

## Installation

1. Create a New Virtual Environment (named `.venv` in this case):

```bash
python3 -m venv venv
```

2. Activate the Virtual Environment:

```bash
source venv/bin/activate
```

3. Install the Package:

To install the `qurix-kafka-generic-consumer` package, use `pip`:

```bash
pip install qurix-kafka-generic-consumer
```

## Example

### Generic Consumer

To use the GenericConsumer class, follow these steps:

```python
from qurix.kafka.generic_consumer.consumer import GenericConsumer
from qurix.kafka.generic_consumer.entities.config import ConsumerConfig, Offset

# Create a ConsumerConfig object with your Kafka settings
conf = ConsumerConfig(
    bootstrap_servers="Kafka-Bootstrap-Server",
    group_id="my_consumer_group",
    auto_offset_reset=Offset.EARLIEST.value,
    sasl_password="password",
    sasl_username="username",
    sasl_mechanisms="PLAIN",
    security_protocol="SASL_SSL"
)

# Initialize a GenericConsumer
consumer = GenericConsumer(topic="my_topic", consumer_config=conf)

# Consume messages from the topic
consumer.read_messages()

# Set the offset option to consume messages from a specific point
consumer.set_offset(partition=0, offset_option=Offset.EARLIEST)

# Extend the DataFrame with header
consumer.extend_df_with_header(df=your_df_from_read_messages)

# Extract JSON values from the DataFrame
consumer.extract_json(df, 'column_name')
```

## Contact

For any inquiries or questions, feel free [reach out](https://qurix.tech/about_us.html).
