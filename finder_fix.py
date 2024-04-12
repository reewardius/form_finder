# python finder_fix.py -l file.txt
# python finder_fix.py -d https://example.com

import aiohttp
import asyncio
import sys
from bs4 import BeautifulSoup
from aiohttp.client_exceptions import ClientConnectorCertificateError

# ANSI escape codes for colors
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

async def fetch(session, url):
    try:
        async with session.get(url) as response:
            return await response.text(), url
    except ClientConnectorCertificateError:
        print(f"{RED}SSL Certificate Error: Unable to verify certificate for {url}{RESET}")
        return None, url
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None, url

async def process_url(session, url):
    html, url = await fetch(session, url)
    if html:
        soup = BeautifulSoup(html, "html.parser")
        forms = soup.find_all("form")
        text_inputs = soup.find_all("input", type="text")
        if forms or text_inputs:
            print(GREEN + f"Form Found at {url}" + RESET)
        else:
            print(RED + f"Form Not Found at {url}" + RESET)

async def main(input_source, is_list):
    urls = []
    if is_list:
        with open(input_source, "r") as file:
            urls = [line.strip() for line in file]
    else:
        urls = [input_source]

    async with aiohttp.ClientSession() as session:
        tasks = [process_url(session, url) for url in urls]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <-l filename|-d url>")
        sys.exit(1)
    input_flag = sys.argv[1]
    input_source = sys.argv[2]
    
    is_list = False
    if input_flag == "-l":
        is_list = True
    elif input_flag == "-d":
        is_list = False
    else:
        print("Invalid flag. Use -l for file or -d for single domain.")
        sys.exit(1)
        
    asyncio.run(main(input_source, is_list))
