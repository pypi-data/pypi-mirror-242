# KafkaObserver

## What is it?

The KafkaObserver package provides a set of tools for observing and retrieving information about  Kafka topics and consumer groups. It facilitates monitoring and managing Kafka infrastructure by offering insights into offset statuses, watermarks, and retention policies.

## Main Features

- **Watermark Information:** Retrieve information about the watermark (low and high offsets) for a specified topic.

- **Retention Policy Information:** Retrieve information about the retention policy (time and size) for a specified topic.

- **Topic Information:** Obtain details about Kafka topics, including basic information and extended details like watermark information and retention policies.

- **Consumer Groups Information:** Retrieve information about existing consumer groups.

- **Offset Status:** Get the offset status (current, committed, etc.) for a specific consumer and topic. Plot the offset status for visualization.


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

To install the `qurix-kafka-observer` package, use `pip`:

```bash
pip install qurix-kafka-observer
```

## Usage

### Kafka Observer

To use the KafkaObserver class:

```python
from qurix.kafka.observer import KafkaObserver
from qurix.kafka.entities.config import ConsumerConfig

# Create a ConsumerConfig object with your Kafka settings
BOOTSTRAP_SERVERS = "localhost:9092"
consumer_config = ConsumerConfig(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    # ...
)

observer = KafkaObserver(consumer_config)

# Get consumer groups
observer.get_consumer_groups()

# Get consumer groups with offsets
observer.get_consumer_groups_offsets()

from confluent_kafka import Consumer

my_consumer = Consumer({"bootstrap.servers": BOOTSTRAP_SERVERS, "group.id": "your_consumer_group"})

# Get offset status
observer.get_offset_status(my_consumer, "some_topic")
```

The observer has also the possibility to plot important water mark and offset information for a certain topic:

```python
# Plot offset status
observer.plot_offset_status(my_consumer, "some_topic")


## Contact

For any inquiries or questions, feel free [reach out](https://qurix.tech/about_us.html).
