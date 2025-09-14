import requests
import os
from urllib.parse import urlparse
from hashlib import md5

def get_filename_from_url(url, content=None):
    """
    Extract a filename from the URL or generate one from content hash.
    """
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)

    if not filename and content:
        # Use content hash to generate a unique filename
        hash_name = md5(content).hexdigest()[:10]
        filename = f"image_{hash_name}.jpg"

    elif not filename:
        filename = "downloaded_image.jpg"

    return filename


def fetch_images(urls):
    """
    Download and save images from a list of URLs.
    Ensure you avoid duplicates and check safety precautions.
    """
    folder = "Fetched_Images"
    os.makedirs(folder, exist_ok=True)

    downloaded_hashes = set()

    for url in urls:
        print(f"\nFetching from: {url}")
        try:
            # Fetch with headers (to simulate polite request)
            headers = {"User-Agent": "UbuntuFetcher/1.0 (Respectful Web Client)"}
            response = requests.get(url, timeout=10, headers=headers)
            response.raise_for_status()

            # Safety check: Content-Type should be image
            content_type = response.headers.get("Content-Type", "")
            if not content_type.startswith("image/"):
                print(f"✗ Skipped (not an image): {url}")
                continue

            # Prevent duplicate downloads
            content_hash = md5(response.content).hexdigest()
            if content_hash in downloaded_hashes:
                print("✗ Duplicate detected, skipping.")
                continue
            downloaded_hashes.add(content_hash)

            # Generate filename
            filename = get_filename_from_url(url, response.content)
            filepath = os.path.join(folder, filename)

            # Save image
            with open(filepath, "wb") as f:
                f.write(response.content)

            print(f"✓ Successfully fetched: {filename}")
            print(f"✓ Image saved to {filepath}")

        except requests.exceptions.RequestException as e:
            print(f"✗ Connection error: {e}")
        except Exception as e:
            print(f"✗ An error occurred: {e}")

    print("\nConnection strengthened. Community enriched.")


def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Get multiple URLs from user
    urls = input("Please enter one or more image URLs (comma-separated): ").split(",")
    urls = [url.strip() for url in urls if url.strip()]

    if urls:
        fetch_images(urls)
    else:
        print("✗ No URLs provided.")


if __name__ == "__main__":
    main()
