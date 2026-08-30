# Manga Downloader & CBZ Converter

An automated Python tool designed to scrape manga chapters from sites powered by the Madara/wp-manga theme (e.g., `3asq.online`), package each chapter directly into `.cbz` comic book archives, and save them directly to your local library folder for reading in **YACReader**.

---

## 📋 Features
- Automatically downloads chapter images from `div.reading-content`.
- Handles lazy-loaded image attributes (`data-src`, `data-lazy-src`, `src`).
- Packages downloaded images directly into `.cbz` format with ordered page numbering (`001.jpg`, `002.jpg`, etc.).
- Automatically moves completed `.cbz` files to your designated manga destination folder.
- Cleans up temporary uncompressed files after packaging.
- Seamlessly integrates with **YACReader** for comic/manga reading.

---

## ⚙️ Requirements & Installation

1. Make sure **Python 3.x** is installed on your system.
2. Install the required Python packages:

```bash
pip install requests bs4
```

3. Download and install **YACReader** (if not already installed):
   - Website: [https://www.yacreader.com/](https://www.yacreader.com/)

---

## 🛠️ User Configurations (`downloader.py`)

Before running the script, open `downloader.py` in your text editor and adjust the configuration parameters at the top of the file according to your needs:

| Variable | Description | Example Value |
| :--- | :--- | :--- |
| `MANGA_SLUG` | The URL identifier of the target manga on the website | `"one-piece"` |
| `START_CHAPTER` | The starting chapter number to download | `61` |
| `END_CHAPTER` | The ending chapter number to download | `65` |
| `OUTPUT_DIR` | The destination directory where `.cbz` files will be saved | `r"C:\Users\hamro\Videos\manga"` |

### Configuration Example in `downloader.py`:

```python
# ==========================================
# USER CONFIGURATION SECTION
# ==========================================

# 1. Target Manga Slug (found in the site URL: https://3asq.online/manga/<MANGA_SLUG>/)
MANGA_SLUG = "one-piece"

# 2. Chapter Range
START_CHAPTER = 61
END_CHAPTER = 65

# 3. Destination folder for CBZ files
OUTPUT_DIR = r"C:\Users\you\manga
# ==========================================
```

---

## 🚀 How to Run

1. Open PowerShell or Command Prompt in your project directory:
```powershell
   git clone https://github.com/rizu-SM/manga-craft
   ```
   ```powershell
   cd manga_craft
   ```
2. Run the script:
   ```powershell
   python .\downloader.py
   ```

---

## 📖 How to Read in YACReader

Once the script finishes downloading and generating the `.cbz` files:

1. Launch **YACReader**.
2. Press **`O`** on your keyboard to open the file picker.
3. Navigate to your output folder (`C:\Users\hamro\Videos\manga`).
4. Select your generated `.cbz` file (e.g., `chapter_61.cbz`) and open it.
5. Enjoy reading!