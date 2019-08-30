import tornado.httpserver
import tornado.websocket
import tornado.ioloop
from tornado.ioloop import PeriodicCallback
import tornado.web
import RPi.GPIO as GPIO
import time, os, datetime, dht11

try:
    # initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()

    # read data using pin 14
    instance = dht11.DHT11(pin=20)
    class WSHandler(tornado.websocket.WebSocketHandler):
        def open(self):
            self.callback = PeriodicCallback(self.send_temp, 120)
            self.callback.start()

        def send_hello(self):
            self.write_message('hello')

        def on_message(self, message):
            pass

        def on_close(self):
            self.callback.stop()
            print( "Closed Connection")

        def send_temp(self):
            result = instance.read()
            if result.is_valid():
                print("Last valid input: " + str(datetime.datetime.now()))
                print("Temperature: %d C" % result.temperature)
                print("Humidity: %d %%" % result.humidity)
                self.write_message("Last valid input: " + str(datetime.datetime.now()))
                self.write_message("Temperature: %d C" % result.temperature)
                self.write_message("Humidity: %d %%" % result.humidity)
            
            time.sleep(2)


    application = tornado.web.Application([(r'/', WSHandler),])

    if __name__ == "__main__":
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(9999)
        tornado.ioloop.IOLoop.instance().start()

except KeyboardInterrupt:
    print('\nSaliendo...')
    GPIO.cleanup()
    os._exit(0)