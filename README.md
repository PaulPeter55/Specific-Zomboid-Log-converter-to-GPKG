# Specific-Zomboid-Log-converter-to-GPKG

The program converts the log file "EtsarsPositionLogger" into a GPKG file that can be used in QGIS.

Usage:

- create a folder called "logs" beside this file where you deposit all the logs
- Add excluded players to excluded_users_Username.
- Change world_epoch to the world's start date.
- Add the y_Offset you plan to use for georeferencing.
- Since this uses game coordinates, the missing CRS will not cause any issues.
