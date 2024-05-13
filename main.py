import os
import asyncio
from pathlib import Path

import httpx

from config import NUM_THREADS, TEXT


ROOT_DIR = Path(__file__).parent.absolute()
DATADIR = os.path.join(ROOT_DIR, "data")
ADDRESS_LIST = os.path.join(DATADIR, "address.txt")
RESULT_LIST = os.path.join(DATADIR, "result.txt")

with open(ADDRESS_LIST, 'r') as file:
    addresses = [addr.strip() for addr in file]


class Holograph:
    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'referer': 'https://eligibility.holograph.foundation/',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }
    
    def __init__(self, index: int, address: str) -> None:
        self.address = address
        self.index = index
        
    async def check_drop(self) -> float:
        try: 
            async with httpx.AsyncClient(headers=self.headers) as session:
                r = await session.get(f"https://eligibility.holograph.foundation/api/eligibility/{self.address}")
                
            amount = 0
            if r.json()['status'] == True:
                amount = float(r.json()['amount'])
                
            print(f"{self.index}){self.address}: {amount}")
            with open(RESULT_LIST, "a") as file:
                file.write(f'{self.address}:{amount}\n')
        except Exception as err:
            print(f"error: {err}")

async def run_script(index: int, address: str) -> None:
    client = Holograph(index, address)
    await client.check_drop()

async def main():
    tasks = []
    for index, addr in enumerate(addresses, start=1):
        task = run_script(index, addr)
        tasks.append(task)

        if len(tasks) == NUM_THREADS:
            await asyncio.gather(*tasks)
            tasks.clear()

    if tasks:
        await asyncio.gather(*tasks)
        
        
if __name__ == '__main__':
    print(f'{TEXT}\n\n')
    
    asyncio.run(main())
    
    print('\n\nThank you for using the software. </3')
    input('\nPress "ENTER" To Exit..')