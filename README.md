# IoT_Service_Platform


This repository provides an implementation of an **IoT service platform** and an **LLM-based agent** for evaluating and supporting intelligent IoT service selection.  
The project focuses on enabling interoperability between heterogeneous IoT devices and providing standardized interfaces for both atomic and complex IoT services.  
By combining these services with Large Language Models (LLMs), the platform allows agents to interpret natural language queries and select appropriate IoT services effectively.

# Usage

1. Agent Response

You can get Agent Response from src/Agent/main.py. Agent directory simply enables us to acquire Agent response.

2. Service Select Evaluation

You can evaluate service selection of LLM Agent uasing Platform from src/serviceselect/eval.sh. Detailed usage is described in src/serviceselect/README.txt. This evaluation doesn't include Agent response and tool use.

3. Code Line Evaluation
You can evaluate code lines with src/code_line/simulate_atomic.py and src/code_line/simulate_complex.py.
## Repository Structure

```text
├── data/                 # Ground-truth datasets for evaluation
├── src/
│   ├── servicesselect/   # evaluate service selection
│   ├── code_line/        # evaluate code lines
│   ├── iot_service_platform/ # IoT platform code (Lambda functions, adapters, etc.)
│   └── Agent/            # LLM-based agent implementation and evaluation
└── README.md             # Project overview (this file)


