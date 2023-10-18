#echo $(($1+1))

scanimage -d pixma:04A91827_2A949A --resolution 300 --format png >images/$1.png
convert images/$1.png -rotate 180 images/$1.png
read -p "Press enter to scan page $(($1+1))"
scanimage -d pixma:04A91827_2A949A --resolution 300 --format png >images/$(($1+1)).png

