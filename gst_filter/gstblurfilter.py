import timeit
import numpy as np
import cv2

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')
from gi.repository import Gst, GObject, GstBase

# Gst.init(None)

from .gst_hacks import map_gst_buffer, get_buffer_size
from .cv_utils import gaussian_blur

import skimage.io

GST_BLUR_FILTER = 'gstblurfilter'


def _write(message, filename, mode):
    with open(filename, mode) as handle:
        handle.write(message) 


class GstBlurFilter(GstBase.BaseTransform):

    CHANNELS = 3  # RGB 

    __gstmetadata__ = ("GstBlurFilter",
                       "gstblurfilter.py",
                       "gst.Element blurs image buffer",
                       "LifeStyleTransfer.com")

    __gsttemplates__ = (Gst.PadTemplate.new("src",
                                            Gst.PadDirection.SRC,
                                            Gst.PadPresence.ALWAYS,
                                            Gst.Caps.from_string("video/x-raw,format=RGB")),
                        Gst.PadTemplate.new("sink",
                                            Gst.PadDirection.SINK,
                                            Gst.PadPresence.ALWAYS,
                                            Gst.Caps.from_string("video/x-raw,format=RGB")))
    
    def __init__(self):
        super(GstBlurFilter, self).__init__()  

    def do_transform(self, inbuffer, outbuffer):
        """
            Implementation of simple filter.
            Inbuffer, outbuffer are different buffers, so 
            manipulations with inbuffer not affects outbuffer

            Read more:
            https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gstreamer-libs/html/GstBaseTransform.html
        """

        success, (width, height) = get_buffer_size(self.srcpad.get_current_caps())
        if not success:
            # https://lazka.github.io/pgi-docs/Gst-1.0/enums.html#Gst.FlowReturn
            return Gst.FlowReturn.ERROR
       
        with map_gst_buffer(inbuffer, Gst.MapFlags.READ) as mapped:
            frame = np.ndarray((height, width, self.CHANNELS), buffer=mapped, dtype=np.uint8)

        # YOUR IMAGE PROCESSING FUNCTION
        # BEGIN

        frame = gaussian_blur(frame, 25, sigma=(10, 10))

        # END

        # HACK: force the query to be writable by messing with the refcount
        # https://bugzilla.gnome.org/show_bug.cgi?id=746329
        refcount = outbuffer.mini_object.refcount
        outbuffer.mini_object.refcount = 1

        with map_gst_buffer(outbuffer, Gst.MapFlags.READ | Gst.MapFlags.WRITE) as mapped:
            out = np.ndarray((height, width, self.CHANNELS), buffer=mapped, dtype=np.uint8)
            # Assign processed IN np.array to OUT np.array
            out[:] = frame

        # HACK: decrement refcount value
        outbuffer.mini_object.refcount += refcount - 1 
      
        return Gst.FlowReturn.OK


def register(plugin):
    # https://lazka.github.io/pgi-docs/#GObject-2.0/functions.html#GObject.type_register
    type_to_register = GObject.type_register(GstBlurFilter)

    # https://lazka.github.io/pgi-docs/#Gst-1.0/classes/Element.html#Gst.Element.register
    Gst.Element.register(plugin, GST_BLUR_FILTER, 0, type_to_register)       
    return True


def register_by_name(plugin_name):
    
    # Parameters explanation
    # https://lazka.github.io/pgi-docs/Gst-1.0/classes/Plugin.html#Gst.Plugin.register_static
    version, gstlicense = '12', 'LGPL'
    origin = 'LifeStyleTransfer'
    source, package = 'gstblurfilter.py', 'gstblurfilter'
    description = "gst.Element blurs image buffer"
    if not Gst.Plugin.register_static(Gst.VERSION_MAJOR, Gst.VERSION_MINOR,
                                      plugin_name, description,
                                      register, version, gstlicense,
                                      source, package, origin):
        raise ImportError("Plugin {} not registered".format(plugin_name)) 
    return True

register_by_name(GST_BLUR_FILTER)