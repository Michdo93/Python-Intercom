import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst, GObject
import RPi.GPIO as GPIO

BUTTON_PIN1 = 17  # GPIO-Pin für den Audio-Taster
BUTTON_PIN2 = 18  # GPIO-Pin für den Video-Taster

class Intercom:
    def __init__(self, target_ip):
        Gst.init(None)

        self.pipeline = Gst.Pipeline()

        # Audio-Elemente
        self.asrc = Gst.ElementFactory.make("alsasrc", "audio-source")
        self.audioconvert = Gst.ElementFactory.make("audioconvert", "audio-convert")
        self.audioresample = Gst.ElementFactory.make("audioresample", "audio-resample")
        self.speexenc = Gst.ElementFactory.make("speexenc", "speex-enc")
        self.rtpspeexpay = Gst.ElementFactory.make("rtpspeexpay", "rtp-speex-pay")
        self.udpsink = Gst.ElementFactory.make("udpsink", "udp-sink")
        self.udpsrc = Gst.ElementFactory.make("udpsrc", "udp-source")
        self.rtpjitterbuffer = Gst.ElementFactory.make("rtpjitterbuffer", "rtp-jitterbuffer")
        self.rtpspeexdepay = Gst.ElementFactory.make("rtpspeexdepay", "rtp-speex-depay")
        self.speexdec = Gst.ElementFactory.make("speexdec", "speex-dec")
        self.audioconvert2 = Gst.ElementFactory.make("audioconvert", "audio-convert2")
        self.audioresample2 = Gst.ElementFactory.make("audioresample", "audio-resample2")
        self.tee = Gst.ElementFactory.make("tee", "tee")
        self.queue1 = Gst.ElementFactory.make("queue", "queue1")
        self.queue2 = Gst.ElementFactory.make("queue", "queue2")
        self.sink = Gst.ElementFactory.make("autoaudiosink", "audio-sink")

        # Video-Elemente
        self.vsrc = Gst.ElementFactory.make("v4l2src", "video-source")
        self.videoconvert = Gst.ElementFactory.make("videoconvert", "video-convert")
        self.videoscale = Gst.ElementFactory.make("videoscale", "video-scale")
        self.videorate = Gst.ElementFactory.make("videorate", "video-rate")
        self.x264enc = Gst.ElementFactory.make("x264enc", "x264-enc")
        self.rtph264pay = Gst.ElementFactory.make("rtph264pay", "rtp-h264-pay")
        self.udpsink2 = Gst.ElementFactory.make("udpsink", "udp-sink2")
        self.udpsrc2 = Gst.ElementFactory.make("udpsrc", "udp-source2")
        self.rtpjitterbuffer2 = Gst.ElementFactory.make("rtpjitterbuffer", "rtp-jitterbuffer2")
        self.rtph264depay = Gst.ElementFactory.make("rtph264depay", "rtp-h264-depay")
        self.avdec_h264 = Gst.ElementFactory.make("avdec_h264", "av-dec-h264")
        self.videoconvert2 = Gst.ElementFactory.make("videoconvert", "video-convert2")
        self.queue3 = Gst.ElementFactory.make("queue", "queue3")
        self.queue4 = Gst.ElementFactory.make("queue", "queue4")
        self.sink2 = Gst.ElementFactory.make("autovideosink", "video-sink")

        if not self.pipeline or not self.asrc or not self.audioconvert or not self.audioresample \
                or not self.speexenc or not self.rtpspeexpay or not self.udpsink or not self.udpsrc \
                or not self.rtpjitterbuffer or not self.rtpspeexdepay or not self.speexdec \
                or not self.audioconvert2 or not self.audioresample2 or not self.tee or not self.queue1 \
                or not self.queue2 or not self.sink or not self.vsrc or not self.videoconvert \
                or not self.videoscale or not self.videorate or not self.x264enc or not self.rtph264pay \
                or not self.udpsink2 or not self.udpsrc2 or not self.rtpjitterbuffer2 or not self.rtph264depay \
                or not self.avdec_h264 or not self.videoconvert2 or not self.queue3 or not self.queue4 \
                or not self.sink2:
            print("Failed to create elements.")
            exit(1)

        self.pipeline.add(self.asrc)
        self.pipeline.add(self.audioconvert)
        self.pipeline.add(self.audioresample)
        self.pipeline.add(self.speexenc)
        self.pipeline.add(self.rtpspeexpay)
        self.pipeline.add(self.udpsink)
        self.pipeline.add(self.udpsrc)
        self.pipeline.add(self.rtpjitterbuffer)
        self.pipeline.add(self.rtpspeexdepay)
        self.pipeline.add(self.speexdec)
        self.pipeline.add(self.audioconvert2)
        self.pipeline.add(self.audioresample2)
        self.pipeline.add(self.tee)
        self.pipeline.add(self.queue1)
        self.pipeline.add(self.queue2)
        self.pipeline.add(self.sink)
        self.pipeline.add(self.vsrc)
        self.pipeline.add(self.videoconvert)
        self.pipeline.add(self.videoscale)
        self.pipeline.add(self.videorate)
        self.pipeline.add(self.x264enc)
        self.pipeline.add(self.rtph264pay)
        self.pipeline.add(self.udpsink2)
        self.pipeline.add(self.udpsrc2)
        self.pipeline.add(self.rtpjitterbuffer2)
        self.pipeline.add(self.rtph264depay)
        self.pipeline.add(self.avdec_h264)
        self.pipeline.add(self.videoconvert2)
        self.pipeline.add(self.queue3)
        self.pipeline.add(self.queue4)
        self.pipeline.add(self.sink2)

        self.asrc.link(self.audioconvert)
        self.audioconvert.link(self.audioresample)
        self.audioresample.link(self.speexenc)
        self.speexenc.link(self.rtpspeexpay)
        self.rtpspeexpay.link(self.udpsink)
        self.udpsrc.link(self.rtpjitterbuffer)
        self.rtpjitterbuffer.link(self.rtpspeexdepay)
        self.rtpspeexdepay.link(self.speexdec)
        self.speexdec.link(self.audioconvert2)
        self.audioconvert2.link(self.audioresample2)
        self.audioresample2.link(self.tee)
        self.tee.link(self.queue1)
        self.tee.link(self.queue2)
        self.queue1.link(self.sink)
        self.queue2.link(self.sink2)

        self.vsrc.link(self.videoconvert)
        self.videoconvert.link(self.videoscale)
        self.videoscale.link(self.videorate)
        self.videorate.link(self.x264enc)
        self.x264enc.link(self.rtph264pay)
        self.rtph264pay.link(self.udpsink2)
        self.udpsrc2.link(self.rtpjitterbuffer2)
        self.rtpjitterbuffer2.link(self.rtph264depay)
        self.rtph264depay.link(self.avdec_h264)
        self.avdec_h264.link(self.videoconvert2)
        self.videoconvert2.link(self.queue3)
        self.queue3.link(self.queue4)
        self.queue4.link(self.sink2)

        self.udpsrc.set_property("port", 6666)
        self.udpsrc2.set_property("port", 6667)
        self.udpsink.set_property("host", target_ip)
        self.udpsink.set_property("port", 6666)
        self.udpsink2.set_property("host", target_ip)
        self.udpsink2.set_property("port", 6667)

        self.pipeline.set_state(Gst.State.PLAYING)

        # GPIO-Setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_PIN1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BUTTON_PIN2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(BUTTON_PIN1, GPIO.RISING, callback=self.audio_button_callback, bouncetime=200)
        GPIO.add_event_detect(BUTTON_PIN2, GPIO.RISING, callback=self.video_button_callback, bouncetime=200)

    def audio_button_callback(self, channel):
        print("Audio button pressed!")
        self.tee.set_state(Gst.State.NULL)
        self.queue1.set_state(Gst.State.NULL)
        self.queue2.set_state(Gst.State.PLAYING)

    def video_button_callback(self, channel):
        print("Video button pressed!")
        self.tee.set_state(Gst.State.PLAYING)
        self.queue1.set_state(Gst.State.PLAYING)
        self.queue2.set_state(Gst.State.NULL)

    def run(self):
        loop = GObject.MainLoop()
        try:
            loop.run()
        except KeyboardInterrupt:
            pass

        self.pipeline.set_state(Gst.State.NULL)
        GPIO.cleanup()

if __name__ == "__main__":
    target_ip = "<Ziel-IP>"  # IP-Adresse des Zielgeräts eintragen
    intercom = Intercom(target_ip)
    intercom.run()
