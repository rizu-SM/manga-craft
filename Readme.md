# Manga Downloader & CBZ Converter

An automated Python toolset built with **Playwright** and **Requests** to scrape manga chapters from various online readers (e.g., `3asq.online`, `mangadar.com`), bypass lazy-loading and anti-bot protections, package each chapter directly into `.cbz` comic book archives, and save them to your local library folder for reading in **YACReader**.

---

## 📋 Features

* **Multi-Site Scrapers:** Dedicated scripts tailored for different manga hosting platforms and reader architectures.
* **Headless Browser Automation:** Uses Playwright (Chromium) to execute dynamic JavaScript and fetch images via authenticated browser contexts.
* **Element Viewport Hydration:** Scrolls to each individual image element prior to scraping to ensure lazy-loaded attributes (`data-src`, `data-lazy-src`, `data-url`) are fully populated in the DOM.
* **Environment-Based Configuration:** Dynamically loads output folder paths from a root `.env` file to keep local machine paths out of Git history.
* **CBZ Archiving:** Packages downloaded chapter images directly into ordered `.cbz` archives (`001.jpg`, `002.jpg`, etc.).
* **Automatic Cleanup & Deduplication:** Cleans up temporary image files after archiving and skips downloading chapters that already exist in your destination folder.
* **YACReader Compatible:** Produces standardized archives ready for instant reading in **YACReader**.

---

## ⚙️ Requirements & Installation

### 1. Install Python

Ensure **Python 3.8+** is installed on your system.

### 2. Clone the Repository

Clone the repository and navigate into the project directory:

```powershell
git clone https://github.com/rizu-SM/manga-craft
cd manga_craft
```

### 3. Install Python Dependencies

```powershell
pip install playwright python-dotenv requests beautifulsoup4
```

### 4. Install Playwright Browser Binaries

```powershell
playwright install chromium
```

### 5. Install YACReader

Download and install **YACReader** if you don't already have it.

Website: https://www.yacreader.com/

---

## 🔑 Environment Setup (`.env`)

Create a `.env` file in the project root directory:

```text
manga_craft/
├── .env
└── ...
```

Define your local output destination inside `.env`:

```env
OUTPUT_DIR=C:\Users\hamro\Videos\manga
```

> **Note:** Copy `.env.example` to `.env` if using a cloned template. `.env` is ignored by Git to keep personal storage paths out of public repositories.

---

## 🛠️ Project Structure & Usage

This repository contains multiple scrapers targeting different websites:

```text
manga_craft/
├── .env
├── downloader.py              # Scraper for 3asq.online (Madara / wp-manga theme)
└── mangadar/
    └── sec-download.py        # Playwright scraper for mangadar.com
```

### Option 1: Scraping 3asq.online (`downloader.py`)

Open `downloader.py` and set your target manga slug and chapter range:

```python
MANGA_SLUG = "one-piece"
START_CHAPTER = 61
END_CHAPTER = 65
```

Run the script:

```powershell
python .\downloader.py
```

### Option 2: Scraping Mangadar (`mangadar/sec-download.py`)

Open `mangadar/sec-download.py` and set your URL template and chapter range:

```python
URL_TEMPLATE = "https://mangadar.com/manga/kingdom/{}"
START_CHAPTER = 185
END_CHAPTER = 200
```

Run the script:

```powershell
python .\mangadar\sec-download.py
```

---

## 📖 How to Read in YACReader

Once the script finishes downloading and generating the `.cbz` files:

1. Launch **YACReader**.

2. Press **`O`** on your keyboard to open the file picker.

3. Navigate to your configured output folder, for example:

   ```text
   C:\Users\hamro\Videos\manga
   ```

4. Select your generated `.cbz` file, for example:

   ```text
   Kingdom_Chapter_185.cbz
   ```

5. Open the file and enjoy reading.

---

## 📌 Notes

* Keep your `.env` file private and never commit it to Git.
* Make sure the target websites allow automated access and downloading.
* The scrapers may need updates if the target websites change their HTML structure or anti-bot mechanisms.
