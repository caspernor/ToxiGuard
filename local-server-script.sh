#!/bin/bash

WATCHED_DIR="/home/aske1304/Patient_Data"
DEST_USER="aske"
DEST_IP="192.168.3.11"
DEST_DIR="/home/aske/Desktop/ToxiGuard"
MOVE_TO_DIR="/home/aske1304/backup"
COUNTER_FILE="/home/aske1304/counter.txt"

if [ -e "$COUNTER_FILE" ]; then
    counter=$(<"$COUNTER_FILE")
else
    counter=1
fi

inotifywait -m "$WATCHED_DIR" -e create -e moved_to |
while read path action file; do
    echo "The file '$file' appeared in directory '$path' via '$action'"
    
    file_numbered="patient_data$counter.csv"
    image_numbered="patient_image$counter.jpg"
    sleep 5

    if scp "$WATCHED_DIR/$file" "$DEST_USER@$DEST_IP:$DEST_DIR/$file_numbered" &&
       scp "$WATCHED_DIR/patient_image.jpg" "$DEST_USER@$DEST_IP:$DEST_DIR/$image_numbered"; then
       
        echo "Transfer successful, moving $file to $MOVE_TO_DIR"    
        mv "$WATCHED_DIR/$file" "$MOVE_TO_DIR/$file_numbered"
        mv "$WATCHED_DIR/patient_image.jpg" "$MOVE_TO_DIR/$image_numbered"

        ((counter++))
        echo "$counter" > "$COUNTER_FILE"
        sleep 5  
    else
        echo "Transfer failed, not moving $file"
    fi
done
