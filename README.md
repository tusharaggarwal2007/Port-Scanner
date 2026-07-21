# ⚡ Terminal Port Scanner

A lightweight, high-performance cross-platform network port scanner built with **Python**, **Flet**, and **ThreadPoolExecutor**. Features a sleek, hacker-inspired terminal UI with real-time status updates and multi-threaded concurrency.

![App Screenshot](assets/screenshot.png)

## 🚀 Features

* **Multi-Threaded Scanning:** Powered by a `ThreadPoolExecutor` pool (default 200 workers) for ultra-fast port evaluation.
* **Real-Time UI Updates:** Thread-safe state management ensuring smooth performance without race conditions or UI crashes.
* **Smart Filtering:** Instant toggle to show only open ports or a full report log.
* **Hacker Aesthetic:** Designed with a dark terminal theme, neon green highlights, and custom Windows branding.

---

## 🛠️ Tech Stack

* **Language:** Python 3.14+
* **UI Framework:** [Flet](https://flet.dev/) (v0.86.1+)
* **Concurrency:** `concurrent.futures`, `threading`

---

## 💻 Getting Started

### Prerequisites

Make sure you have Python installed on your system. 

### Installation & Execution

1. Clone the repository:
   ```bash
   git clone [https://github.com/tusharaggarwal2007/portscanner.git](https://github.com/tusharaggarwal2007/portscanner.git)
   cd portcanner