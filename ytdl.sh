while read text; do
    echo $text
    youtube-dl $text
done < yturl.txt
