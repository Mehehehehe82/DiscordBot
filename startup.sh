#!/bin/sh
clear
while true; do
	python __main__.py
	EXIT=$?
	# echo "---   SHUT DOWN.   ---" | tee -a bot.log
	echo Exited with code ${EXIT}.
	if [ $EXIT \> 0 ]; then
		exit
	fi
	sleep 3
	clear
done
