import ntplib
import time


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
    if int(year) % 4 == 0:
        sec_in_one_month = (366/12)*86400
        total_sec_in_month = month * sec_in_one_month
    else:
        sec_in_one_month = (365/12)*86400
        total_sec_in_month = month * sec_in_one_month
    return total_sec_in_month
    
def xxx(x=0):
    return time.strftime("%Y.%m.%d", time.localtime(actual_time_from_net() - month_to_second(x))) 


print(actual_time_from_net())
print(month_to_second(6))
print(xxx(6))

import requests



#x = requests.get('http://172.16.0.33:8042/studies', auth=('orthanc', 'orthanc'))

url = "http://172.16.0.33:8042/studies/923023e3-9ac5fc61-1188d4fd-34d3c6c3-516584ee/archive"
x = requests.get(url , auth=('orthanc', 'orthanc'))

url_arch = "http://172.16.0.33:8043/instances"
file_name = "image.zip"

with open("image.zip", "wb") as file:
        file.write(x.content)



#response = requests.post(url_arch, files={'file': (file_name, open(file_name, 'rb'))}, auth=('orthanc', 'orthanc'))

#with open(file_name, 'rb') as send_file:
#    response = requests.post(url_arch, data=send_file.read(), auth=('orthanc', 'orthanc'))



#print(x.json())

#sent file to server
#curl -X POST http://localhost:8042/instances --data-binary @multiple-files.zip

#delete file from server
#curl -X DELETE http://localhost:8042/instances/8e289db9-0e1437e1-3ecf395f-d8aae463-f4bb49fe