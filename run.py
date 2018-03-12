
import logging
import traceback

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

GObject.threads_init()
Gst.init(None)

from gst_filter.gstpipeline import GstPipeline
from gst_filter.gstblurfilter import GstBlurFilter

logging.basicConfig(level=0)

video_file_name = '/home/taras/Downloads/data_ai_videos/video0008.mpg'
command = 'filesrc location={} ! '.format(video_file_name)
command += 'decodebin ! '
command += 'videoconvert ! '
command += 'gstblurfilter ! '
command += 'gtksink '

pipeline = GstPipeline(command)
pipeline.start()

loop = GObject.MainLoop()

try:
    loop.run()
except:
    traceback.print_exc()

pipeline.stop()