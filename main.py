"""Main module of the project.

This module provides functionality to read URLs from a file, process
them for downloading Anime content, and write results back to the file.

Usage:
    To use this module, ensure that 'URLs.txt' is present in the same
    directory as this script. Execute the script to read URLs, download
    content, and clear the URL list upon completion.
"""

from __future__ import annotations

import asyncio

from anime_downloader import parse_arguments, process_anime_download
from src.config import URLS_FILE
from src.file_utils import read_file, write_file
from src.general_utils import clear_terminal


async def process_urls(urls: list[str], custom_path: str | None = None) -> None:
    """Validate and downloads items for a list of URLs."""
    for url in urls:
        await process_anime_download(url, custom_path=custom_path)


def parse_urls(lines: list[str]) -> list[str]:
    """Parse URLs, ignoring blank lines and comments introduced by '#'."""
    urls = []
    for line in lines:
        url = line.partition("#")[0].strip()
        if url:
            urls.append(url)
    return urls


async def main() -> None:
    """Run the script."""
    # Clear terminal and parse arguments
    clear_terminal()
    args = parse_arguments(common_only=True)

    urls = parse_urls(read_file(URLS_FILE))
    await process_urls(urls, custom_path=args.custom_path)

    # Clear URLs file
    write_file(URLS_FILE)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nDownload interrupted by the user")
