#!/usr/bin/env python3
import re
import subprocess
import json
import sys
from datetime import datetime
from typing import List, Dict, Any

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

class TenstorrentDiagnostic:
    def __init__(self):
        self.known_vendors = {
            '10de': 'NVIDIA',
            '1e30': 'Tenstorrent',
            '1e52': 'Tenstorrent',
            '1002': 'AMD',
            '8086': 'Intel'
        }
        self.relevant_classes = {
            '0300': 'GPU',
            '1200': 'Accelerator',
            '0403': 'Audio',
            '0c03': 'USB',
            '0106': 'SATA',
            '0107': 'SAS'
        }

    def run_command(self, cmd: str) -> str:
        try:
            result = subprocess.run(
                cmd, shell=True, check=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            if "grep" not in cmd or e.returncode != 1:
                print(f"\n[!] Command failed: {cmd}\nError: {e.stderr}", file=sys.stderr)
            return ""

    def get_system_info(self) -> Dict[str, str]:
        info = {
            'date': datetime.now().isoformat(),
            'hostname': self.run_command("hostname").strip(),
            'kernel': self.run_command("uname -r").strip(),
            'cpu': self.run_command("lscpu | grep 'Model name' | cut -d: -f2").strip(),
            'memory': self.run_command("free -h | grep Mem | awk '{print $2}'").strip() + "B"
        }

        os_info = self.run_command("lsb_release -d 2>/dev/null")
        if os_info and "Description" in os_info:
            info['os'] = os_info.split(":")[1].strip()
        else:
            info['os'] = self.run_command("cat /etc/os-release | grep PRETTY_NAME | cut -d= -f2").strip('"')
        
        return info

    def parse_lspci_devices(self) -> List[Dict[str, Any]]:
        output = self.run_command("lspci -nnvvv")
        devices = []
        current_device = {}

        for line in output.split('\n'):
            if not line.strip():
                if current_device:
                    class_id = current_device.get('class_id', '')
                    current_device['device_class'] = self.relevant_classes.get(class_id, 'Other')
                    devices.append(current_device)
                    current_device = {}
                continue

            if line[0].isdigit():
                parts = line.split()
                current_device = {
                    'bus_address': parts[0],
                    'raw_description': ' '.join(parts[1:]),
                    'details': [],
                    'vendor_name': 'Unknown'  # Default value
                }

                vendor_match = re.search(r'([0-9a-f]{4}):([0-9a-f]{4})', line)
                if vendor_match:
                    vendor_id = vendor_match.group(1)
                    device_id = vendor_match.group(2)
                    current_device.update({
                        'vendor_id': vendor_id,
                        'device_id': device_id,
                        'vendor_name': self.known_vendors.get(vendor_id, "Unknown"),
                    })

                class_match = re.search(r'([0-9a-f]{4}):', line)
                if class_match:
                    current_device['class_id'] = class_match.group(1)

            else:
                cleaned = line.strip()
                if any(x in cleaned.lower() for x in ['lnkcap', 'lnksta', 'iommu', 'bar', 'irq']):
                    current_device['details'].append(cleaned)

        return devices

    def analyze_pcie_devices(self, devices: List[Dict[str, Any]]) -> Dict[str, Any]:
        analysis = {
            'tenstorrent_devices': [],
            'other_accelerators': [],
            'potential_issues': []
        }

        for dev in devices:
            if 'device_class' not in dev:
                dev['device_class'] = 'Other'

            if dev['vendor_name'] == 'Intel' and not any(x in dev['raw_description'] for x in ['RAID', 'SATA']):
                continue

            analysis['tenstorrent_devices'].append(dev)

            for detail in dev.get('details', []):
                if 'BAR size mismatch' in detail:
                    analysis['potential_issues'].append(f"BAR size mismatch detected on {dev['bus_address']}")
                if 'LnkSta' in detail and 'LnkCap' in detail:
                    cap_match = re.search(r'LnkCap:\s+Speed\s+(\d+)GT/s,\s+Width\s+x(\d+)', detail)
                    sta_match = re.search(r'LnkSta:\s+Speed\s+(\d+)GT/s,\s+Width\s+x(\d+)', detail)
                    if cap_match and sta_match:
                        cap_speed, cap_width = int(cap_match.group(1)), int(cap_match.group(2))
                        sta_speed, sta_width = int(sta_match.group(1)), int(sta_match.group(2))
                        if sta_speed < cap_speed or sta_width < cap_width:
                            analysis['potential_issues'].append(
                                f"PCIe link degraded on {dev['bus_address']}: "
                                f"(Running at x{sta_width}GT/s (capable of x{cap_width}GT/s))"
                            )
        return analysis

    def check_system_config(self) -> Dict[str, Any]:
        config = {
            'hugepages': self.check_hugepages(),
            'kernel_modules': self.check_kernel_modules(),
            'dmesg_errors': self.check_dmesg(),
            'cpu_flags': self.check_cpu_flags()
        }
        return config

    def check_hugepages(self) -> Dict[str, Any]:
        hugepages = {'configured': False, 'size': None, 'count': 0}
        meminfo = self.run_command("grep -i huge /proc/meminfo")
        
        if 'HugePages_Total' in meminfo:
            hugepages['configured'] = True
            hugepages['count'] = int(re.search(r'HugePages_Total:\s+(\d+)', meminfo).group(1))
            hugepages['size'] = re.search(r'Hugepagesize:\s+(\d+)', meminfo).group(1) + " kB"
        
        hugepages['mounted'] = bool(self.run_command("mount | grep -i huge"))
        
        return hugepages

    def check_kernel_modules(self) -> Dict[str, Any]:
        modules = {
            'tt_kmd': False,
            'nvidia': False,
            'iommu': False
        }

        lsmod = self.run_command("lsmod")
        modules['tt_kmd'] = 'tt_kmd' in lsmod
        modules['nvidia'] = 'nvidia' in lsmod
        modules['iommu'] = ('iommu' in lsmod) or ('intel_iommu' in lsmod)
        
        return modules

    def check_dmesg(self) -> List[str]:
        errors = []
        dmesg = self.run_command("dmesg | grep -iE 'error|fail|warn|tt|iommu|pcie' | tail -n 50")
        
        for line in dmesg.split('\n'):
            if line and any(x in line.lower() for x in ['bar size', 'iommu', 'pcie error', 'tt']):
                errors.append(line.strip())
        
        return errors

    def check_cpu_flags(self) -> Dict[str, bool]:
        flags = self.run_command("grep flags /proc/cpuinfo | head -1").lower()
        return {
            'iommu': 'iommu' in flags,
            'svm': 'svm' in flags,
            'vmx': 'vmx' in flags
        }

    def print_detailed_report(self, system_info: Dict[str, Any], 
                            devices: List[Dict[str, Any]], 
                            analysis: Dict[str, Any], 
                            config: Dict[str, Any]):
        print("\n" + "="*80)
        print("TENSTORRENT SYSTEM DIAGNOSTIC REPORT".center(80))
        print("="*80)

        # System Overview
        print("\n[SYSTEM OVERVIEW]")
        for key, value in system_info.items():
            print(f"{key.capitalize():<10}: {value}")
        
        # PCIe Devices
        print("\n[PCIe DEVICES]")
        for dev in devices:
            if (dev['vendor_name'] not in ['Intel', 'Unknown'] or 
                dev['device_class'] in ['GPU', 'Accelerator'] or 
                any(issue in str(dev['details']) for issue in ['BAR', 'error', 'fail'])):
                
                print(f"\n{dev['bus_address']}: {dev.get('vendor_name', 'Unknown')} {dev.get('device_class', 'Unknown')}")
                print(f"Description: {dev.get('raw_description', 'N/A')}")
                
                # Print relevant details
                printed_details = False
                for detail in dev.get('details', []):
                    if any(x in detail.lower() for x in ['lnkcap', 'lnksta', 'bar', 'iommu', 'error', 'fail']):
                        print(f"  {detail}")
                        printed_details = True
                
                if not printed_details and dev.get('details'):
                    print(f"  (No relevant technical details available)")
        
        # Tenstorrent Specific Analysis
        if analysis['tenstorrent_devices']:
            print("\n[TENSTORRENT DEVICES]")
            for tt_dev in analysis['tenstorrent_devices']:
                print(f"\nDevice at {tt_dev['bus_address']}:")
                print(f"  Vendor/Device: {tt_dev.get('vendor_id', 'N/A')}:{tt_dev.get('device_id', 'N/A')}")
                print(f"  Class: {tt_dev.get('device_class', 'Unknown')}")
                
                # Print link status
                link_details = [d for d in tt_dev.get('details', []) if 'Lnk' in d]
                if link_details:
                    print("  PCIe Link Status:")
                    for detail in link_details:
                        print(f"    {detail}")
        
        # System Configuration
        print("\n[SYSTEM CONFIGURATION]")
        print("\nHugepages:")
        print(f"  Configured: {'Yes' if config['hugepages']['configured'] else 'No'}")
        if config['hugepages']['configured']:
            print(f"  Size: {config['hugepages']['size']}")
            print(f"  Count: {config['hugepages']['count']}")
            print(f"  Mounted: {'Yes' if config['hugepages']['mounted'] else 'No'}")
        
        print("\nKernel Modules:")
        print(f"  tt_kmd: {'Loaded' if config['kernel_modules']['tt_kmd'] else 'Not loaded'}")
        print(f"  NVIDIA: {'Loaded' if config['kernel_modules']['nvidia'] else 'Not loaded'}")
        print(f"  IOMMU: {'Enabled' if config['kernel_modules']['iommu'] else 'Disabled'}")
        
        # CPU Features
        cpu_flags = config['cpu_flags']
        if cpu_flags['iommu']:
            print("  IOMMU Support: Yes")
        if cpu_flags.get('svm'):
            print("  AMD SVM: Enabled")
        if cpu_flags.get('vmx'):
            print("  Intel VT-x: Enabled")
        
        # Issues and Recommendations
        if analysis['potential_issues'] or config['dmesg_errors']:
            print("\n[POTENTIAL ISSUES]")
            
            for issue in analysis['potential_issues']:
                print(f"- {issue}")
            
            if config['dmesg_errors']:
                print("\nRelevant kernel messages:")
                for error in config['dmesg_errors'][-5:]:  # Show last 5 errors
                    print(f"- {error}")
            
            print("\n[RECOMMENDATIONS]")
            if not config['kernel_modules']['tt_kmd']:
                print("- Install and load Tenstorrent kernel module (tt_kmd)")
            if not config['hugepages']['configured']:
                print("- Configure hugepages for better performance")
            if not config['kernel_modules']['iommu']:
                print("- Enable IOMMU in BIOS and kernel parameters (add 'intel_iommu=on' to kernel cmdline)")

        print("\n" + "="*80)
        print("DIAGNOSTIC COMPLETE".center(80))
        print("="*80)

    def save_report(self, data: Dict[str, Any]):
        with open("tenstorrent_diagnostic.json", "w") as f:
            json.dump(data, f, indent=2)
        
        if YAML_AVAILABLE:
            with open("tenstorrent_diagnostic.yaml", "w") as f:
                yaml.dump(data, f, default_flow_style=False)

def main():
    diag = TenstorrentDiagnostic()
    
    print("Running Tenstorrent PCIe Diagnostic Tool...")
    
    # Collect data
    system_info = diag.get_system_info()
    devices = diag.parse_lspci_devices()
    analysis = diag.analyze_pcie_devices(devices)
    config = diag.check_system_config()
    
    # Generate output
    diag.print_detailed_report(system_info, devices, analysis, config)
    
    # Save report
    diag.save_report({'system_info': system_info, 'devices': devices, 'analysis': analysis, 'config': config})
    
    print("\nReport saved to 'tenstorrent_diagnostic.json'")
    if YAML_AVAILABLE:
        print("Report also saved to 'tenstorrent_diagnostic.yaml'")

if __name__ == "__main__":
    main()
