# The file to put on AWS Lambda
import requests
import re
import json
import io
from zipfile import ZipFile


def lambda_handler(event, context):
    site = event["site"]
    html = requests.get(site)

    # match the images and replace them with higher quality ones
    # match pages.push("xxx/500x711.jpg")
    image_urls = re.findall("pages\.push\(\"(.*)500x711\.jpg\"\)", html.text)
    image_urls = [url + "1080x1536.jpg" for url in image_urls]
    num_images = len(image_urls)

    if not num_images:
        return

    with io.BytesIO() as flo:
        # ignore compression for now
        with ZipFile(flo, "w") as z:
            z.filename = 'images.zip'
            for i in range(num_images):
                url = image_urls[i]
                image_data = requests.get(url).content
                z.writestr("{}.jpg".format(i), image_data)
    
        upload_site = "https://0x0.st"
    
        upload_response = requests.post(upload_site, files={'file': flo.getvalue()})

    return {
        'body': json.dumps(upload_response.text)
    }
