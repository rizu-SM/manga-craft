import os
import time
import zipfile
import shutil
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Load .env file from root folder (manga_craft/.env)
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# Fetch output directory from environment variable or default to output folder
OUTPUT_DIR = os.getenv("OUTPUT_DIR")
if not OUTPUT_DIR:
    OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
else:
    OUTPUT_DIR = Path(OUTPUT_DIR)

os.makedirs(OUTPUT_DIR, exist_ok=True)

URL_TEMPLATE = "https://mangadar.com/manga/kingdom/{}"
START_CHAPTER = 185
END_CHAPTER = 200


def extract_image_url(img):
    """Checks multiple possible data attributes used for lazy loading."""
    attrs = ["src", "data-src", "data-lazy-src", "data-full-url", "data-url"]
    for attr in attrs:
        url = img.get_attribute(attr)
        if url and not url.startswith("data:image"):
            return url.strip()
    return None


def create_cbz(temp_dir: Path, output_cbz_path: Path):
    """Compresses all image files in temp_dir into a .cbz archive."""
    image_files = sorted(
        [f for f in temp_dir.iterdir() if f.is_file() and f.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]]
    )

    if not image_files:
        print(f"  [!] No downloaded images found to package into {output_cbz_path.name}.")
        return False

    with zipfile.ZipFile(output_cbz_path, "w", zipfile.ZIP_DEFLATED) as cbz:
        for img_path in image_files:
            cbz.write(img_path, arcname=img_path.name)

    print(f"  [✓] Successfully created CBZ archive: {output_cbz_path}")
    return True


def process_chapter(page, chapter_num):
    url = URL_TEMPLATE.format(chapter_num)
    print(f"\n[+] Processing Chapter {chapter_num}: {url}")

    cbz_filename = f"Kingdom_Chapter_{chapter_num:03d}.cbz"
    output_cbz_path = OUTPUT_DIR / cbz_filename

    if output_cbz_path.exists():
        print(f"  [i] Chapter {chapter_num} already exists at {output_cbz_path}. Skipping.")
        return

    temp_dir = Path(__file__).resolve().parent.parent / f"temp_chapter_{chapter_num}"

    try:
        response = page.goto(url, wait_until="domcontentloaded", timeout=30000)

        if response and response.status == 404:
            print(f"  [!] Chapter not found (404): {url}")
            return

        page.wait_for_selector("div.reader-page", timeout=15000)
        img_elements = page.query_selector_all("div.reader-page img")
        print(f"  [+] Found {len(img_elements)} image elements.")

        if not img_elements:
            print("  [!] No images found in DOM.")
            return

        # FORCE HYDRATION: Scroll directly to each image element individually
        print("  [+] Hydrating image elements via viewport scrolling...")
        for img in img_elements:
            img.scroll_into_view_if_needed()
            time.sleep(0.05)

        time.sleep(1)

        os.makedirs(temp_dir, exist_ok=True)
        downloaded_count = 0

        for idx, img in enumerate(img_elements, start=1):
            img_url = extract_image_url(img)

            if not img_url:
                print(f"    [!] Skipping image {idx}: No valid URL found.")
                continue

            if img_url.startswith("//"):
                img_url = "https:" + img_url

            ext = img_url.split(".")[-1].split("?")[0]
            if ext.lower() not in ["jpg", "jpeg", "png", "webp"]:
                ext = "jpg"

            filename = os.path.join(temp_dir, f"{idx:03d}.{ext}")

            img_response = page.context.request.get(img_url)
            if img_response.ok:
                with open(filename, "wb") as f:
                    f.write(img_response.body())
                downloaded_count += 1
            else:
                print(f"    [!] Failed to fetch image {idx} (Status {img_response.status}): {img_url}")

        print(f"  [+] Downloaded {downloaded_count}/{len(img_elements)} images.")

        # Step 2: Package into .cbz archive
        success = create_cbz(temp_dir, output_cbz_path)

        if not success and output_cbz_path.exists():
            output_cbz_path.unlink()

    except Exception as e:
        print(f"  [!] Exception encountered: {e}")

    finally:
        # Step 3: Cleanup temporary directory
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    print(f"[+] Output directory set to: {OUTPUT_DIR.resolve()}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        )
        page = context.new_page()

        for chap in range(START_CHAPTER, END_CHAPTER + 1):
            process_chapter(page, chap)

        browser.close()


if __name__ == "__main__":
    main()