#echo $(($1+1))

scanimage -d pixma:04A91827_2A949A --resolution 300 --format png >images/$1.png
convert images/$1.png -rotate 180 images/$1.png
python clinterface.py -i $1.png -s 0 -r 1
read -p "Press enter to scan page $(($1+1))"
scanimage -d pixma:04A91827_2A949A --resolution 300 --format png >images/$(($1+1)).png
python clinterface.py -i $(($1+1)).png -s 0 -r 1
