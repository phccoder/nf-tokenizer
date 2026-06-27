# Unified Netflix Cookie Checker

A modern, fast, and multi-threaded **Netflix Cookie Checker** desktop application built using Python and Tkinter. This tool allows users to import raw cookies or JSON array blocks, automatically parse them, and query validation statuses in real-time. It features a polished Tokyo Night-inspired dark theme, a built-in live debugging console, and an elegant card dashboard to review account analytics.

---

## 🚀 Features

* **Dual-Format Parsing:** Effortlessly reads cookies from either **raw text patterns** (Key=Value pairs) or **standard JSON array structures**.
* **Asynchronous Processing:** Powered by Python's `threading` library, ensuring the graphical user interface (GUI) never freezes while validating inputs over the network.
* **Server-Sent Events (SSE) Streaming:** Interacts dynamically with API streaming endpoints to output raw statuses directly to a scrolling log window.
* **Intuitive Dashboard Layout:** Renders parsed account metrics like plan status, signup country, price tier, billing cycle dates, and email verification status into readable grids.
* **Cross-Account Navigation:** Easily toggle back and forth through multiple bulk results using the interactive built-in navigation bar (`◀ Previous` / `Next ▶`).
* **One-Click Clipboard Links:** Generated tokens can be quickly modified for separate deployment targets (**PC**, **Mobile**, or **TV**) and copied natively to your clipboard.

---

## 🛠️ Technology Stack

* **GUI Framework:** `tkinter` (Native Python GUI)
* **Networking:** `requests` (With streaming response iterator processing)
* **Data Serialization:** `json` & `re` (Regular expression patterns for advanced text block chunking)
* **Concurrency:** `threading` 

---

## ⚙️ Getting Started

### Prerequisites

Make sure you have **Python 3.x** installed on your system. You will also need the `requests` library to manage HTTP handshakes.

### Installation

1. Clone this repository to your local system:
   ```bash
   git clone https://github.com/phccoder/nf-tokenizer.git
   cd YOUR_REPOSITORY_NAME

2. Install the necessary dependencies via pip:
   ```bash
   pip install requests

### Running the Application

Execute the Python script to open up the desktop control layout:
   ```bash
   python nf-tokenizer.py