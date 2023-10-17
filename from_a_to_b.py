import requests
import os
import logging

credentials=('orthanc', 'orthanc')

url_from = "http://172.16.0.33:8042/studies/"
url_to = "http://172.16.0.33:8044/instances"

#logging
logging.basicConfig(level=logging.INFO, filename="log.txt", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

response = requests.get(url_from, auth=credentials)

if response.status_code == 200:
    logging.info("Connected to Server")
    for item in response.json():
        #get file one by one
        if True:
            response_get = requests.get(f"{url_from}{item}/archive", auth=credentials)
            with open(f"{item}.zip", "wb") as file:
                file.write(response_get.content)
        else:
            logging.error(f"{item}.zip <- Write error")
        
        #send file
        if True:
            with open(f"{item}.zip", "rb") as file:
                response_post = requests.post(url_to, data=file, auth=credentials)  
        else:
            logging.error(f"{item}.zip <- Send error")

        #remove file
        if os.path.exists(f"{item}.zip"):
            os.remove(f"{item}.zip")
        else:
            logging.error(f"File {item}.zip does not exist")
    logging.info("Job done")
else:
    logging.critical("Connect not complete !!!")



