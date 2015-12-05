/**
 * The MySensors Arduino library handles the wireless radio link and protocol
 * between your home built sensors/actuators and HA controller of choice.
 * The sensors forms a self healing radio network with optional repeaters. Each
 * repeater and gateway builds a routing tables in EEPROM which keeps track of the
 * network topology allowing messages to be routed to nodes.
 *
 * Created by Henrik Ekblad <henrik.ekblad@mysensors.org>
 * Copyright (C) 2013-2015 Sensnology AB
 * Full contributor list: https://github.com/mysensors/Arduino/graphs/contributors
 *
 * Documentation: http://www.mysensors.org
 * Support Forum: http://forum.mysensors.org
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * version 2 as published by the Free Software Foundation.
 *
 *******************************

/*************** SETTINGS ***************/

// Enable debug prints
//#define MY_DEBUG

{% if radio is equalto 'NRF24' %}
// Enable and select radio type attached
#define MY_RADIO_NRF24
{% endif %}

{% if not no_repeater %}
// Enabled repeater feature for this node
#define MY_REPEATER_FEATURE
{% endif %}

#include <SPI.h>
#include <MySensor.h>

/********* SKETCH SETTINGS ********/
#define SKETCH_NAME     "{{ name }}"
#define SKETCH_VERSION  "{{ version }}"
/**********************************/

/******** SENSORS SETTINGS *******/
#define CHILD_A  1  // childId
/**********************************/

/*********** END SETTINGS ***************/

MyMessage msg(CHILD_A, V_VAR1);

void setup(){
    // Setup locally attached sensors
}

void presentation(){
    /*
     * This function is called at the start of the node
     * and every time the node receives an I_PRESENTATION message.
     * You must present all your node's child here
     */

    // Send the sketch version information to the gateway and Controller
    sendSketchInfo(SKETCH_NAME, SKETCH_VERSION);

    // Register a sensors to  Use binary light for test purposes.
    present(CHILD_A, S_LIGHT);
}

void loop(){
    // Send locally attached sensor data here
}

void receive(const MyMessage &message) {
    /*
     * This function is called every time the node receives an message.
     * So, it is here that you must filter your messages and decide how to react.
     * Enjoy and becareful! With great power comes great responsabilities!
     */
}