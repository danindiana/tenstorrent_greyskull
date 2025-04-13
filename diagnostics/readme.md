# Tenstorrent e75 and e150 series Diagnostic Tool

The **Tenstorrent Diagnostic Tool** is a Python script designed to analyze and report on the PCIe devices and system configuration of a Linux machine. It provides detailed information about the system, PCIe devices, and potential issues, with a focus on Tenstorrent hardware.

## Features

- Collects system information (hostname, kernel version, CPU model, memory, OS).
- Parses PCIe devices using `lspci` and identifies device classes (e.g., GPU, Accelerator).
- Detects Tenstorrent devices and analyzes their PCIe link status.
- Checks system configuration for:
  - Hugepages configuration.
  - Kernel modules (e.g., `tt_kmd`, `nvidia`, `iommu`).
  - Relevant kernel messages from `dmesg`.
  - CPU flags for virtualization and IOMMU support.
- Generates a detailed diagnostic report.
- Saves the report in JSON and YAML formats (if PyYAML is installed).

## Requirements

- Python 3.6 or higher
- Linux operating system
- The following system commands must be available:
  - `lspci`
  - `lsmod`
  - `dmesg`
  - `grep`
  - `free`
  - `hostname`
  - `uname`
  - `lsb_release` (optional, for OS information)

## Installation

1. Clone or download this repository to your local machine.
2. Ensure Python 3 is installed on your system.
3. (Optional) Install the `PyYAML` library to enable YAML report generation:
   ```bash
   pip install pyyaml
   ```

## Usage

1. Make the script executable:
   ```bash
   chmod +x tenstorrent_diagnostic.py
   ```

2. Run the script:
   ```bash
   ./tenstorrent_diagnostic.py
   ```
   Alternatively, you can run it with Python:
   ```bash
   python3 tenstorrent_diagnostic.py
   ```

3. The script will:
   - Print a detailed diagnostic report to the terminal.
   - Save the report in `tenstorrent_diagnostic.json`.
   - Save the report in `tenstorrent_diagnostic.yaml` (if PyYAML is installed).

## Output

The script generates a detailed report that includes:

1. **System Overview**:
   - Date and time
   - Hostname
   - Kernel version
   - CPU model
   - Memory size
   - Operating system

2. **PCIe Devices**:
   - Bus address
   - Vendor and device information
   - Device class (e.g., GPU, Accelerator)
   - Technical details (e.g., PCIe link status, BAR size mismatches)

3. **Tenstorrent Devices**:
   - Specific analysis of Tenstorrent hardware
   - PCIe link status and potential issues

4. **System Configuration**:
   - Hugepages configuration
   - Kernel modules loaded
   - CPU flags for virtualization and IOMMU support
   - Relevant kernel messages from `dmesg`

5. **Potential Issues and Recommendations**:
   - Identifies degraded PCIe links, missing kernel modules, and other issues.
   - Provides actionable recommendations for system optimization.

## Example Output

### Terminal Output
```
================================================================================
                        TENSTORRENT SYSTEM DIAGNOSTIC REPORT
================================================================================

[SYSTEM OVERVIEW]
Date      : 2025-04-13T12:34:56
Hostname  : dellserver
Kernel    : 5.15.0-70-generic
CPU       : Intel(R) Xeon(R) CPU E5-2690 v4 @ 2.60GHz
Memory    : 128GB
OS        : Ubuntu 22.04.2 LTS

[PCIe DEVICES]
0000:00:1f.2: Intel SATA
Description: SATA controller [0106]: Intel Corporation C600/X79 series chipset SATA RAID Controller [8086:2822] (rev 06)

...

[TENSTORRENT DEVICES]
Device at 0000:03:00.0:
  Vendor/Device: 1e30:1234
  Class: Accelerator
  PCIe Link Status:
    LnkCap: Speed 16GT/s, Width x16
    LnkSta: Speed 8GT/s, Width x8

...

[POTENTIAL ISSUES]
- PCIe link degraded on 0000:03:00.0: (Running at x8GT/s (capable of x16GT/s))

[RECOMMENDATIONS]
- Enable IOMMU in BIOS and kernel parameters (add 'intel_iommu=on' to kernel cmdline)
- Configure hugepages for better performance

================================================================================
                              DIAGNOSTIC COMPLETE
================================================================================
```

### JSON Report
The report is saved as `tenstorrent_diagnostic.json`:
```json
{
  "system_info": {
    "date": "2025-04-13T12:34:56",
    "hostname": "dellserver",
    "kernel": "5.15.0-70-generic",
    "cpu": "Intel(R) Xeon(R) CPU E5-2690 v4 @ 2.60GHz",
    "memory": "128GB",
    "os": "Ubuntu 22.04.2 LTS"
  },
  "devices": [
    {
      "bus_address": "0000:00:1f.2",
      "raw_description": "SATA controller [0106]: Intel Corporation C600/X79 series chipset SATA RAID Controller [8086:2822] (rev 06)",
      "details": [],
      "vendor_name": "Intel",
      "device_class": "SATA"
    }
  ],
  "analysis": {
    "tenstorrent_devices": [
      {
        "bus_address": "0000:03:00.0",
        "vendor_id": "1e30",
        "device_id": "1234",
        "vendor_name": "Tenstorrent",
        "device_class": "Accelerator",
        "details": [
          "LnkCap: Speed 16GT/s, Width x16",
          "LnkSta: Speed 8GT/s, Width x8"
        ]
      }
    ],
    "potential_issues": [
      "PCIe link degraded on 0000:03:00.0: (Running at x8GT/s (capable of x16GT/s))"
    ]
  },
  "config": {
    "hugepages": {
      "configured": false,
      "size": null,
      "count": 0,
      "mounted": false
    },
    "kernel_modules": {
      "tt_kmd": false,
      "nvidia": false,
      "iommu": false
    },
    "dmesg_errors": [],
    "cpu_flags": {
      "iommu": false,
      "svm": false,
      "vmx": true
    }
  }
}
```

## Troubleshooting

- If the script fails to run, ensure all required system commands are installed and accessible in your `PATH`.
- If the YAML report is not generated, install the `PyYAML` library:
  ```bash
  pip install pyyaml
  ```

## License

This script is provided under the MIT License. Feel free to use, modify, and distribute it.

## Author

Developed by Calisota.ai. 2025
