import requests
import os
import logging
import time


#VARS
counter = 0
mb_counter = 0

#Connect credential
credentials_src=('orthanc', 'orthanc')
credentials_dst=('orthanc', 'orthanc')

url_src = "http://172.16.0.33:8042/studies/"
url_dst = "http://172.16.0.33:8043/instances"

#logging
logging.basicConfig(level=logging.INFO, filename="log_.log", filemode="a+",
                    format="%(asctime)s %(levelname)s %(message)s")

#Program code
try:
    response_src = requests.get(url_src, auth=credentials_src)
    response_dst = requests.get(url_dst, auth=credentials_dst)
except requests.exceptions.RequestException:
    logging.error("Connection error, check your server or parameters")
    raise SystemExit    
else:
    #get how much file on server
    num_all_studies = len(response_src.json())
    #get file one by one
    logging.info("Connected to Server \n")
    for item in response_src.json():
        response_src_get = requests.get(f"{url_src}{item}/archive", auth=credentials_src)
        with open(f"{item}.zip", "wb") as file:
            file.write(response_src_get.content)
            #Get file size
            file_stats = os.stat(f"{item}.zip")
            logging.info(f"File {item}.zip {round(file_stats.st_size/(1024*1024))}MB -> down done")

        #Rend file
        with open(f"{item}.zip", "rb") as file:
            response_dst_post = requests.post(url_dst, data=file, auth=credentials_dst)  
            logging.info(f"File {item}.zip {round(file_stats.st_size/(1024*1024))}MB -> send done")
            # MB summ
            mb_counter = mb_counter + round(file_stats.st_size/(1024*1024))
        
        #Remove tmp_local file
        if os.path.exists(f"{item}.zip"):
            os.remove(f"{item}.zip")

        #DELETE SRC FILE !!! WARNING !!! BEE CAREFULL
        # response_src_get = requests.delete(f"{url_src}{item}", auth=credentials_src)
        # logging.info(f"File {item}.zip WAS DELETED FROM SRC\n")

        #Show progression
        counter = counter+1
        print(f'\rProgress {response_src.json().index(item)+1} from {num_all_studies}', end='', flush=True)

finally:
    logging.info(f"Script work done, {counter} files processed, Send {mb_counter} MB")
               