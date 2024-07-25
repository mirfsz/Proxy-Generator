# 🚀 Proxy Generator v2.0

## 📌 Overview

Proxy Generator is a user-friendly Python script that fetches, validates, and exports free proxies. It's designed to be easy to use while providing powerful functionality for proxy management.

Created by: Irfan

## ✨ Features

- 🔍 Fetch free proxies from sslproxies.org
- 🧪 Validate proxies for functionality
- 📁 Export working proxies to a file
- 🖥️ User-friendly console interface with emojis
- 🔄 Real-time progress updates with simple animations

## 🛠️ Requirements

- Python 3.6+
- requests
- lxml

## 📦 Installation

1. Clone this repository
2. Navigate to the project directory: cd proxy-generator
3. Install the required packages: pip install -r requirements.txt

## 🚀 Usage

Run the script:
python proxy_generator.py

Follow the on-screen prompts to:
1. Fetch and validate proxies
2. View information about the script
3. Exit the program

When fetching proxies, you can specify:
- The maximum number of proxies to fetch
- The timeout for proxy validation

After validation, you'll have the option to export working proxies to a file.

## 📄 Output

The script generates two types of output:
1. Console output with real-time updates and results
2. A log file (`proxy_operations.log`) with detailed operation logs
3. An optional export file with working proxies (default: `working_proxies.txt`)

## ⚠️ Disclaimer

This tool is for educational purposes only. Always respect website terms of service and use proxies responsibly.

