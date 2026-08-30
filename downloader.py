import os
import shutil
import zipfile
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

# Configuration
MANGA_SLUG = "kingdom-2"  # Target manga slug on 3asq.online
START_CHAPTER = 61
END_CHAPTER = 62

# Destination folder for CBZ files
OUTPUT_DIR = r"C:\Users\you\manga"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Referer": "https://3asq.online/",
}


def extract_image_url(img_tag):
    possible_attrs = ["src", "data-src", "data-lazy-src", "data-full-url"]
    for attr in possible_attrs:
        url = img_tag.get(attr)
        if url:
            url = url.strip()
            if url.startswith("//"):
                return "https:" + url
            if url.startswith("http"):
                return url
    return None


def convert_to_cbz(folder_path, cbz_path):
    """Compresses all images inside folder_path into a .cbz file at cbz_path."""
    with zipfile.ZipFile(cbz_path, "w", zipfile.ZIP_DEFLATED) as cbz:
        for file in sorted(os.listdir(folder_path)):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                # Add file into zip with relative path name
                cbz.write(file_path, arcname=file)


def process_chapter(chapter_num):
    url = f"https://3asq.online/manga/{MANGA_SLUG}/{chapter_num}/"
    print(f"\n[+] Processing Chapter {chapter_num}: {url}")

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 404:
            print(f"[!] Chapter not found (404): {url}")
            return
        elif response.status_code != 200:
            print(f"[!] Server returned status code: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, "html.parser")
        container = soup.find("div", class_="reading-content")

        if not container:
            print("[!] Could not find '.reading-content' container on page.")
            return

        images = container.find_all("img")
        print(f"[+] Found {len(images)} images.")

        # Temporary folder for raw images
        temp_dir = f"temp_chapter_{chapter_num}"
        os.makedirs(temp_dir, exist_ok=True)

        for idx, img in enumerate(images, start=1):
            img_url = extract_image_url(img)
            if not img_url:
                continue

            ext = img_url.split(".")[-1].split("?")[0]
            if ext.lower() not in ["jpg", "jpeg", "png", "webp"]:
                ext = "jpg"

            filename = os.path.join(temp_dir, f"{idx:03d}.{ext}")

            img_data = requests.get(img_url, headers=HEADERS, timeout=10).content
            with open(filename, "wb") as f:
                f.write(img_data)

        # Build output directory
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        cbz_filename = f"chapter_{chapter_num}.cbz"
        cbz_destination = os.path.join(OUTPUT_DIR, cbz_filename)

        # Compress to .cbz directly
        print(f"  [-] Packaging to CBZ: {cbz_destination}")
        convert_to_cbz(temp_dir, cbz_destination)

        # Clean up temporary raw images folder
        shutil.rmtree(temp_dir)
        print(f"  [✓] Successfully created: {cbz_filename}")

    except Exception as e:
        print(f"  [!] Exception encountered: {e}")


if __name__ == "__main__":
    for chap in range(START_CHAPTER, END_CHAPTER + 1):
        process_chapter(chap)