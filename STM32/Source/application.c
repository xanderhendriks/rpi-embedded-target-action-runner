//! @file application.c

// Interface for this file
#include "application.h"

// Standard library includes
#include <stdio.h>
#include <stdbool.h>

// Library includes
#include "cmsis_os.h"

// Application includes
#include "main.h"
#include "version.h"
#include "sensor.h"

static bool runCalculation = true;

void Application_RunDefaultTask(void)
{
	int16_t calculate = 0;

	printf("image_id: %d, version: %d.%d.%d-%s\n", (int) IMAGE_ID, (int) VERSION_MAJOR, (int) VERSION_MINOR, (int) VERSION_BUGFIX, SHORT_GIT_HASH_STRING);

    if (runCalculation)
    {
    	calculate = Sensor_GetValue() + 20;

		printf("Calculated value: %hd\n", calculate);
    }
    
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
