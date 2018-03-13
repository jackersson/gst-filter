
import logging
import traceback

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


# TODO argparse filename
video_file_name = '/home/taras/Downloads/data_ai_videos/video0008.mpg'

# Build pipeline
# filesrc https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gstreamer-plugins/html/gstreamer-plugins-filesrc.html
# decodebin https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-base-plugins/html/gst-plugins-base-plugins-decodebin.html
# videoconvert https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-base-plugins/html/gst-plugins-base-plugins-videoconvert.html
# gtksink https://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-good/html/gst-plugins-good-plugins-gtksink.html
command = 'filesrc location={} ! '.format(video_file_name)
command += 'decodebin ! '
command += 'videoconvert ! '
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