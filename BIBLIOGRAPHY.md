# Bibliography: Code Libraries and Technologies

> A comprehensive reference of libraries, frameworks, and tools sustaining the Tenstorrent Grayskull ERBF implementation repository.

## Table of Contents

1. [Core Mechanics: Neural Networks & AI Frameworks](#1-core-mechanics-neural-networks--ai-frameworks)
2. [Functionality Extensions: Advanced ML Capabilities](#2-functionality-extensions-advanced-ml-capabilities)
3. [Networking: Communication & Data Transfer](#3-networking-communication--data-transfer)
4. [Setup: Environment Management & Dependencies](#4-setup-environment-management--dependencies)
5. [Containerization: Deployment & Isolation](#5-containerization-deployment--isolation)
6. [Deployment: Hardware Interfaces & System Integration](#6-deployment-hardware-interfaces--system-integration)
7. [CI/CD: Automated Pipelines & Quality Assurance](#7-cicd-automated-pipelines--quality-assurance)
8. [Supporting Libraries: Utilities & Infrastructure](#8-supporting-libraries-utilities--infrastructure)

---

## 1. Core Mechanics: Neural Networks & AI Frameworks

### Deep Learning Frameworks

#### PyTorch
- **Version**: 2.1.0+cpu.cxx11.abi
- **Purpose**: Primary deep learning framework for tensor computations, automatic differentiation, and neural network training
- **URL**: https://pytorch.org/
- **Citation**: Paszke, A., Gross, S., Massa, F., et al. (2019). "PyTorch: An Imperative Style, High-Performance Deep Learning Library." *NeurIPS*.
- **Role in ERBF**: Implements cortical network computations, belief update mechanisms, and gradient flow
- **Related Libraries**:
  - `torchvision` (0.16.0+fbb4cc5): Computer vision utilities and models
  - `torchmetrics` (1.7.1): Metrics for model evaluation

#### TensorFlow
- **Version**: 2.13.0 (CPU)
- **Purpose**: Alternative deep learning framework for graph-based computation
- **URL**: https://www.tensorflow.org/
- **Citation**: Abadi, M., Barham, P., Chen, J., et al. (2016). "TensorFlow: A System for Large-Scale Machine Learning." *OSDI*.
- **Role in ERBF**: Model interoperability and alternative computational backend
- **Related Libraries**:
  - `keras` (2.13.1): High-level neural network API
  - `tensorflow-estimator` (2.13.0): High-level API for training models
  - `tensorboard` (2.13.0): Visualization toolkit
  - `tf2onnx` (1.15.1): TensorFlow to ONNX model conversion

#### JAX
- **Version**: 0.4.13
- **Purpose**: High-performance array computing with automatic differentiation
- **URL**: https://github.com/google/jax
- **Citation**: Bradbury, J., Frostig, R., Hawkins, P., et al. (2018). "JAX: Composable transformations of Python+NumPy programs."
- **Role in ERBF**: Functional programming approach to neural computations, optimized for hardware acceleration
- **Related Libraries**:
  - `jaxlib` (0.4.11): JAX backend runtime
  - `flax` (0.6.0): Neural network library built on JAX
  - `optax` (0.1.7): Gradient processing and optimization library
  - `chex` (0.1.6): Utilities for JAX code reliability

#### Apache MXNet
- **Version**: 1.9.1
- **Purpose**: Flexible and efficient deep learning framework
- **URL**: https://mxnet.apache.org/
- **Citation**: Chen, T., Li, M., Li, Y., et al. (2015). "MXNet: A Flexible and Efficient Machine Learning Library for Heterogeneous Distributed Systems." *arXiv*.
- **Role in ERBF**: Additional framework support for model compatibility

#### Apache TVM
- **Version**: 0.14.0+dev.tt.dfda3826c (Tenstorrent fork)
- **Purpose**: Deep learning compiler stack for optimizing models across hardware backends
- **URL**: https://tvm.apache.org/
- **Citation**: Chen, T., Moreau, T., Jiang, Z., et al. (2018). "TVM: An Automated End-to-End Optimizing Compiler for Deep Learning." *OSDI*.
- **Role in ERBF**: Critical for compiling ERBF models to Tenstorrent Grayskull hardware primitives

### Tenstorrent-Specific Frameworks

#### PyBuda
- **Version**: 0.1.240401+dev.gs.c7ce1e7
- **Purpose**: Tenstorrent's Python-based unified development architecture
- **URL**: https://github.com/tenstorrent/tt-buda
- **Documentation**: https://docs.tenstorrent.com/pybuda/
- **Role in ERBF**: Primary framework for mapping neural networks to Tensix cores, managing NoC communication, and orchestrating SFPU operations
- **Key Features**:
  - Automatic tensor tiling for L1 SRAM (32×32 tiles)
  - NoC routing configuration
  - SFPU kernel generation
  - Multi-chip orchestration

#### PyLuwen
- **Version**: 0.7.1
- **Purpose**: Low-level Python interface to Tenstorrent hardware
- **URL**: https://github.com/tenstorrent/tt-luwen
- **Role in ERBF**: Direct hardware access for diagnostics and low-level control

#### TT-SMI
- **Version**: 3.0.12
- **Purpose**: Tenstorrent System Management Interface
- **Role in ERBF**: Hardware monitoring, telemetry, and system diagnostics

#### TT-Tools-Common
- **Version**: 1.4.14
- **Purpose**: Common utilities for Tenstorrent toolchain
- **Role in ERBF**: Shared infrastructure for hardware tooling

### Model Interchange Formats

#### ONNX
- **Version**: 1.15.0
- **Purpose**: Open Neural Network Exchange format
- **URL**: https://onnx.ai/
- **Citation**: "ONNX: Open Neural Network Exchange." Linux Foundation AI & Data.
- **Role in ERBF**: Model portability between frameworks
- **Related Libraries**:
  - `onnxruntime` (1.16.3): Inference engine for ONNX models
  - `tf2onnx` (1.15.1): TensorFlow to ONNX converter

### Numerical Computing Core

#### NumPy
- **Version**: 1.23.1
- **Purpose**: Fundamental package for array computing in Python
- **URL**: https://numpy.org/
- **Citation**: Harris, C.R., Millman, K.J., et al. (2020). "Array programming with NumPy." *Nature*.
- **Role in ERBF**: Foundation for all tensor operations and numerical computations

#### SciPy
- **Version**: 1.8.0
- **Purpose**: Scientific computing library (optimization, linear algebra, integration)
- **URL**: https://scipy.org/
- **Citation**: Virtanen, P., Gommers, R., et al. (2020). "SciPy 1.0: fundamental algorithms for scientific computing in Python." *Nature Methods*.
- **Role in ERBF**: Advanced mathematical operations for belief update computations

---

## 2. Functionality Extensions: Advanced ML Capabilities

### Transformer Architectures

#### Transformers (Hugging Face)
- **Version**: 4.35.2
- **Purpose**: State-of-the-art natural language processing models
- **URL**: https://huggingface.co/transformers/
- **Citation**: Wolf, T., Debut, L., et al. (2020). "Transformers: State-of-the-Art Natural Language Processing." *EMNLP*.
- **Role in ERBF**: Attention mechanism implementations applicable to ERBF's Φ (attention) component
- **Related Libraries**:
  - `tokenizers` (0.15.2): Fast tokenization for text processing
  - `huggingface-hub` (0.30.2): Model repository access

### Computer Vision

#### Ultralytics
- **Version**: 8.0.145
- **Purpose**: YOLO (You Only Look Once) object detection framework
- **URL**: https://ultralytics.com/
- **Role in ERBF**: Vision applications mapping to cortical hierarchy (V1 → IT pathway)

#### OpenCV
- **Versions**:
  - `opencv-python` (4.11.0.86): Full OpenCV with GUI
  - `opencv-python-headless` (4.6.0.66): Headless version for servers
- **Purpose**: Computer vision and image processing
- **URL**: https://opencv.org/
- **Role in ERBF**: Preprocessing visual stimuli for cortical network input

### Optimization & Hyperparameter Tuning

#### Optuna
- **Version**: 3.6.2
- **Purpose**: Automated hyperparameter optimization framework
- **URL**: https://optuna.org/
- **Citation**: Akiba, T., Sano, S., et al. (2019). "Optuna: A Next-generation Hyperparameter Optimization Framework." *KDD*.
- **Role in ERBF**: Optimizing belief update parameters, attention weights, and network architecture

#### PyTorch Optimizer
- **Version**: 2.12.0
- **Purpose**: Collection of optimization algorithms for PyTorch
- **URL**: https://github.com/kozistr/pytorch_optimizer
- **Role in ERBF**: Advanced optimizers for training ERBF networks

### Time Series & Forecasting

#### PyTorch Forecasting
- **Version**: 1.0.0
- **Purpose**: Time series forecasting with deep learning
- **URL**: https://pytorch-forecasting.readthedocs.io/
- **Role in ERBF**: Temporal dynamics in belief propagation

#### Statsmodels
- **Version**: 0.14.4
- **Purpose**: Statistical modeling and hypothesis testing
- **URL**: https://www.statsmodels.org/
- **Role in ERBF**: Probabilistic inference and statistical analysis of belief distributions

### Lightning Framework

#### PyTorch Lightning
- **Version**: 2.5.1
- **Purpose**: High-level PyTorch wrapper for research and production
- **URL**: https://lightning.ai/
- **Citation**: Falcon, W., et al. (2019). "PyTorch Lightning."
- **Role in ERBF**: Structured training loops, distributed training, and experiment management
- **Related Libraries**:
  - `lightning` (2.5.1): Unified Lightning framework
  - `lightning-utilities` (0.14.3): Utilities for Lightning ecosystem

---

## 3. Networking: Communication & Data Transfer

### Asynchronous I/O

#### aiohttp
- **Version**: 3.11.16
- **Purpose**: Asynchronous HTTP client/server framework
- **URL**: https://docs.aiohttp.org/
- **Role in ERBF**: Asynchronous communication for distributed multi-chip setups
- **Related Libraries**:
  - `aiohappyeyeballs` (2.6.1): Fast connection establishment
  - `aiosignal` (1.3.2): Signal management for asyncio
  - `async-timeout` (5.0.1): Timeout utilities

### Network Protocol Support

#### Requests
- **Version**: 2.28.2
- **Purpose**: HTTP library for Python
- **URL**: https://requests.readthedocs.io/
- **Role in ERBF**: API communication and data retrieval
- **Related Libraries**:
  - `urllib3` (1.26.14): HTTP client backend
  - `certifi` (2025.1.31): SSL certificate bundle

### Inter-Chip Communication

#### PyZMQ
- **Version**: 26.4.0
- **Purpose**: Python bindings for ZeroMQ messaging library
- **URL**: https://zeromq.org/languages/python/
- **Role in ERBF**: Message passing for multi-chip Ethernet mesh coordination

#### gRPC
- **Version**: 1.71.0
- **Purpose**: High-performance RPC framework
- **URL**: https://grpc.io/
- **Role in ERBF**: Efficient inter-process communication for distributed ERBF deployments

### Network-on-Chip (NoC) Abstraction

**Note**: Tenstorrent's 2D NoC is hardware-implemented and controlled through PyBuda's routing configuration. Software libraries provide abstraction layers for:
- Packet routing tables
- DMA configuration
- Ring buffer management
- Credit-based flow control

---

## 4. Setup: Environment Management & Dependencies

### Package Management

#### Conda/Mamba
- **Purpose**: Cross-platform package and environment manager
- **URL**: https://docs.conda.io/
- **Role in ERBF**: Primary environment management (see `diagnostics/python_environment.yaml`)

#### pip
- **Version**: 24.0
- **Purpose**: Python package installer
- **URL**: https://pip.pypa.io/
- **Role in ERBF**: Secondary package management for PyPI packages

### Development Tools

#### Pre-commit
- **Version**: 3.5.0
- **Purpose**: Git hook framework for code quality checks
- **URL**: https://pre-commit.com/
- **Role in ERBF**: Automated code formatting and linting before commits
- **Related Libraries**:
  - `identify` (2.6.9): File type identification
  - `nodeenv` (1.9.1): Node.js environment management
  - `cfgv` (3.4.0): Configuration file validation

#### virtualenv
- **Version**: 20.30.0
- **Purpose**: Virtual Python environment creator
- **URL**: https://virtualenv.pypa.io/
- **Role in ERBF**: Isolated Python environments

### Configuration Management

#### PyYAML
- **Version**: 6.0.2
- **Purpose**: YAML parser and emitter
- **URL**: https://pyyaml.org/
- **Role in ERBF**: Configuration file management (environment specs, routing tables)

#### RapidYAML
- **Version**: 0.9.0
- **Purpose**: Fast YAML parser written in C++
- **Role in ERBF**: High-performance configuration parsing

### File Utilities

#### fsspec
- **Version**: 2025.3.2
- **Purpose**: Filesystem abstraction for Python
- **URL**: https://filesystem-spec.readthedocs.io/
- **Role in ERBF**: Unified interface for file operations across storage backends

---

## 5. Containerization: Deployment & Isolation

### Docker (Recommended for Future Use)

**Status**: Not currently implemented in repository

**Recommended Technologies**:

#### Docker
- **Purpose**: Container platform for application packaging
- **URL**: https://www.docker.com/
- **Proposed Role**: Isolate ERBF runtime environment with all dependencies
- **Typical Dockerfile Structure**:
  ```dockerfile
  FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04
  # Install Tenstorrent drivers and PyBuda
  # Copy ERBF implementation
  # Configure Conda environment
  ```

#### Docker Compose
- **Purpose**: Multi-container orchestration
- **URL**: https://docs.docker.com/compose/
- **Proposed Role**: Coordinate multi-chip ERBF deployments across containers

#### Singularity/Apptainer
- **Purpose**: Container platform for HPC environments
- **URL**: https://apptainer.org/
- **Proposed Role**: HPC-friendly containerization for research clusters

### Alternative: Conda Environments

**Current Approach**: Using Conda/Mamba for environment isolation
- **File**: `diagnostics/python_environment.yaml`
- **Advantages**: Simpler than Docker, good for development
- **Limitations**: Less isolation than containers, OS-dependent

---

## 6. Deployment: Hardware Interfaces & System Integration

### PCIe Communication

#### Tenstorrent Kernel Module (tt_kmd)
- **Purpose**: Linux kernel driver for PCIe communication with Grayskull
- **Documentation**: Tenstorrent software stack
- **Role in ERBF**: Direct memory access (DMA) to/from host DRAM

### System Diagnostics

#### psutil
- **Version**: 5.9.6
- **Purpose**: Cross-platform system and process utilities
- **URL**: https://psutil.readthedocs.io/
- **Role in ERBF**: System resource monitoring in diagnostic tool (`tt_diagnostic.py`)

#### py-cpuinfo
- **Version**: 9.0.0
- **Purpose**: CPU information gathering
- **Role in ERBF**: Hardware capability detection

#### pyelftools
- **Version**: 0.32
- **Purpose**: ELF (Executable and Linkable Format) file parsing
- **URL**: https://github.com/eliben/pyelftools
- **Role in ERBF**: Analyzing binary formats for kernel modules

### Hardware Monitoring

#### Loguru
- **Version**: 0.5.3
- **Purpose**: Simplified Python logging
- **URL**: https://loguru.readthedocs.io/
- **Role in ERBF**: Runtime logging and debugging

#### Coloredlogs
- **Version**: 15.0.1
- **Purpose**: Colored terminal output for logs
- **Role in ERBF**: Enhanced diagnostic output readability

### Profiling & Performance

#### Pyinstrument
- **Version**: 4.1.1
- **Purpose**: Statistical Python profiler
- **URL**: https://pyinstrument.readthedocs.io/
- **Role in ERBF**: Performance analysis of belief update computations

### Binary Format Support

#### FlatBuffers
- **Version**: 23.5.26
- **Purpose**: Memory-efficient serialization library
- **URL**: https://flatbuffers.dev/
- **Role in ERBF**: Efficient data serialization for hardware communication

---

## 7. CI/CD: Automated Pipelines & Quality Assurance

### Testing Frameworks

#### pytest (Recommended)
- **Status**: Not explicitly listed but commonly used with pre-commit
- **Purpose**: Python testing framework
- **URL**: https://pytest.org/
- **Proposed Role**: Unit and integration testing for ERBF components

#### Coverage
- **Version**: 7.8.0
- **Purpose**: Code coverage measurement
- **URL**: https://coverage.readthedocs.io/
- **Role in ERBF**: Ensuring comprehensive test coverage

### Code Quality

#### Pre-commit Hooks
- **Version**: 3.5.0
- **Configuration File**: `.pre-commit-config.yaml` (to be created)
- **Typical Checks**:
  - Code formatting (black, isort)
  - Linting (flake8, pylint)
  - Type checking (mypy)
  - YAML validation
  - Security scanning (bandit)

### GitHub Actions (Recommended)

**Status**: Not currently implemented

**Proposed Workflows**:

#### 1. Continuous Integration
```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    - Run pytest
    - Check code coverage
    - Validate documentation
```

#### 2. Documentation Build
```yaml
# .github/workflows/docs.yml
name: Documentation
on: [push]
jobs:
  build:
    - Render Mermaid diagrams
    - Generate API docs
    - Deploy to GitHub Pages
```

#### 3. Hardware Validation
```yaml
# .github/workflows/hardware.yml
name: Hardware Tests
on: [push]
jobs:
  validate:
    - Run diagnostic tool
    - Check Tenstorrent device status
    - Validate PCIe configuration
```

### Alternative CI/CD Platforms

#### GitLab CI/CD
- **URL**: https://docs.gitlab.com/ee/ci/
- **Proposed Role**: Alternative to GitHub Actions for private deployments

#### Jenkins
- **URL**: https://www.jenkins.io/
- **Proposed Role**: Self-hosted CI/CD for organizations with existing infrastructure

---

## 8. Supporting Libraries: Utilities & Infrastructure

### Data Processing

#### Pandas
- **Version**: 1.5.3
- **Purpose**: Data manipulation and analysis
- **URL**: https://pandas.pydata.org/
- **Citation**: McKinney, W. (2010). "Data Structures for Statistical Computing in Python." *SciPy*.
- **Role in ERBF**: Time series data handling, belief state tracking

#### PyArrow
- **Version**: 19.0.1
- **Purpose**: Apache Arrow Python bindings
- **URL**: https://arrow.apache.org/docs/python/
- **Role in ERBF**: High-performance columnar data interchange

#### Datasets (Hugging Face)
- **Version**: 2.3.2
- **Purpose**: Dataset loading and processing
- **Role in ERBF**: Efficient dataset management for training

### Visualization

#### Matplotlib
- **Version**: 3.5.1
- **Purpose**: Comprehensive plotting library
- **URL**: https://matplotlib.org/
- **Citation**: Hunter, J.D. (2007). "Matplotlib: A 2D Graphics Environment." *Computing in Science & Engineering*.
- **Role in ERBF**: Visualizing belief distributions, attention maps
- **Related Libraries**:
  - `cycler` (0.12.1): Color cycling for plots
  - `fonttools` (4.57.0): Font manipulation

#### Seaborn
- **Version**: 0.13.2
- **Purpose**: Statistical data visualization
- **URL**: https://seaborn.pydata.org/
- **Role in ERBF**: High-level statistical plots for analysis

#### Graphviz
- **Version**: 0.8.4
- **Purpose**: Graph visualization
- **URL**: https://graphviz.org/
- **Role in ERBF**: Visualizing cortical network topology

### Text Processing

#### Markdown
- **Version**: 3.8
- **Purpose**: Markdown to HTML converter
- **Role in ERBF**: Documentation processing

#### Markdown-it-py
- **Version**: 3.0.0
- **Purpose**: Fast Markdown parser
- **Role in ERBF**: Enhanced Markdown rendering
- **Related Libraries**:
  - `mdit-py-plugins` (0.4.2): Plugins for markdown-it-py
  - `linkify-it-py` (2.0.3): Link recognition

#### Pygments
- **Version**: 2.19.1
- **Purpose**: Syntax highlighting
- **URL**: https://pygments.org/
- **Role in ERBF**: Code highlighting in documentation

#### Rich
- **Version**: 11.2.0
- **Purpose**: Rich text formatting in terminal
- **URL**: https://rich.readthedocs.io/
- **Role in ERBF**: Enhanced console output

#### Textual
- **Version**: 0.59.0
- **Purpose**: TUI (Text User Interface) framework
- **URL**: https://textual.textualize.io/
- **Role in ERBF**: Interactive diagnostic interfaces

### String Matching & Fuzzy Search

#### FuzzyWuzzy
- **Version**: 0.18.0
- **Purpose**: Fuzzy string matching
- **Role in ERBF**: Name matching in hardware device detection

#### Levenshtein
- **Versions**:
  - `Levenshtein` (0.27.1)
  - `python-Levenshtein` (0.27.1)
- **Purpose**: Fast Levenshtein distance computation
- **Role in ERBF**: String similarity metrics

#### RapidFuzz
- **Version**: 3.13.0
- **Purpose**: Fast string matching library
- **Role in ERBF**: Efficient fuzzy matching

### Database & Search

#### Elasticsearch
- **Version**: 8.11.0
- **Purpose**: Distributed search and analytics engine
- **URL**: https://www.elastic.co/elasticsearch/
- **Role in ERBF**: Logging and telemetry aggregation
- **Related Libraries**:
  - `elastic-transport` (8.17.1): Transport layer for Elasticsearch

#### SQLAlchemy
- **Version**: 2.0.24
- **Purpose**: SQL toolkit and ORM
- **URL**: https://www.sqlalchemy.org/
- **Role in ERBF**: Database abstraction for experiment tracking
- **Related Libraries**:
  - `alembic` (1.14.1): Database migration tool
  - `greenlet` (3.1.1): Lightweight concurrency

### Serialization & Data Formats

#### Protocol Buffers
- **Version**: 3.20.3
- **Purpose**: Language-neutral data serialization
- **URL**: https://protobuf.dev/
- **Role in ERBF**: Efficient model serialization

#### Safetensors
- **Version**: 0.5.3
- **Purpose**: Safe tensor serialization format
- **URL**: https://github.com/huggingface/safetensors
- **Role in ERBF**: Secure model weight storage

#### MessagePack
- **Version**: 1.1.0
- **Purpose**: Binary serialization format
- **URL**: https://msgpack.org/
- **Role in ERBF**: Compact data interchange

#### xxHash
- **Version**: 3.5.0
- **Purpose**: Fast hashing algorithm
- **Role in ERBF**: Data integrity checks

### Authentication & Security

#### Google Auth
- **Version**: 2.38.0
- **Purpose**: Google authentication library
- **Related Libraries**:
  - `google-auth-oauthlib` (1.0.0): OAuth 2.0 integration
  - `oauthlib` (3.2.2): OAuth implementation
  - `requests-oauthlib` (2.0.0): OAuth for Requests

### Template Engines

#### Jinja2
- **Version**: 3.1.6
- **Purpose**: Modern templating engine
- **URL**: https://jinja.palletsprojects.com/
- **Role in ERBF**: Code generation templates for kernel operations

#### Mako
- **Version**: 1.3.10
- **Purpose**: Fast Python templating
- **Role in ERBF**: Alternative templating for code generation

### Utilities

#### tqdm
- **Version**: 4.66.3
- **Purpose**: Progress bar library
- **URL**: https://tqdm.github.io/
- **Role in ERBF**: Training progress visualization

#### tabulate
- **Version**: 0.9.0
- **Purpose**: Pretty-print tabular data
- **Role in ERBF**: Formatting diagnostic output

#### PrettyTable
- **Version**: 3.0.0
- **Purpose**: ASCII table generation
- **Role in ERBF**: Console table formatting

#### docopt
- **Version**: 0.6.2
- **Purpose**: Command-line argument parsing
- **Role in ERBF**: CLI utilities

---

## Additional References

### Research Papers

#### ERBF Theoretical Foundations

1. **Predictive Coding**
   - Rao, R.P. & Ballard, D.H. (1999). "Predictive coding in the visual cortex: a functional interpretation of some extra-classical receptive-field effects." *Nature Neuroscience*.

2. **Variational Inference**
   - Friston, K. (2010). "The free-energy principle: a unified brain theory?" *Nature Reviews Neuroscience*.

3. **Graph Neural Networks**
   - Scarselli, F., Gori, M., et al. (2009). "The Graph Neural Network Model." *IEEE Transactions on Neural Networks*.

4. **Attention Mechanisms**
   - Vaswani, A., Shazeer, N., et al. (2017). "Attention Is All You Need." *NeurIPS*.

#### Hardware Architecture

1. **Network-on-Chip**
   - Dally, W.J. & Towles, B. (2001). "Route packets, not wires: on-chip interconnection networks." *DAC*.

2. **AI Accelerators**
   - Jouppi, N.P., Young, C., et al. (2017). "In-datacenter performance analysis of a tensor processing unit." *ISCA*.

3. **Specialized Computing**
   - Hennessy, J.L. & Patterson, D.A. (2019). "A New Golden Age for Computer Architecture." *Communications of the ACM*.

### Official Documentation

1. **Tenstorrent Resources**
   - Grayskull Architecture Guide: https://tenstorrent.com/hardware/grayskull
   - PyBuda Documentation: https://docs.tenstorrent.com/pybuda/
   - TT-Metalium (Low-level framework): https://github.com/tenstorrent/tt-metal

2. **Python Ecosystem**
   - Python 3.10 Documentation: https://docs.python.org/3.10/
   - Conda User Guide: https://docs.conda.io/projects/conda/en/latest/user-guide/

3. **Community Resources**
   - Tenstorrent Discord: https://discord.gg/tenstorrent
   - GitHub Discussions: https://github.com/tenstorrent/tt-buda/discussions

---

## Version Information

**Document Version**: 1.0.0
**Last Updated**: 2025-01-15
**Python Version**: 3.10.13
**Environment**: See `diagnostics/python_environment.yaml` for complete dependency tree

---

## Citation for This Repository

If you use this repository in your research, please cite:

```bibtex
@misc{tenstorrent_greyskull_erbf,
  title={Tenstorrent Grayskull: ERBF Hardware Acceleration},
  author={Calisota.ai},
  year={2025},
  publisher={GitHub},
  url={https://github.com/danindiana/tenstorrent_greyskull},
  note={Evidence-based Relational Belief Feedback implementation on Tenstorrent Grayskull AI accelerator hardware}
}
```

---

## Contributing to This Bibliography

To add or update entries:

1. Follow the existing format (Name, Version, Purpose, URL, Citation, Role)
2. Place entries in appropriate categories
3. Include version numbers from `python_environment.yaml`
4. Add official documentation links where available
5. Submit pull request with clear description

---

**License**: This bibliography is part of the Tenstorrent Grayskull ERBF repository and is subject to the same license terms (Calisota.ai Public Software License, Version 1.0).
