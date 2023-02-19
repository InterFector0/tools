#!/bin/bash

while getopts u: flag
do
    case "${flag}" in
        u) url=${OPTARG};;
    esac
done
clear
echo URL is: $url
echo -------------------------------------------
echo
echo Which wordlist to use?
echo 1\) common.txt
echo 2\) BIG.txt
echo 

read num
if [ $num == 1 ]; then
	wordlist="/usr/share/dirb/wordlists/common.txt"

elif [ $num == 2 ]; then
	wordlist="/usr/share/dirb/wordlists/big.txt"
fi

clear
echo Wordlist being used: $wordlist
echo
test_for_tor="$(netstat -na | grep 9050)"
if [ -n $test_for_tor ]
then
	gobuster dir -u $url -w $wordlist -x php,json,txt,yml,csv -s 200,301,403 -b "" -k --no-progress --no-error --random-agent --proxy socks5://127.0.0.1:9050 > 'tty'
else
	tor&
	clear
	gobuster dir -u $url -w $wordlist -x php,json,txt,yml,csv -s 200,301,403 -b "" -k --no-progress --no-error --random-agent --proxy socks5://127.0.0.1:9050
fi



