/*
   pulse.c

   gcc -o pulse pulse.c -lpigpio -lrt -lpthread

   sudo ./pulse
*/

#include <stdio.h>
#include <pigpio.h>


int main(int argc, char *argv[])
{
   double start;
   int pin = 20;
   int val = -1;
   int i = 0;

   if (gpioInitialise() < 0)
   {
      fprintf(stderr, "pigpio initialisation failed\n");
      return 1;
   }

   /* Set GPIO modes */
   gpioSetMode(pin, PI_INPUT);


//    start = time_time();

//    while ((time_time() - start) < 60.0)
//    {
//       gpioWrite(18, 1); /* on */

//       time_sleep(0.5);

//       gpioWrite(18, 0); /* off */

//       time_sleep(0.5);

//       /* Mirror GPIO24 from GPIO23 */
//       gpioWrite(24, );
//    }
    for(i = 0; i < 1000; i++) {
        printf("%d: %d\n", i, gpioRead(pin));
    }

    

   /* Stop DMA, release resources */
   gpioTerminate();

   return 0;
}