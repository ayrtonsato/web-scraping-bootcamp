import logging
import os

from httpx import get
from selectolax.parser import HTMLParser


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_response_for(keyword, results_per_page, page=1):
    """Search images"""
    url = f"https://unsplash.com/napi/search/photos?query={keyword}&per_page={results_per_page}&page={page}"

    resp = get(url)

    if resp.status_code == 200:
        return resp.json()


def get_image_urls(data: list[str]) -> list[str]:
    results = data["results"]
    img_urls = [x["urls"]["raw"] for x in results if x["premium"] is False]
    img_urls = [x.split("?")[0] for x in img_urls]

    return img_urls


def download_images(img_urls, max_download, dest_dir="images", tag=""):
    successfully_downloaded = 0

    for url in img_urls:
        if successfully_downloaded < max_download:
            resp = get(url)
            file_name = url.split("/")[-1]

            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            with open(f"{dest_dir}/{tag}{file_name}.jpeg", "wb") as f:
                f.write(resp.content)
                successfully_downloaded = 1

        else:
            break

        return successfully_downloaded


def scrape(keyword, num_of_results):
    start_page = 1
    success_count = 0

    while success_count < num_of_results:
        data = get_response_for(keyword, results_per_page=20, page=start_page)
        max_downloads = num_of_results - success_count

        if data:
            img_urls = get_image_urls(data)
            success_downloads = download_images(
                img_urls, max_downloads, tag=keyword
            )
            success_count += success_downloads
            start_page += 1
        else:
            print("Error: no data returned")
            break


if __name__ == "__main__":
    scrape("snowboarding", 3)
