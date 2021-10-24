#include <iostream>
#include <unistd.h>
#include <math.h>
#include "src/ina219.h"

// kulick
#include <stdio.h>
#include <time.h>
#define TENMILLION 10000000
#define ONEMILLION 1000000
#define ONEBILLION 1000000000
time_t rawtime;
struct timespec finetime;
long int val_old;
long int sec_old;
long int ns_old;
long int val;
long int sec;
long int ns;
int repetition = 0;
// end kulick

int main(int argc, char *argv[])
{
    int opt;

	float SHUNT_OHMS = 0.1;
	float MAX_EXPECTED_AMPS = 3.2;
    float INITIAL_CHARGE = 15000.0;
    float INTERVAL = 1000.0;

    bool profile_enabled = false;

    while ((opt = getopt(argc, argv, ":r:a:e:t:p")) != -1)
    {
        switch (opt) {
        case 'r':
            SHUNT_OHMS = atof(optarg);
            break;
        case 'a':
            MAX_EXPECTED_AMPS = atof(optarg);
            break;
        case 'e':
            INITIAL_CHARGE = atof(optarg);
            break;
        case 't':
            INTERVAL = atof(optarg);
            break;
        case 'p':
            profile_enabled = true;
            break;
        default: /* '?' */
            fprintf(stderr, "Usage: %s [-r shunt_resistance_ohms] [-a max_expected_amps] [-e initial_charge_coulombs] [-t update_interval_millisec] [-p]\n"
            "\t -r resistance\t the resistance of the shunt resistor in Ohms\n"
            "\t -a current\t the maximum expected current in the system, in Amperes\n"
            "\t -e charge\t initial charge of the battery in Coulombs, only useful if not using -p\n"
            "\t -t interval\t the interval to pull info from the sensor in milliseconds\n"
            "\t -p\t\t profiles the battery\n"
            "Equivalent to no arguments: %s -r 0.1 -a 3.2 -e 15000 -t 1000\n",
                    argv[0]);
            return 1;
        }
    }

    if (profile_enabled)
    {
        INA219 i(SHUNT_OHMS, MAX_EXPECTED_AMPS);
        i.configure(RANGE_16V, GAIN_8_320MV, ADC_12BIT, ADC_12BIT);

//kulick

        std::cout << "NS_ABS, time_s,current_mA,power_mW" << std::endl;

        int c = 0;

// get the start time of the loop

 clock_gettime(CLOCK_REALTIME, &finetime);
  val_old  = finetime.tv_nsec;
  sec_old =  finetime.tv_sec;
  ns_old  = val_old + ONEBILLION*sec_old;
  ns      = ns_old;
// end kulick

        while(true)
        {
            float current = i.current();
//kulick
            std::cout << ns << ","
                    << (roundf(c*(INTERVAL/1000.0) * 1000) / 1000) << ","
                    << (roundf(current * 1000) / 1000) << ","
                    << (roundf(i.power() * 100) / 100) << ","
                    << std::endl;
            c++;
// kulick

 // wait until 10 ms has passed
 // get the current time
 while((ns - ns_old) <= TENMILLION)
 {
 clock_gettime(CLOCK_REALTIME, &finetime);
  val = finetime.tv_nsec;
  sec =  finetime.tv_sec;
  ns   = val + ONEBILLION*sec;
 }

 ns_old = ns;




            //usleep(INTERVAL * 1000);
// end kulick
        }
    } else {

// kulick

// get the start time of the loop

 clock_gettime(CLOCK_REALTIME, &finetime);
  val_old  = finetime.tv_nsec;
  sec_old =  finetime.tv_sec;
  ns_old  = val_old + ONEBILLION*sec_old;
  ns      = ns_old;
// end kulick



        float remaining_charge = INITIAL_CHARGE;
        INA219 i(SHUNT_OHMS, MAX_EXPECTED_AMPS);
        i.configure(RANGE_16V, GAIN_8_320MV, ADC_12BIT, ADC_12BIT);
//kulick
        std::cout << "NS_ABS, time_s,current_mA,power_mW" << std::endl;
        int c = 0;


// kulick
        while(true)
        {
            float current = i.current();
//kulick
//            remaining_charge = remaining_charge - ( (current/1000.0) * (INTERVAL/1000.0) );
 //           float percentage = (100.0*remaining_charge) / INITIAL_CHARGE;
            std::cout << ns << ","
                    << (roundf(c*(INTERVAL/1000.0) * 1000) / 1000) << ","
                    << (roundf(current * 1000) / 1000) << ","
                    << (roundf(i.power() * 100) / 100) << "," << std::endl;
            c++;
// kulick


 while((ns - ns_old) <= TENMILLION)
 {
 clock_gettime(CLOCK_REALTIME, &finetime);
  val = finetime.tv_nsec;
  sec =  finetime.tv_sec;
  ns   = val + ONEBILLION*sec;
 }

 ns_old = ns;


}


            //usleep(INTERVAL * 1000);

 //  end kulick
      }





//            usleep(INTERVAL * 1000);

	return 0;
}
