# The file to put on AWS Lambda
import requests
import re
import json
import io
from zipfile import ZipFile
import asyncio
import aiohttp

async def fetch(session, url):
    async with session.get(url) as resp:
        return await resp.read()

async def get_image_data(image_urls):
    # get all images via async
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(len(image_urls)):
            url = image_urls[i]
            task = asyncio.ensure_future(fetch(session, url))
            tasks.append(task)
        return await asyncio.gather(*tasks)

def lambda_handler(event, context):
    site = event["site"]
    html = requests.get(site)

    # match the images and replace them with higher quality ones
    # match pages.push("xxx/500x711.jpg")
    image_urls = re.findall("pages\.push\(\"(.*)500x711\.jpg\"\)", html.text)
    image_urls = [url + "1080x1536.jpg" for url in image_urls]

    if not image_urls:
        return

    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    try:
        image_data = loop.run_until_complete(get_image_data(image_urls))
    finally:
        loop.close()

    with io.BytesIO() as flo:
        # ignore compression for now
        with ZipFile(flo, 'w') as z:
            z.filename = 'images.zip'
            for i in range(len(image_data)):
                image_datum = image_data[i]
                z.writestr("{}.jpg".format(i), image_datum)
    
        upload_site = "https://0x0.st"
    
        upload_response = requests.post(upload_site, files={'file': flo.getvalue()})

    return {
        'body': json.dumps(upload_response.text)
    }
