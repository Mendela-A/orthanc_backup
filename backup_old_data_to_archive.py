import ntplib
import time
import logging
import requests


#VARS
#Set period of time
MONTH = 6

#Connect credential
credentials=('orthanc', 'orthanc')
url = "http://172.16.0.33:8042/studies/"


#logging
logging.basicConfig(level=logging.INFO, filename="transfer_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")


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
    DATA_STR = time.strftime("%Y.%m.%d", time.localtime(actual_time_from_net() - month_to_second(MONTH))) 
except Exception:    
    logging.error("Connection error, check your server or parameters")
    raise SystemExit  
else:
    data = {
    "Level": "Study",
    "Query": {
        "StudyDate": f"{DATA_STR}",
        "PatientID": "*"
            }
    }
    request = requests.get(url, auth=credentials, verify=False)
    for item in request.json():
        request1 = requests.get(f"{url}{item}", auth=credentials, verify=False)
        print(f"{item} ---> {request1.json()['PatientMainDicomTags']['PatientName']}")
        


finally:
    logging.info("End. Scripts work done")



# #x = requests.get('http://172.16.0.33:8042/studies', auth=('orthanc', 'orthanc'))

# url = "http://172.16.0.33:8042/studies/923023e3-9ac5fc61-1188d4fd-34d3c6c3-516584ee/archive"
# x = requests.get(url , auth=('orthanc', 'orthanc'))

# url_arch = "http://172.16.0.33:8043/instances"
# file_name = "image.zip"

# with open("image.zip", "wb") as file:
#         file.write(x.content)



#response = requests.post(url_arch, files={'file': (file_name, open(file_name, 'rb'))}, auth=('orthanc', 'orthanc'))

#with open(file_name, 'rb') as send_file:
#    response = requests.post(url_arch, data=send_file.read(), auth=('orthanc', 'orthanc'))



#print(x.json())

#sent file to server
#curl -X POST http://localhost:8042/instances --data-binary @multiple-files.zip

#delete file from server
#curl -X DELETE http://localhost:8042/instances/8e289db9-0e1437e1-3ecf395f-d8aae463-f4bb49fe



# import requests
# from urllib3.exceptions import InsecureRequestWarning

# data = {
#     "Level": "Study",
#     "Query": {
#         "StudyDate": "20230501",
#         "PatientID": "*"
#     }
# }

# # Suppress the warnings from urllib3
# requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# req = requests.get('https://kt-data.crh.local/studies', auth=('KT', 'kt2022'), verify=False)
# counter = 0
# for item in req.json():
#     counter = counter + 1
# print(f'{counter} Founded studies')



# def finder():
#     req_ = requests.post('https://kt-data.crh.local/tools/find', auth=('KT', 'kt2022'), verify=False, json=data)
#     count = 0
#     for item in req_.json():
#         count = count+1
#         #print(item)

#     print(f'Founded {count} Studies - functions info')

# finder()
