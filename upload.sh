#!/bin/bash
#For start script you need use few params.
#like ./upload.sh ip user pass ./path_to_folder_with_files
#
#./upload.sh 127.0.0.1:8042 alice alice /tmp/data


COUNTER=0
TOTAL_FILE=$(find $4 -type f | wc -l)


if [ $# -ne 4 ]
then
	echo "Error in params, pls check it !"
else
	CODE_STATUS=$(curl -i $1 --user $2:$3 2> /dev/null | grep HTTP | awk '{print $2}')
	if [ -z $CODE_STATUS ] ||[ $CODE_STATUS -gt 400 ] || [ $CODE_STATUS -lt 200 ] 
	then
		echo "Connect error !!!"
	else
		for file in $(find $4 -type f)
		do
			if [ -f "$file" ]
			then
				STATUS=$(/usr/bin/curl -X POST $1/instances --data-binary @$file --user "$2:$3" 2> /dev/null | grep "Status" | awk '{print $3}')
				COUNTER=$((COUNTER+1))	
				echo "File upload : $COUNTER/$TOTAL_FILE ---> $STATUS"
			fi
		done
	fi
fi