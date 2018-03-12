# import sys
import timeit
import numpy as np
import cv2

import gi
from gi.repository import Gst, GObject, GstBase
gi.require_version('Gst', '1.0')
Gst.init(None)
from .gst_hacks import map_gst_buffer, get_buffer_size

GST_BLUR_FILTER = 'gstblurfilter'


def grayscale(img):   
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def gaussian_blur(img, kernel_size, sigma=(1, 1)):    
    sigmaX, sigmaY = sigma
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), sigmaX=sigmaX, sigmaY=sigmaY)


class GstBlurFilter(GstBase.BaseTransform):

    __gstmetadata__ = ("GstBlurFilter",
                       "gstblurfilter.py",
                       "gst.Element blurs image buffer",
                       "LifeStyleTransfer")

    __gsttemplates__ = (Gst.PadTemplate.new("src",
                                            Gst.PadDirection.SRC,
                                            Gst.PadPresence.ALWAYS,
                                            Gst.Caps.new_any()),
                        Gst.PadTemplate.new("sink",
                                            Gst.PadDirection.SINK,
                                            Gst.PadPresence.ALWAYS,
                                            Gst.Caps.new_any()))
    
    def __init__(self):
        super(GstBlurFilter, self).__init__()  

    def do_transform(self, inbuffer, outbuffer):

        success, (width, height) = get_buffer_size(self.srcpad.get_current_caps())
       
        with map_gst_buffer(inbuffer, Gst.MapFlags.READ) as mapped:
            frame = np.ndarray((height, width, 4), buffer=mapped, dtype=np.uint8)

        # YOUR IMAGE PROCESSING FUNCTION
        # BEGIN

        frame = gaussian_blur(frame, 25, sigma=(10, 10))

        # END

        refcount = outbuffer.mini_object.refcount
        outbuffer.mini_object.refcount = 1

        with map_gst_buffer(outbuffer, Gst.MapFlags.READ | Gst.MapFlags.WRITE) as mapped:
            out = np.ndarray((height, width, 4), buffer=mapped, dtype=np.uint8)
            out[:] = frame

        outbuffer.mini_object.refcount += refcount - 1 
      
        return Gst.FlowReturn.OK


def register(plugin):
    type_to_register = GObject.type_register(GstBlurFilter)
    Gst.Element.register(plugin, GST_BLUR_FILTER, 0, type_to_register)       
    return True


def register_by_name(plugin_name):
    
    # Parameters explanation
    # https://lazka.github.io/pgi-docs/Gst-1.0/classes/Plugin.html#Gst.Plugin.register_static
    version, gstlicense = '12.06', 'LGPL'
    origin = ''
    source, package = 'gstblurfilter.py', 'gstblurfilter'
    description = "gst.Element blurs image buffer"
    if not Gst.Plugin.register_static(Gst.VERSION_MAJOR, Gst.VERSION_MINOR,
                                      plugin_name, description,
                                      register, version, gstlicense,
                                      source, package, origin):
        raise ImportError("Plugin {} not registered".format(plugin_name)) 
    return True

register_by_name(GST_BLUR_FILTER)



# register()

'''
GObject.type_register(GstBlurFilter)
__gstelementfactory__ = (GST_BLUR_FILTER, Gst.Rank.NONE, GstBlurFilter)
'''

'''
if not Gst.Plugin.register_static(Gst.VERSION_MAJOR, Gst.VERSION_MINOR,
                                  GST_BLUR_FILTER, 'test',
                                  register, '12.06', 'LGPL',
                                  'source', 'package', 'origin'):
    raise ImportError("Plugin {} not registered".format(GST_BLUR_FILTER)) 
'''