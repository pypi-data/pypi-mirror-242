# Trust Platform Design Suite - Usecase Help - Quarklink Connect

This document helps to understand Pre and Post steps of Usecase transaction diagram.

## Setup requirements
 - [DM320118](https://www.microchip.com/developmenttools/ProductDetails/DM320118)
 - [WIFI 7 CLICK](https://www.mikroe.com/wifi-7-click)
 - [MPLAB X IDE](https://www.microchip.com/en-us/development-tools-tools-and-software/mplab-x-ide) 5.45 or above

## Pre Usecase transaction Steps
 - Connect DM320118 board to PC running Trust Platform Design Suite
 - Ensure *MPLAB X Path* is set in *File* -> *Preference* under *System Settings*. This helps
    - To program the Usecase prototyping kit to factory reset application by TPDS
    - To open the embedded project of the Usecase
 - Request for an Instance of Quarklink to be created from Crypto Quantique.
 - Ensure *~/.trustplatform/quarklink_credentials.yaml* contains the account credentials.
    - ~ indicates home directory.
        - Windows home directory is \user\username
        - Mac home directory is /users/username
        - Most Linux/Unix home directory is /home/username
 - Note that *~/.trustplatform/cryptoquantique_quarklink* is the **Usecase working directory**. It contains the resources generated during transaction diagram execution.
 - On older versions of WIFI 7 click boards, It is required to upgrade the WIFI 7 click board firmware.
    - Run the *winc_firmware_update.bat* batch file in *~/.trustplatform/winc_firmware_upgrade*.
        - Note1: This requires [Microchip/Atmel Studio](https://www.microchip.com/en-us/development-tools-tools-and-software/microchip-studio-for-avr-and-sam-devices) installed on the system. It works only on Windows.
        - Note2: Some versions of DM320118 nEDBG firmware fails to upgrade winc software. In such cases, upgrade the firmware to 1.18.528 as below and try running above batch file.
            - Open Microchip Studio Command Prompt, navigate to *~/.trustplatform/winc_firmware_upgrade* folder and run the below command.
                - *atfw -t nedbg -a nedbg_fw-1.18.528.zip*
        - Note3: Winc firmware upgrade process can take a while, wait for it to complete.

## Post Usecase transaction Steps
 - Run the *winc_RootCerts_update.bat* batch file in *~/.trustplatform/winc_firmware_upgrade*.
    - Note1: This requires [Microchip/Atmel Studio](https://www.microchip.com/en-us/development-tools-tools-and-software/microchip-studio-for-avr-and-sam-devices) installed on the system. It works only on Windows.
    - Note2: Some versions of nEDBG firmware fails to upgrade winc software. In such cases, upgrade the firmware to 1.18.528 as below and try running above batch file.
        - Open Microchip Studio Command Prompt, navigate to *~/.trustplatform/winc_firmware_upgrade* folder and run the below command.
            - *atfw -t nedbg -a nedbg_fw-1.18.528.zip*
    - Note3: If Root Certs update batch file fails with "(ERROR) Root Certificate Flash is Full", it is required to remove one/more certs from *winc_firmware_upgrade\firmware\Tools\root_certificate_downloader\binary\ *. User can keep these certs as backup and reload as and when needed. After removing the certs rerun *winc_RootCerts_update.bat* batch file in *~/.trustplatform/winc_firmware_upgrade*

On completing Usecase steps execution on TPDS, it is possible to either run the embedded project or view C source files by clicking *MPLAB X Project* or *C Source Folder* button.

- Once the Usecase project is loaded on MPLAB X IDE,
    - Set the project as Main -> right click on Project and select *Set as Main Project*
    - Set WiFi SSID and Password -> Open *cloud_wifi_config.h* under Project Header Files -> common -> cloud_wifi_config.h.
        - Uncomment and update WLAN_SSID and WLAN_PSK macros with user's wifi SSID and password
    - Set the configuration -> right click on Project, expand *Set Configuration* to select *QUARKLINK_CONNECT*
    - Build and Program the project -> right click on Project and select *Make and Program Device*
- Log from the embedded project can be viewed using applications like TeraTerm. Select the COM port and set baud rate as 115200-8-N-1

Example TeraTerm Log after successfully executing embedded project:

- Connecting to Cloud messages appear along with the led state.

![Quarklink Connect TeraTerm Log](images/aws_ttlog.png "Quarklink Connect TeraTerm Log")
