# Tenstorrent Grayskull: Build, Validation & CI/CD Pipeline

> Bare metal setup, validation, and continuous integration infrastructure for Tenstorrent Grayskull AI accelerator development.

## Overview

This repository provides infrastructure for building, validating, and deploying workloads on Tenstorrent Grayskull AI accelerator hardware. It includes bare metal setup procedures, diagnostic tools, smoke tests, and CI/CD pipeline configurations.

**Status**: Private development repository
**Hardware Target**: Tenstorrent Grayskull (e75/e150/e300)
**Primary Use**: Development, validation, and testing infrastructure

---

## Table of Contents

- [Quick Start](#quick-start)
- [Hardware Requirements](#hardware-requirements)
- [Bare Metal Setup](#bare-metal-setup)
- [Build Environment](#build-environment)
- [Validation & Smoke Tests](#validation--smoke-tests)
- [CI/CD Pipeline](#cicd-pipeline)
- [Troubleshooting](#troubleshooting)
- [Documentation Archive](#documentation-archive)

---

## Quick Start

### Prerequisites Checklist

```bash
# Check system compatibility
uname -r                    # Linux kernel 4.15+
lscpu | grep -E "avx|sse"  # x86_64 with AVX support
free -h                     # 32GB+ RAM recommended
lspci | grep Tenstorrent    # Grayskull device detected
```

### 5-Minute Smoke Test

```bash
# 1. Clone repository
git clone https://github.com/danindiana/tenstorrent_greyskull.git
cd tenstorrent_greyskull

# 2. Run hardware diagnostic
cd diagnostics
conda env create -f python_environment.yaml
conda activate tenstorrent-diag
python tt_diagnostic.py

# 3. Review results
cat tenstorrent_diagnostic.json
```

---

## Hardware Requirements

### Minimum System Specifications

| Component | Requirement | Notes |
|-----------|-------------|-------|
| **CPU** | x86_64 (Intel/AMD) | AVX2 support recommended |
| **RAM** | 32 GB | 64 GB for multi-chip setups |
| **PCIe** | Gen 3.0 x16 slot | Gen 4.0 x16 optimal |
| **OS** | Ubuntu 20.04/22.04 | Kernel 4.15+ |
| **Storage** | 100 GB SSD | For software stack + datasets |
| **Power** | 75W per card | Verify PSU capacity |

### Tenstorrent Grayskull Variants

| Model | Tensix Cores | DRAM | TDP | Use Case |
|-------|--------------|------|-----|----------|
| **e75** | 120 (10x12) | 8 GB LPDDR4 | 75W | Single-chip development |
| **e150** | 240 (2x e75) | 16 GB | 150W | Multi-chip inference |
| **e300** | 480 (4x e75) | 32 GB | 300W | Training/large models |

### Verified Platforms

- **Supermicro**: X11/X12 series workstations
- **Dell**: Precision 7920/7960 tower
- **HP**: Z8/Z6 G4 workstations
- **Custom builds**: ATX motherboards with PCIe 3.0/4.0 support

---

## Bare Metal Setup

### 1. Hardware Installation

#### Physical Installation

```bash
# 1. Power down system completely
sudo shutdown -h now

# 2. Install Grayskull card in PCIe x16 slot
#    - Use slot closest to CPU for best performance
#    - Ensure card is fully seated with retention bracket secured
#    - Connect auxiliary power if required (e75 typically doesn't need it)

# 3. Power on and verify detection
lspci | grep -i tenstorrent
# Expected output: XX:00.0 Processing accelerators: Tenstorrent Inc Device XXXX
```

#### BIOS Configuration

Required BIOS settings:

```
1. Enable IOMMU/VT-d (Intel) or AMD-Vi (AMD)
   - Intel: Advanced > Integrated IO > Intel VT for Directed I/O > Enabled
   - AMD: AMD CBS > NBIO > IOMMU > Enabled

2. Set PCIe to Gen 3.0 or Gen 4.0 (not Auto)
   - Advanced > PCI Subsystem Settings > PCI Express Speed > Gen3/Gen4

3. Enable Above 4G Decoding (for large PCIe BARs)
   - Advanced > PCI Subsystem > Above 4G Decoding > Enabled

4. Disable Secure Boot (if using custom kernel modules)
   - Boot > Secure Boot > Disabled

5. Set PCIe ASPM to Disabled
   - Advanced > PCIe Configuration > ASPM Support > Disabled
```

### 2. Operating System Configuration

#### Install Ubuntu 20.04 LTS / 22.04 LTS

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y \
    build-essential \
    linux-headers-$(uname -r) \
    dkms \
    git \
    wget \
    curl \
    pciutils \
    vim \
    htop \
    python3-pip \
    python3-dev
```

#### Configure Kernel Parameters

```bash
# Edit GRUB configuration
sudo vim /etc/default/grub

# Add/modify GRUB_CMDLINE_LINUX_DEFAULT:
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash intel_iommu=on iommu=pt hugepagesz=1G hugepages=16 default_hugepagesz=1G"

# For AMD systems, use:
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash amd_iommu=on iommu=pt hugepagesz=1G hugepages=16 default_hugepagesz=1G"

# Update GRUB
sudo update-grub

# Reboot
sudo reboot
```

#### Verify Kernel Configuration

```bash
# Check IOMMU
dmesg | grep -i iommu
# Expected: DMAR: IOMMU enabled (Intel) or AMD-Vi: IOMMU enabled (AMD)

# Check hugepages
cat /proc/meminfo | grep Huge
# Expected: HugePages_Total: 16

# Verify PCIe link speed
sudo lspci -vvv -s $(lspci | grep Tenstorrent | cut -d' ' -f1) | grep LnkSta
# Expected: Speed 8GT/s (Gen3) or 16GT/s (Gen4), Width x16
```

### 3. Tenstorrent Driver Installation

#### Install Kernel Module (tt_kmd)

```bash
# Clone Tenstorrent kernel module repository
git clone https://github.com/tenstorrent/tt-kmd.git
cd tt-kmd

# Build and install
make
sudo make install

# Load module
sudo modprobe tenstorrent

# Verify module loaded
lsmod | grep tenstorrent
# Expected: tenstorrent    XXXXX  0

# Make persistent across reboots
echo "tenstorrent" | sudo tee -a /etc/modules

# Verify device nodes
ls -l /dev/tenstorrent/
# Expected: crw-rw-rw- 1 root root ... /dev/tenstorrent/0
```

#### Set Device Permissions

```bash
# Create udev rule for non-root access
sudo tee /etc/udev/rules.d/99-tenstorrent.rules <<EOF
KERNEL=="tenstorrent/*", MODE="0666"
EOF

# Reload udev rules
sudo udevadm control --reload-rules
sudo udevadm trigger

# Verify permissions
ls -l /dev/tenstorrent/
```

---

## Build Environment

### 1. Install Miniconda/Mamba

```bash
# Download Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Install
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3

# Initialize
$HOME/miniconda3/bin/conda init bash
source ~/.bashrc

# Optional: Install Mamba (faster than conda)
conda install -n base -c conda-forge mamba -y
```

### 2. Create Development Environment

#### Using Provided Environment File

```bash
# Navigate to repository
cd tenstorrent_greyskull/diagnostics

# Create environment from YAML
conda env create -f python_environment.yaml

# Activate environment
conda activate tenstorrent-diag

# Verify installation
python --version  # Should show Python 3.10.13
pip list | grep -E "pybuda|torch|jax"
```

#### Manual Environment Setup (Alternative)

```bash
# Create new environment
conda create -n tt-dev python=3.10 -y
conda activate tt-dev

# Install PyTorch (CPU version for compatibility)
pip install torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cpu

# Install Tenstorrent software stack
pip install pybuda pyluwen tt-smi tt-tools-common

# Install development tools
pip install pytest pytest-cov black flake8 mypy pre-commit

# Install additional dependencies
pip install numpy scipy pandas matplotlib seaborn jupyterlab
```

### 3. Install Tenstorrent Software Stack

#### PyBuda Installation

```bash
# Install from Tenstorrent repository
pip install pybuda --extra-index-url https://pypi.tenstorrent.com/packages

# Verify installation
python -c "import pybuda; print(pybuda.__version__)"

# Expected output: 0.1.XXXXXX+dev.gs.XXXXXXX
```

#### TT-Metalium (Low-Level Framework)

```bash
# Clone TT-Metal repository
git clone https://github.com/tenstorrent/tt-metal.git
cd tt-metal

# Set environment variables
export ARCH_NAME=grayskull
export TT_METAL_HOME=$(pwd)

# Build
./build_metal.sh

# Run smoke test
./build/test/tt_metal/unit_tests_common
```

### 4. Set Environment Variables

```bash
# Add to ~/.bashrc or ~/.bash_profile
cat >> ~/.bashrc <<EOF

# Tenstorrent Environment
export TT_METAL_HOME=\$HOME/tt-metal
export ARCH_NAME=grayskull
export PYTHONPATH=\$TT_METAL_HOME:\$PYTHONPATH
export LD_LIBRARY_PATH=\$TT_METAL_HOME/build/lib:\$LD_LIBRARY_PATH

# Performance tuning
export OMP_NUM_THREADS=16
export TT_BACKEND_TIMEOUT=300

EOF

# Reload
source ~/.bashrc
```

---

## Validation & Smoke Tests

### 1. Hardware Diagnostic Tool

#### Run Full Diagnostic

```bash
cd diagnostics
conda activate tenstorrent-diag

# Run diagnostic (generates JSON output)
python tt_diagnostic.py

# View results
cat tenstorrent_diagnostic.json | python -m json.tool

# Generate YAML output (optional)
python tt_diagnostic.py --output-format yaml
```

#### Diagnostic Checks

The diagnostic tool validates:

- **System Information**: Hostname, kernel version, CPU, memory, OS
- **PCIe Devices**: Enumeration and Tenstorrent device detection
- **PCIe Link Status**: Speed, width, link degradation
- **Kernel Modules**: tt_kmd/tenstorrent module loaded
- **IOMMU Status**: Intel VT-d or AMD-Vi enabled
- **Hugepages**: 1GB hugepages configured
- **Device Access**: /dev/tenstorrent/* permissions

#### Expected Output (Healthy System)

```json
{
  "timestamp": "2025-01-15T12:34:56",
  "system": {
    "hostname": "tt-workstation",
    "kernel": "5.15.0-94-generic",
    "cpu": "Intel(R) Xeon(R) W-2245 CPU @ 3.90GHz",
    "memory_gb": 64.0,
    "os": "Ubuntu 22.04.3 LTS"
  },
  "tenstorrent_devices": [
    {
      "bus_id": "0000:65:00.0",
      "device_name": "Tenstorrent Grayskull",
      "link_speed": "8.0 GT/s (Gen 3)",
      "link_width": "x16",
      "status": "OK"
    }
  ],
  "kernel_modules": {
    "tenstorrent": "loaded"
  },
  "iommu": "enabled",
  "hugepages_1gb": 16,
  "recommendations": []
}
```

### 2. PyBuda Smoke Tests

#### Test 1: Device Detection

```python
# test_device_detection.py
import pybuda

# Detect Grayskull devices
devices = pybuda.detect_available_devices()
print(f"Detected {len(devices)} Tenstorrent device(s)")

for i, device in enumerate(devices):
    print(f"Device {i}: {device}")

# Expected output:
# Detected 1 Tenstorrent device(s)
# Device 0: Grayskull (ARCH_NAME=grayskull, ID=0)
```

#### Test 2: Simple Tensor Operation

```python
# test_tensor_op.py
import torch
import pybuda

# Create simple PyTorch model
class SimpleAdd(torch.nn.Module):
    def forward(self, x, y):
        return x + y

# Compile for Grayskull
model = SimpleAdd()
compiler = pybuda.PyBudaModule("simple_add", model)

# Create input tensors
x = torch.randn(1, 32, 32)
y = torch.randn(1, 32, 32)

# Run on device
result = compiler(x, y)
print(f"Result shape: {result.shape}")
print("✓ Tensor operation successful")
```

#### Test 3: SFPU Operations

```python
# test_sfpu.py
import torch
import pybuda

class SFPUTest(torch.nn.Module):
    def forward(self, x):
        # Test special functions (run on SFPU)
        return torch.sigmoid(torch.exp(x))

model = SFPUTest()
compiler = pybuda.PyBudaModule("sfpu_test", model)

x = torch.randn(1, 64, 64)
result = compiler(x)
print("✓ SFPU operations successful")
```

### 3. TT-Metal Unit Tests

```bash
cd $TT_METAL_HOME

# Run core unit tests
./build/test/tt_metal/unit_tests_common

# Run DRAM tests
./build/test/tt_metal/unit_tests_dram

# Run NoC tests
./build/test/tt_metal/test_noc

# Run all tests
./tests/scripts/run_tests.sh
```

### 4. Performance Benchmarks

#### Memory Bandwidth Test

```bash
cd $TT_METAL_HOME/tests/tt_metal/perf_microbenchmark

# DRAM read bandwidth
./test_dram_read

# L1 read bandwidth
./test_l1_read

# Expected results:
# DRAM read: ~20-30 GB/s per core
# L1 read: ~200-400 GB/s per core
```

#### NoC Bandwidth Test

```bash
# Test NoC0 bandwidth
./test_noc_unicast

# Expected: ~100-200 GB/s aggregate NoC bandwidth
```

### 5. Automated Smoke Test Script

```bash
#!/bin/bash
# smoke_test.sh

set -e

echo "=== Tenstorrent Grayskull Smoke Test ==="

echo "[1/6] Checking hardware detection..."
lspci | grep Tenstorrent || (echo "❌ Hardware not detected" && exit 1)
echo "✓ Hardware detected"

echo "[2/6] Checking kernel module..."
lsmod | grep tenstorrent || (echo "❌ Kernel module not loaded" && exit 1)
echo "✓ Kernel module loaded"

echo "[3/6] Checking device nodes..."
ls /dev/tenstorrent/0 || (echo "❌ Device node missing" && exit 1)
echo "✓ Device nodes present"

echo "[4/6] Running diagnostic tool..."
cd diagnostics
python tt_diagnostic.py || (echo "❌ Diagnostic failed" && exit 1)
echo "✓ Diagnostic passed"

echo "[5/6] Testing PyBuda import..."
python -c "import pybuda; print(f'PyBuda {pybuda.__version__}')" || (echo "❌ PyBuda import failed" && exit 1)
echo "✓ PyBuda import successful"

echo "[6/6] Running basic inference..."
python test_device_detection.py || (echo "❌ Device detection failed" && exit 1)
echo "✓ Device detection passed"

echo ""
echo "=== All smoke tests passed ✓ ==="
```

---

## CI/CD Pipeline

### 1. Pre-commit Hooks

#### Install and Configure

```bash
# Install pre-commit
pip install pre-commit

# Create configuration
cat > .pre-commit-config.yaml <<EOF
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
        args: ['--maxkb=10000']
      - id: mixed-line-ending

  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.10

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=120', '--ignore=E203,W503']

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ['--profile', 'black']

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
EOF

# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

### 2. GitHub Actions Workflows

#### CI Workflow: Hardware Validation

```yaml
# .github/workflows/hardware-ci.yml
name: Hardware CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  diagnostic:
    runs-on: [self-hosted, tenstorrent]

    steps:
    - uses: actions/checkout@v4

    - name: Setup Conda
      uses: conda-incubator/setup-miniconda@v3
      with:
        environment-file: diagnostics/python_environment.yaml
        activate-environment: tenstorrent-diag

    - name: Run Hardware Diagnostic
      run: |
        cd diagnostics
        python tt_diagnostic.py

    - name: Upload Diagnostic Report
      uses: actions/upload-artifact@v4
      with:
        name: diagnostic-report
        path: diagnostics/tenstorrent_diagnostic.json

    - name: Verify Device Status
      run: |
        python -c "
        import json
        with open('diagnostics/tenstorrent_diagnostic.json') as f:
            data = json.load(f)
            assert len(data['tenstorrent_devices']) > 0, 'No devices detected'
            assert data['kernel_modules']['tenstorrent'] == 'loaded'
        "

  smoke-tests:
    runs-on: [self-hosted, tenstorrent]
    needs: diagnostic

    steps:
    - uses: actions/checkout@v4

    - name: Run Smoke Tests
      run: |
        bash smoke_test.sh

    - name: PyBuda Version Check
      run: |
        python -c "import pybuda; print(pybuda.__version__)"
```

#### Code Quality Workflow

```yaml
# .github/workflows/code-quality.yml
name: Code Quality

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        pip install black flake8 mypy isort

    - name: Run Black
      run: black --check .

    - name: Run Flake8
      run: flake8 . --max-line-length=120

    - name: Run MyPy
      run: mypy . --ignore-missing-imports
```

#### Documentation Build

```yaml
# .github/workflows/docs.yml
name: Documentation

on:
  push:
    branches: [ main ]

jobs:
  build-docs:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Validate Markdown
      uses: gaurav-nelson/github-action-markdown-link-check@v1

    - name: Check Mermaid Diagrams
      run: |
        npm install -g @mermaid-js/mermaid-cli
        find . -name "*.md" -exec sh -c 'grep -q "```mermaid" {} && echo {}' \;
```

### 3. Self-Hosted Runner Setup

#### Configure GitHub Runner on Hardware

```bash
# On machine with Tenstorrent hardware:

# Download runner
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.311.0.tar.gz -L \
  https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz
tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz

# Configure (requires repo token from GitHub)
./config.sh --url https://github.com/danindiana/tenstorrent_greyskull \
  --token YOUR_TOKEN_HERE \
  --labels tenstorrent,grayskull,bare-metal

# Install as service
sudo ./svc.sh install
sudo ./svc.sh start

# Verify
sudo ./svc.sh status
```

### 4. Continuous Deployment

#### Artifact Management

```yaml
# .github/workflows/release.yml
name: Release Build

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: [self-hosted, tenstorrent]

    steps:
    - uses: actions/checkout@v4

    - name: Build Package
      run: |
        python setup.py sdist bdist_wheel

    - name: Create Release
      uses: softprops/action-gh-release@v1
      with:
        files: dist/*
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## Troubleshooting

### Common Issues

#### 1. Device Not Detected

**Symptoms**: `lspci` doesn't show Tenstorrent device

**Solutions**:
```bash
# Check physical connection
sudo lspci -vvv | grep -i pci
# Look for "Empty slot" or link down messages

# Reseat card
sudo shutdown -h now
# Remove and reinsert card
# Power on

# Check BIOS PCIe settings
# Ensure slot is enabled and set to Gen3/Gen4
```

#### 2. Kernel Module Fails to Load

**Symptoms**: `modprobe tenstorrent` fails

**Solutions**:
```bash
# Check dmesg for errors
sudo dmesg | tail -50

# Rebuild module
cd tt-kmd
make clean
make
sudo make install

# Check for kernel version mismatch
uname -r
ls /lib/modules/$(uname -r)/build  # Should exist

# Install kernel headers if missing
sudo apt install linux-headers-$(uname -r)
```

#### 3. PCIe Link Degradation

**Symptoms**: Link running at x8 or x4 instead of x16

**Solutions**:
```bash
# Check current link status
sudo lspci -vvv -s $(lspci | grep Tenstorrent | cut -d' ' -f1) | grep -E "LnkCap|LnkSta"

# LnkCap shows maximum capability
# LnkSta shows current status

# Common causes:
# - Card in x8 physical slot (check motherboard manual)
# - Bifurcation enabled in BIOS (disable if not needed)
# - Physical damage to PCIe connector
# - Other cards consuming PCIe lanes

# Solution: Move to primary x16 slot closest to CPU
```

#### 4. IOMMU Issues

**Symptoms**: DMA errors in dmesg

**Solutions**:
```bash
# Check IOMMU status
dmesg | grep -i iommu

# If not enabled, add to kernel parameters:
sudo vim /etc/default/grub
# Intel: intel_iommu=on iommu=pt
# AMD: amd_iommu=on iommu=pt

sudo update-grub
sudo reboot

# Verify
cat /proc/cmdline | grep iommu
```

#### 5. Hugepages Not Configured

**Symptoms**: Poor performance, memory allocation errors

**Solutions**:
```bash
# Check current configuration
cat /proc/meminfo | grep Huge

# Configure 1GB hugepages
sudo vim /etc/default/grub
# Add: hugepagesz=1G hugepages=16 default_hugepagesz=1G

sudo update-grub
sudo reboot

# Verify
cat /proc/meminfo | grep "HugePages_Total"
# Should show: HugePages_Total:      16
```

#### 6. PyBuda Import Errors

**Symptoms**: `ImportError: No module named 'pybuda'`

**Solutions**:
```bash
# Verify conda environment
conda env list
conda activate tenstorrent-diag

# Reinstall PyBuda
pip uninstall pybuda
pip install pybuda --extra-index-url https://pypi.tenstorrent.com/packages

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Verify installation
pip show pybuda
```

#### 7. Permission Denied on /dev/tenstorrent

**Symptoms**: Cannot access device without sudo

**Solutions**:
```bash
# Check current permissions
ls -l /dev/tenstorrent/

# Create udev rule
sudo tee /etc/udev/rules.d/99-tenstorrent.rules <<EOF
KERNEL=="tenstorrent/*", MODE="0666"
EOF

# Reload
sudo udevadm control --reload-rules
sudo udevadm trigger

# Add user to group (if using group permissions)
sudo usermod -a -G tenstorrent $USER
newgrp tenstorrent
```

### Debug Logging

#### Enable Verbose Logging

```bash
# PyBuda debug logging
export PYBUDA_VERBOSE=1
export LOGGER_LEVEL=DEBUG

# TT-Metal debug logging
export TT_METAL_LOGGER_LEVEL=DEBUG
export TT_METAL_DPRINT_ALL_CORES=1

# Run with debug output
python your_script.py 2>&1 | tee debug.log
```

#### Kernel Module Debug

```bash
# Enable kernel module debug output
sudo modprobe -r tenstorrent
sudo modprobe tenstorrent debug=1

# Check dmesg
sudo dmesg -w
```

### Performance Debugging

#### Monitor Hardware Utilization

```bash
# Install tt-smi
pip install tt-smi

# Monitor in real-time
tt-smi

# Log to file
watch -n 1 'tt-smi >> tt-smi.log'
```

#### Profiling

```bash
# Use pyinstrument for Python profiling
pip install pyinstrument

# Profile script
pyinstrument your_script.py

# Generate HTML report
pyinstrument -r html -o profile.html your_script.py
```

---

## Documentation Archive

Historical documentation has been moved to preserve the theoretical ERBF content while refocusing this README on operational aspects.

### Archived Documentation

- **ERBF Theory**: `archive/docs/README_ERBF_THEORY.md`
- **Diagram Index**: `archive/docs/DIAGRAM_INDEX.md`
- **Structure Improvements**: `archive/docs/STRUCTURE_IMPROVEMENTS.md`
- **Live Diagrams**: `diagrams/` directory (unchanged)

### Access Theoretical Documentation

```bash
# View ERBF theory documentation
cat archive/docs/README_ERBF_THEORY.md

# Browse diagrams
ls diagrams/ERBF/
```

---

## Repository Structure

```
tenstorrent_greyskull/
├── README.md                          # This file (operational focus)
├── BIBLIOGRAPHY.md                    # Library references
├── LICENSE                            # MIT License
├── .github/
│   └── workflows/                     # CI/CD pipelines
│       ├── hardware-ci.yml
│       ├── code-quality.yml
│       └── docs.yml
├── archive/
│   └── docs/                          # Historical documentation
│       ├── README_ERBF_THEORY.md
│       ├── DIAGRAM_INDEX.md
│       └── STRUCTURE_IMPROVEMENTS.md
├── diagnostics/                       # Hardware diagnostic tools
│   ├── tt_diagnostic.py              # Main diagnostic script
│   ├── python_environment.yaml       # Conda environment
│   ├── readme.md                     # Tool documentation
│   └── example_output.txt            # Sample output
├── diagrams/                          # Mermaid diagrams
│   ├── ERBF/                         # Theory diagrams
│   └── [Hardware mapping diagrams]
└── tests/                             # Smoke tests (to be added)
    ├── test_device_detection.py
    ├── test_tensor_op.py
    └── smoke_test.sh
```

---

## Contributing

### Development Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Follow code style (Black formatter)
   - Add tests for new functionality
   - Update documentation

3. **Run Pre-commit Checks**
   ```bash
   pre-commit run --all-files
   ```

4. **Run Tests Locally**
   ```bash
   pytest tests/
   bash smoke_test.sh
   ```

5. **Commit and Push**
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Ensure CI passes
   - Request review
   - Address feedback

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Calisota.ai

---

## Support & Resources

### Internal Resources
- **Diagnostic Tool**: `diagnostics/readme.md`
- **Bibliography**: `BIBLIOGRAPHY.md`
- **Theory Docs**: `archive/docs/`

### External Resources
- **Tenstorrent Documentation**: https://docs.tenstorrent.com/
- **PyBuda GitHub**: https://github.com/tenstorrent/tt-buda
- **TT-Metal GitHub**: https://github.com/tenstorrent/tt-metal
- **Community Discord**: https://discord.gg/tenstorrent

### Reporting Issues

For issues with this repository:
1. Check troubleshooting section
2. Review diagnostic output
3. Search existing issues
4. Open new issue with:
   - System information
   - Diagnostic output (`tenstorrent_diagnostic.json`)
   - Error messages
   - Steps to reproduce

---

**Last Updated**: 2025-01-15
**Repository Status**: Private Development
**Primary Maintainer**: danindiana
