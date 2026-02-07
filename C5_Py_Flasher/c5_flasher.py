# === ESP32-C5 Auto Flasher Script By: AWOK ===

import sys
import subprocess
import os
import platform
import glob
import time
import shutil
import argparse

def ensure_package(pkg):
    try:
        __import__(pkg if pkg != 'gitpython' else 'git')
    except ImportError:
        print(f"Installing missing package: {pkg}")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', pkg])

try:
    import serial.tools.list_ports
except ImportError:
    ensure_package('pyserial')
try:
    import esptool
except ImportError:
    ensure_package('esptool')
try:
    from colorama import Fore, Style
except ImportError:
    ensure_package('colorama')

# Dependency check and install if needed
REQUIRED_PACKAGES = [
    'pyserial',
    'esptool',
    'colorama'
]

def ensure_requirements():
    for pkg in REQUIRED_PACKAGES:
        ensure_package(pkg)
ensure_requirements()

# Finds the first file from a list of possible names in the bins folder
def find_file(name_options, bins_dir):
    for name in name_options:
        files = glob.glob(os.path.join(bins_dir, name))
        if files:
            return files[0]
    return None

CHIP_CONFIGS = {
    "esp32c5": {
        "display_name": "ESP32-C5",
        "bootloader_offset": "0x2000",
        "partition_offset": "0x8000",
        "ota_offset": "0xd000",
        "app_offset": "0x10000",
        "esptool_chip": "esp32c5",
    },
    "esp32": {
        "display_name": "ESP32",
        "bootloader_offset": "0x1000",
        "partition_offset": "0x8000",
        "ota_offset": "0xd000",
        "app_offset": "0x10000",
        "esptool_chip": "esp32",
    },
    "esp32-a1s": {
        "display_name": "ESP32-A1S",
        "bootloader_offset": "0x1000",
        "partition_offset": "0x8000",
        "ota_offset": "0xd000",
        "app_offset": "0x10000",
        "esptool_chip": "esp32",
    },
}

def list_serial_ports():
    return [port.device for port in serial.tools.list_ports.comports()]

def choose_port(available_ports, preferred=None):
    if preferred and preferred in available_ports:
        return preferred
    if len(available_ports) == 1:
        return available_ports[0]
    print(Fore.YELLOW + "Multiple serial ports detected:" + Style.RESET_ALL)
    for idx, port in enumerate(available_ports, start=1):
        print(f"{idx}) {port}")
    while True:
        selection = input(Fore.YELLOW + "Select the port number to use: " + Style.RESET_ALL).strip()
        if selection.isdigit():
            choice = int(selection)
            if 1 <= choice <= len(available_ports):
                return available_ports[choice - 1]
        print(Fore.RED + "Invalid selection. Please try again." + Style.RESET_ALL)

def main():
    parser = argparse.ArgumentParser(description="ESP32 Auto Flasher (bins subdir)")
    parser.add_argument(
        "--chip",
        default="esp32c5",
        choices=sorted(CHIP_CONFIGS.keys()),
        help="Target chip type (default: esp32c5). Use esp32-a1s for ESP32-A1S.",
    )
    parser.add_argument(
        "--port",
        default=None,
        help="Serial port to use (optional). If not provided, auto-detects.",
    )
    parser.add_argument(
        "--baud",
        default="921600",
        help="Baud rate for flashing (default: 921600).",
    )
    parser.add_argument(
        "--bins-dir",
        default=os.path.join(os.path.dirname(__file__), "bins"),
        help="Directory containing the .bin files (default: bins folder).",
    )
    parser.add_argument(
        "--no-wait",
        action="store_true",
        help="Skip waiting for a new device and instead select from available ports.",
    )
    args = parser.parse_args()

    bins_dir = args.bins_dir
    if not os.path.isdir(bins_dir):
        print(Fore.RED + f"Bins directory not found: {bins_dir}\nPlease create a 'bins' folder with your .bin files." + Style.RESET_ALL)
        exit(1)

    # Logo and splash, both centered and purple
    terminal_width = shutil.get_terminal_size((100, 20)).columns
    def center(text): return text.center(terminal_width)
    logo_lines = [
        "                                            @@@@@@                              ",
        "                                @@@@@@@@  @@@@@ @@@@                            ",
        "                               @@@    @@@@@@@     @@@     @@@@@@@@              ",
        "                    @@@@@@@@@@@@@      @@@@@       @@@  @@@@    @@@             ",
        "                   @@@      @@@@@       @@@         @@@@@@       @@@            ",
        "                  @@@         @@@        @@         @@@@         @@@            ",
        "         @@@@@@@@@@@@          @@        @          @@@         @@@     @@      ",
        "        @@@     @@@@@           @@           @@@    @@          @@@@@@@@@@@@@@  ",
        "       @@@         @@@           @@          @@@               @@@@@        @@@@",
        "       @@@           @@                     @@@@              @@@            @@@",
        "      @@@@@            @@                   @@@@                             @@@",
        "   @@@@@@  @@                @@         @   @@@                            @@@@ ",
        "  @@@                         @@       @@         @                     @@@@@@  ",
        " @@@                           @@     @@@        @@            @@@@@@@@@@@@@@@  ",
        "@@@       @@@@      @          @@@@  @@@@@     @@@        @      @@@@  @@@ @@@  ",
        "@@@       @@@@@@@    @@@       @@@@@@@@@@@@@@@@@@@       @@        @@@ @@@      ",
        "@@@        @@@@@ @@@  @@@@@  @@@@ @@@@  @@@@@@@@@@      @@@@        @@@         ",
        "@@@@            @@@@@@@@@@@@@@@@  @@@   @@@ @@  @@@@@@@@@@@@         @@@        ",
        " @@@@          @@@@@@@@@@@@@@@@   @@@       @@   @@@@@@@@@@@@        @@@        ",
        "  @@@@@@     @@@@@   @@@     @@    @               @@  @@  @@@@    @@@@         ",
        "   @@@@@@@@@@@@@     @@@     @@                    @@  @@   @@@@@@@@@@@         ",
        "   @@@@@@@@@@@@      @@@     @@                   @@@  @     @@@@@@@@           ",
        "        @@  @@                                    @@@        @@  @@@            ",
        "        @   @@                                               @@  @@@            ",
        "           @@@                                                   @@@            ",
        "           @@@                                                                  ",
        ""
    ]
    splash_lines = [
        "--  ESP32 C5 Flasher --",
        "By AWOK",
        "Inspired from LordSkeletonMans ESP32 FZEasyFlasher",
        "Shout out to JCMK for the inspiration on setting up the C5",
        ""
    ]
    print(Fore.MAGENTA + "\n" + "\n".join(center(line) for line in logo_lines + splash_lines) + Style.RESET_ALL)

    chip_config = CHIP_CONFIGS[args.chip]
    chip_label = chip_config["display_name"]

    # Wait for ESP32 device to show up as a new serial port
    serial_port = None
    if args.port:
        available_ports = list_serial_ports()
        serial_port = choose_port(available_ports, preferred=args.port)
    elif not args.no_wait:
        existing_ports = set(list_serial_ports())
        print(Fore.YELLOW + f"Waiting for {chip_label} device to be connected..." + Style.RESET_ALL)
        wait_start = time.time()
        while time.time() - wait_start < 30:
            current_ports = set(list_serial_ports())
            new_ports = current_ports - existing_ports
            if new_ports:
                macos_ports = [p for p in new_ports if p.startswith("/dev/cu.")]
                serial_port = macos_ports[0] if macos_ports else new_ports.pop()
                break
            time.sleep(0.5)
    if serial_port is None:
        available_ports = list_serial_ports()
        if not available_ports:
            print(Fore.RED + "No serial ports detected. Please connect your device and try again." + Style.RESET_ALL)
            exit(1)
        serial_port = choose_port(available_ports)

    print(Fore.GREEN + f"Using serial port: {serial_port}" + Style.RESET_ALL)

    # Find bin files for each firmware component
    bootloader = find_file(['bootloader.bin'], bins_dir)
    partitions = find_file(['partition-table.bin', 'partitions.bin'], bins_dir)
    ota_data = find_file(['ota_data_initial.bin'], bins_dir)

    # Main firmware: largest bin in the folder that's not bootloader, partition, or OTA
    all_bins = glob.glob(os.path.join(bins_dir, "*.bin"))
    exclude = {bootloader, partitions, ota_data}
    firmware_bins = [f for f in all_bins if f not in exclude and os.path.isfile(f)]
    if not firmware_bins:
        print(Fore.RED + "No application firmware .bin file found in the 'bins' folder!" + Style.RESET_ALL)
        exit(1)
    app_bin = max(firmware_bins, key=lambda f: os.path.getsize(f))

    # Print summary, ask for confirmation before flashing
    print(Fore.CYAN + f"\nTarget chip:  {chip_label}")
    print(f"Bootloader:   {bootloader or 'NOT FOUND'}")
    print(f"Partitions:   {partitions or 'NOT FOUND'}")
    print(f"OTA Data:     {ota_data or 'NOT FOUND'}")
    print(f"App (main):   {app_bin}\n" + Style.RESET_ALL)
    if not (bootloader and partitions):
        print(Fore.RED + "Missing bootloader or partition table. Both are required for a complete flash!" + Style.RESET_ALL)
        exit(1)
    confirm = input(Fore.YELLOW + f"Ready to flash these files to {chip_label}? (y/N): " + Style.RESET_ALL)
    if confirm.strip().lower() != 'y':
        print("Aborting.")
        exit(0)

    # Flash using esptool, with offsets per chip
    esptool_args = [
        '--chip', chip_config["esptool_chip"],
        '--port', serial_port,
        '--baud', str(args.baud),
        '--before', 'default_reset',
        '--after', 'hard_reset',
        'write_flash', '-z',
        chip_config["bootloader_offset"], bootloader,
        chip_config["partition_offset"], partitions,
    ]
    if ota_data:
        esptool_args += [chip_config["ota_offset"], ota_data]
    esptool_args += [chip_config["app_offset"], app_bin]

    print(Fore.YELLOW + f"Flashing {chip_label} with bootloader, partition table, and application..." + Style.RESET_ALL)
    try:
        esptool.main(esptool_args)
        print(Fore.GREEN + "Flashing complete!" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Flashing failed: {e}" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
