# LLM-Agent Directory Structure

This repository contains the implementation of an LLM-based agent for IoT service selection and evaluation.  
The directory is organized as follows:
## Overview

- **Agent.py**: Defines the LLM-based agent logic.  
- **Memory.py**: Stores and retrieves conversation history.  
- **Prompt.py**: Provides structured prompts to guide the agent’s reasoning.  
- **Tools.py**: Contains implementations of IoT tools when using the platform.  
- **each_Tools.py**: Implements IoT tools for the non-platform setting.  
- **evaluation.py**: Evaluates the accuracy of service selection with the platform.  
- **main.py**: Entry point for running the agent.  
- **normalize.py**: Normalizes prediction outputs for consistent evaluation.  
- **service_select_evaluation_without_platform.py**: Evaluates service selection without the platform.  
- **serviceselect_with_iotplatform.py**: Runs service selection with platform support.  
- **serviceselect_without_iotplatform.py**: Runs service selection without platform support.

