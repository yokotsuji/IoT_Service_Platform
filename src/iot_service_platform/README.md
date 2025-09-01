# iot_service_platform

`iot_service_platform` is available on AWS Lambda.
This directory contains the core implementation, including standardized interfaces and adapters for sensors, actuators, and complex services.

## Requirements

The Lambda function requires the following Python packages:

- `requests`

Add them to a `requirements.txt` file:


## Platform Structure

- `lambda_function.py`  
  Entry point for the AWS Lambda function (handler).

- `actuator/`  
  Standardized actuator interface and concrete adapters for device control.

- `sensorservice/`  
  Standardized sensor interface and adapters for fetching sensor data.

- `complexservice/`  
  Standardized interface and adapters for composite services  
  (e.g., temperature difference, comfort).

- `api/`  
  Request handling layer (parsing, routing, and response formatting for API Gateway).

- `manager/`  
  Schedulers and runners for periodic web-service tasks and maintenance jobs.

- `utils/`  
  Shared utilities.


