#echo $(($1+1))

page=$1
if [ ! -f images/$page.png ]; then
    #echo "File not found!"
    scanimage -d pixma:04A91827_2A949A --resolution 300 --format png >images/$page.png
    convert images/$page.png -rotate 180 images/$page.png
    python clinterface.py -i $page.png -s 0 -r 1
fi

read -p "Press enter to scan page $(($1+1))"

page=$(($1+1))
if [ ! -f images/$page.png ]; then
    scanimage -d pixma:04A91827_2A949A --resolution 300 --format png >images/$page.png
    python clinterface.py -i $page.png -s 0 -r 1
fi
