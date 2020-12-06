import os
with os.scandir("/var/challenge/") as dirFiles:
  for dirFile in dirFiles:
    f = open(dirFile.name + "_flag_commands.txt", "w")
    f.write("""#!/bin/bash
# script used to automate retrieval of flags from challenges

for i in /var/challenge/*; do 
  echo $i
  rm dictionary.txt
  ln -s $i/flag dictionary.txt
  output=`timeout 1s $i/dict -p flag`
  if [[ $output == *"flag: "* ]]; then
    parsed=${output#*flag:}
  elif [[ $output == *"flag - "* ]]; then
    parsed=${output#*flag -}
  elif [[ $output == *"flag{"* ]]; then
    parsed=${output#*flag{}
    parsed=${parsed::-1}
  elif [[ $output == *"flag "* ]]; then
    parsed=${output#*flag}
  else
    parsed=$output
  fi

  if [[ ! -z "$parsed" ]]; then
    challenge_id=${i##*/}
    parsed=${parsed## }
    parsed=${parsed%% }
    echo "FLAG: $parsed"
    echo $parsed > "flags/${challenge_id}_flag.txt"
  fi
done
    """)
    f.close()