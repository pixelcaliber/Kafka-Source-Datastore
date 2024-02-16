## Source Collector Application for Kafka Streams to process it

### Part of ETL (Extract-Transform-Load) pipeline
Debezium postgres connector will watch the bin/logs of our database and use Capture Data Change CDC mechanism to watch out for the CRUD operations and deliver them to Kafka Event processor pipeline for processing

Tech-stack: python, flask, debezium, Kafka & postgres 
