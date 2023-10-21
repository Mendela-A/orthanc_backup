# orthanc_backup
backup scripts

1) from_a_to_b.py - Simle copy all data from ServerA to ServerB, it is possible dele src data.
2) upload.sh - Copy all file from NAS to Orthanc srv
3) backup_old_data_to_archive.py - Script copy all data than older tnan X-MONTH (date we get from NTP)
              from serA to srvB, then delete src file.
4) mt_five_y - This scrip just delete old data and log it. Data we get from NTP.
