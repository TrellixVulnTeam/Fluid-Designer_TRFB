'''
Created on Jul 25, 2016
Common Unit Conversion Functions
@author: Andrew
'''
import bpy

def inch(inch):
    """ Converts inch to meter
    """
    return round(inch / 39.3700787,6) #METERS

def millimeter(millimeter):
    """ Converts millimeter to meter
    """
    return millimeter * .001 #METERS

def meter_to_inch(meter):
    """ Converts meter to inch
    """
    return round(meter * 39.3700787,4)

def meter_to_millimeter(meter):
    """ Converts meter to millimeter
    """
    return meter * 1000

def meter_to_active_unit(meter):
    """ Converts meter to active unit
    """
    if bpy.context.scene.unit_settings.system == 'METRIC':
        return meter_to_millimeter(meter)
    else:
        return meter_to_inch(meter)