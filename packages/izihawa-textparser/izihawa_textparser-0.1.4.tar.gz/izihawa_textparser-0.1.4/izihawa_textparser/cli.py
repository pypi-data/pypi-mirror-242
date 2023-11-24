import asyncio
import json
import os

import aiofiles
import fire
from aiokit import MultipleAsyncExecution
from aiobaseclient import BaseClient
from izihawa_netlib import ClientPool
from izihawa_utils.file import yield_files

from ._grobid import GrobidParser


async def process_file(sciparse, filepath, target_dir):
    async with aiofiles.open(filepath, "rb") as f:
        processed_document = await sciparse.parse_paper(await f.read())
        target_filepath = os.path.join(
            target_dir, os.path.basename(filepath).removesuffix(".pdf") + ".txt"
        )
        async with aiofiles.open(
            target_filepath,
            "w",
        ) as output:
            r = await asyncio.get_running_loop().run_in_executor(
                None, lambda: json.dumps(processed_document)
            )
            print("writing", target_filepath)
            await output.write(r)


async def grobid(
    source_dir: str,
    target_dir: str,
    grobid_endpoint: str = "http://127.0.0.1:8070",
    threads: int = 32,
):
    executor = MultipleAsyncExecution(threads)

    grobid_client_1 = BaseClient(grobid_endpoint)
    await grobid_client_1.start()

    client_pool = ClientPool([(grobid_client_1, threads)])
    sciparse = GrobidParser(client_pool)

    for filepath in yield_files(f'{source_dir.rstrip("/")}/*'):
        await executor.execute(process_file(sciparse, filepath, target_dir))

    await executor.join()


def run():
    fire.Fire(grobid)
