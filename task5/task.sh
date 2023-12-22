#!/bin/bash

hits=0
misses=0
step=1
numbers=()

RED='\e[31m'
GREEN='\e[32m'
RESET='\e[0m'

while true; do    
    echo "Step: ${step}"
    
    # Generate a random number from 0 to 9
    target_number=${RANDOM: -1}
    
    read -p "Please enter a number from 0 to 9 (q - quit): " user_input
    
    # Check if the user wants to quit
    if [ "${user_input}" == "q" ]; then
        echo "Game over. Quitting..."
        break
    fi
    
    # Validate user input
    if ! [[ "${user_input}" =~ ^[0-9]$ ]]; then
        echo "Invalid input. Please enter a single digit number."
        continue
    fi
    
    # Check if the user guessed the number
    if [ "${user_input}" -eq "${target_number}" ]; then
        echo "Hit! My number: ${target_number}"
        ((hits++))
		numbers+=("${GREEN}${target_number}${RESET}")
    else
        echo "Miss! My number: ${target_number}"
        ((misses++))
		numbers+=("${RED}${target_number}${RESET}")
    fi
    
    # Display game statistics
    let hit_percentage=$((hits * 100 / step))
    let miss_percentage=$((misses * 100 / step))
    
    echo "Hit: ${hit_percentage}% Miss: ${miss_percentage}%"
    
	len=${#numbers[@]}
	if (( len < 10 )); then
		echo -e "Numbers: ${numbers[@]}\n"
	else 
		echo -e "Numbers: ${numbers[@]: -10}\n"
	fi
	
	((step++))
done