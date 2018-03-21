
import os
import logging
import traceback
import argparse 

# Required imports 
# Gst, GstBase, GObject
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

# Init Gobject Threads
# Init Gstreamer
GObject.threads_init()
Gst.init(None)

from gst_filter.gstpipeline import GstPipeline
from gst_filter.gstblurfilter import GstBlurFilter

# Set logging level=DEBUG
logging.basicConfig(level=0)

# How to use argparse:
# https://www.pyimagesearch.com/2018/03/12/python-argparse-command-line-arguments/
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", required=True, help="Path to video file")
ap.add_argument("-b", "--blur", action='store_true', help="ON/OFF blur filter")
args = vars(ap.parse_args())


file_name = os.path.abspath(args['file'])
if not os.path.isfile(file_name):
    raise ValueError('File {} not exists'.format(file_name))

use_blur_filter = args['blur']

# Build pipeline
# filesrc https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gstreamer-plugins/html/gstreamer-plugins-filesrc.html
# decodebin https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-base-plugins/html/gst-plugins-base-plugins-decodebin.html
# videoconvert https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-base-plugins/html/gst-plugins-base-plugins-videoconvert.html
# gtksink https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-good/html/gst-plugins-good-plugins-gtksink.html
command = 'filesrc location={} ! '.format(file_name)
command += 'decodebin ! '
command += 'videoconvert ! '
if use_blur_filter:
    command += 'gstblurfilter ! '
    command += 'videoconvert ! '
command += 'gtksink '

pipeline = GstPipeline(command)
pipeline.start()

# Init GObject loop to handle Gstreamer Bus Events
loop = GObject.MainLoop()

try:
    loop.run()
except:
    traceback.print_exc()

pipeline.stop()