import ntplib
import time
import logging
import requests
import os


#VARS
#Set period of time
MONTH = 8
mb_counter = 0
counter = 0

#Connect credentials
credentials_src=('orthanc', 'orthanc')
url_src = "http://172.16.0.33:8042"

credentials_dst=('orthanc', 'orthanc')
url_dst = "http://172.16.0.33:8043"

#logging
logging.basicConfig(level=logging.INFO, filename="transfer_log.log", filemode="a+",
                    format="%(asctime)s %(levelname)s %(message)s")

# # Suppress the warnings from urllib3
# requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def actual_time_from_net():
    """Get actual time from internet"""
    client = ntplib.NTPClient()
    response = client.request('ua.pool.ntp.org', version=3)
    # Forming date string, by default we get time in seconds
    return response.tx_time


def month_to_second(month=0):
    """Conver mont to second"""
    seconds = 0
    #Get year from network
    year = time.strftime("%Y", time.localtime(actual_time_from_net()))
    #Chech day of year 356 or 366
    if int(year) % 4 == 0:
        sec_in_one_month = (366/12)*86400
        total_sec_in_month = month * sec_in_one_month
    else:
        sec_in_one_month = (365/12)*86400
        total_sec_in_month = month * sec_in_one_month
    #Return total count of seconds
    return total_sec_in_month
    

#Gettin time string for search request, if get error just stop programm
#and record warninng msg to log file

try:
    logging.info("Starting ... ")
    DATA_STR = time.strftime("%Y%m%d", time.localtime(actual_time_from_net() - month_to_second(MONTH)))
except Exception:    
    logging.error("Connection error, check your server or parameters")
    raise SystemExit  
else:
    #Json request
    data = {
    "Level": "Study",
    "Query": {
        "StudyDate": f"-{DATA_STR}",
        "PatientID": "*"
        }
    }
    request_src = requests.post(f"{url_src}/tools/find", auth=credentials_src, verify=False, json=data)
    for item in request_src.json():
    #get file one by one
        response_src_get = requests.get(f"{url_src}/studies/{item}/archive", auth=credentials_src)
        with open(f"{item}.zip", "wb") as file:
            file.write(response_src_get.content)
            #Get file size
            file_stats = os.stat(f"{item}.zip")
            logging.info(f"File {item}.zip {round(file_stats.st_size/(1024*1024))}MB -> down done")
        
        #Send file
        with open(f"{item}.zip", "rb") as file:
            response_dst_post = requests.post(f"{url_dst}/instances", data=file, auth=credentials_dst)  
            logging.info(f"File {item}.zip {round(file_stats.st_size/(1024*1024))}MB -> send done")
            # MB summ
            mb_counter = mb_counter + round(file_stats.st_size/(1024*1024))
        
        #Remove tmp_local file
        if os.path.exists(f"{item}.zip"):
            os.remove(f"{item}.zip")

        #DELETE SRC FILE !!! WARNING !!! BEE CAREFULL
        # response_src_delete = requests.delete(f"{url_src}/studies/{item}", auth=credentials_src)
        # logging.info(f"File {item}.zip WAS DELETED FROM SRC")   

        #Show progression
        counter = counter+1    

finally:
    logging.info(f"Script work done, {counter} files processed, Send {mb_counter} MB\n")