# === ESP32-C5 Auto Flasher Script By: AWOK ===

import sys
import subprocess
import os
import platform
import glob
import time
import shutil
import argparse
import threading
import queue
import io
import contextlib
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

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

def preferred_port(ports):
    if not ports:
        return None
    macos_ports = [p for p in ports if p.startswith("/dev/cu.")]
    if macos_ports:
        return macos_ports[0]
    return ports[0]

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
        "--gui",
        action="store_true",
        help="Launch the graphical interface.",
    )
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
    if args.gui:
        run_gui()
        return

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
                serial_port = preferred_port(sorted(new_ports))
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

def resolve_bins(bins_dir):
    if not os.path.isdir(bins_dir):
        raise FileNotFoundError(f"Bins directory not found: {bins_dir}")
    bootloader = find_file(['bootloader.bin'], bins_dir)
    partitions = find_file(['partition-table.bin', 'partitions.bin'], bins_dir)
    ota_data = find_file(['ota_data_initial.bin'], bins_dir)
    all_bins = glob.glob(os.path.join(bins_dir, "*.bin"))
    exclude = {bootloader, partitions, ota_data}
    firmware_bins = [f for f in all_bins if f not in exclude and os.path.isfile(f)]
    if not firmware_bins:
        raise FileNotFoundError("No application firmware .bin file found in the bins folder.")
    app_bin = max(firmware_bins, key=lambda f: os.path.getsize(f))
    if not (bootloader and partitions):
        raise FileNotFoundError("Missing bootloader or partition table. Both are required for a complete flash.")
    return bootloader, partitions, ota_data, app_bin

def flash_device(chip_key, port, baud, bins_dir, log_queue):
    chip_config = CHIP_CONFIGS[chip_key]
    bootloader, partitions, ota_data, app_bin = resolve_bins(bins_dir)
    esptool_args = [
        '--chip', chip_config["esptool_chip"],
        '--port', port,
        '--baud', str(baud),
        '--before', 'default_reset',
        '--after', 'hard_reset',
        'write_flash', '-z',
        chip_config["bootloader_offset"], bootloader,
        chip_config["partition_offset"], partitions,
    ]
    if ota_data:
        esptool_args += [chip_config["ota_offset"], ota_data]
    esptool_args += [chip_config["app_offset"], app_bin]

    output_buffer = io.StringIO()
    with contextlib.redirect_stdout(output_buffer), contextlib.redirect_stderr(output_buffer):
        esptool.main(esptool_args)
    log_queue.put(output_buffer.getvalue())

def run_gui():
    root = tk.Tk()
    root.title("ESP32 Auto Flasher")
    root.geometry("780x520")
    log_queue = queue.Queue()

    main_frame = ttk.Frame(root, padding=12)
    main_frame.pack(fill="both", expand=True)

    config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding=10)
    config_frame.pack(fill="x")

    ttk.Label(config_frame, text="Chip").grid(row=0, column=0, sticky="w")
    chip_var = tk.StringVar(value="esp32c5")
    chip_combo = ttk.Combobox(config_frame, textvariable=chip_var, values=sorted(CHIP_CONFIGS.keys()), state="readonly")
    chip_combo.grid(row=0, column=1, sticky="ew", padx=6)

    ttk.Label(config_frame, text="Serial Port").grid(row=1, column=0, sticky="w")
    port_var = tk.StringVar()
    port_combo = ttk.Combobox(config_frame, textvariable=port_var, values=[], state="readonly")
    port_combo.grid(row=1, column=1, sticky="ew", padx=6)

    def refresh_ports():
        ports = list_serial_ports()
        port_combo["values"] = ports
        preferred = preferred_port(ports)
        if preferred:
            port_var.set(preferred)
        elif ports:
            port_var.set(ports[0])
        else:
            port_var.set("")

    refresh_button = ttk.Button(config_frame, text="Refresh", command=refresh_ports)
    refresh_button.grid(row=1, column=2, padx=6)

    ttk.Label(config_frame, text="Baud").grid(row=2, column=0, sticky="w")
    baud_var = tk.StringVar(value="921600")
    baud_entry = ttk.Entry(config_frame, textvariable=baud_var)
    baud_entry.grid(row=2, column=1, sticky="ew", padx=6)

    ttk.Label(config_frame, text="Bins Directory").grid(row=3, column=0, sticky="w")
    bins_var = tk.StringVar(value=os.path.join(os.path.dirname(__file__), "bins"))
    bins_entry = ttk.Entry(config_frame, textvariable=bins_var)
    bins_entry.grid(row=3, column=1, sticky="ew", padx=6)

    def browse_bins():
        selected = filedialog.askdirectory(initialdir=bins_var.get() or os.getcwd())
        if selected:
            bins_var.set(selected)

    browse_button = ttk.Button(config_frame, text="Browse", command=browse_bins)
    browse_button.grid(row=3, column=2, padx=6)

    config_frame.columnconfigure(1, weight=1)

    status_frame = ttk.LabelFrame(main_frame, text="Status", padding=10)
    status_frame.pack(fill="both", expand=True, pady=10)

    log_text = tk.Text(status_frame, wrap="word", height=12, state="disabled")
    log_text.pack(fill="both", expand=True)

    def append_log(message):
        log_text.configure(state="normal")
        log_text.insert("end", message + "\n")
        log_text.see("end")
        log_text.configure(state="disabled")

    def process_log_queue():
        while not log_queue.empty():
            append_log(log_queue.get())
        root.after(200, process_log_queue)

    def start_flash():
        chip_key = chip_var.get()
        port = port_var.get()
        baud = baud_var.get().strip()
        bins_dir = bins_var.get().strip()
        if not port:
            messagebox.showerror("Missing Port", "Please select a serial port.")
            return
        if not baud.isdigit():
            messagebox.showerror("Invalid Baud", "Baud rate must be numeric.")
            return
        try:
            bootloader, partitions, ota_data, app_bin = resolve_bins(bins_dir)
        except FileNotFoundError as exc:
            messagebox.showerror("Bins Error", str(exc))
            return
        summary = "\n".join([
            f"Chip: {CHIP_CONFIGS[chip_key]['display_name']}",
            f"Port: {port}",
            f"Baud: {baud}",
            f"Bootloader: {bootloader}",
            f"Partitions: {partitions}",
            f"OTA Data: {ota_data or 'NOT FOUND'}",
            f"App: {app_bin}",
        ])
        if not messagebox.askyesno("Confirm Flash", f"Ready to flash with the following settings?\n\n{summary}"):
            return

        append_log(f"Starting flash for {CHIP_CONFIGS[chip_key]['display_name']} on {port}...")

        def run_flash():
            try:
                flash_device(chip_key, port, baud, bins_dir, log_queue)
                log_queue.put("Flashing complete!")
            except Exception as exc:
                log_queue.put(f"Flashing failed: {exc}")

        threading.Thread(target=run_flash, daemon=True).start()

    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill="x")
    flash_button = ttk.Button(button_frame, text="Flash", command=start_flash)
    flash_button.pack(side="right")

    refresh_ports()
    process_log_queue()
    root.mainloop()

if __name__ == "__main__":
    main()
