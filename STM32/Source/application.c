#include "main.h"

#include <stdio.h>

#include "cmsis_os.h"
#include "version.h"

void Application_RunDefaultTask(void)
{
	int32_t array[5] = {65535};
	int16_t calculate = 0;
	
    printf("image_id: %d, version: %d.%d.%d-%s\n", (int) IMAGE_ID, (int) VERSION_MAJOR, (int) VERSION_MINOR, (int) VERSION_BUGFIX, SHORT_GIT_HASH_STRING);

    printf("First and last values: %ld, %ld\n", array[0], array[5]);

    calculate = array[0] + 20;
    printf("Calculated value: %hd\n", calculate);
    
	for(;;)
	{
		osDelay(1000);
	}
}

void Application_RunLedTask(void)
{
	for (;;)
	{
		HAL_GPIO_TogglePin(LD3_GPIO_Port, LD3_Pin);
		osDelay(500);
	}
}
