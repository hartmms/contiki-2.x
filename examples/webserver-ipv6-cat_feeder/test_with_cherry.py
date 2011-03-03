#! /usr/bin/env python

import socket, sys
import os
from operator import itemgetter
localDir = os.path.dirname(__file__)
curpath = os.path.normpath(os.path.join(os.getcwd(), localDir))

import cherrypy
#import cherrypy.lib.auth_basic
#from cherrypy.process.plugins import Daemonizer
#Daemonizer(cherrypy.engine).subscribe()
class renderpage(object):
   main_ip = '192.168.0.55'
   rx_port = 50010
   tx_port = 50011
   status_image = {'closed':'<img src="images/closed.png" alt="closed">', 
                   'open':'<img src="images/open.png" alt="open">'}
   time = "0:00"
   feed_time = "0:30"
   motor_time = "5"
   mac_addr = "11:22:33:44:55:66:77:88"

   def index(self):
      yield self.header()
      yield '<form name="feedem" action="cat" method="get">'
      yield '    <input type=hidden name=feed value="1">'
      yield '    <input type="submit" value="Feed Them Now"> '
      yield '</form>'
      yield '<hr>'
      yield '<form name="time_form" action="cat_feeder" method="get" onSubmit="return checkTOD()">'
      yield '    Set current time (hh:mm in 24 hour time) '
      yield '    <input type="text" name="time" value="%s" size="15" maxlength="40"/>' % self.time
      yield '    <input type="submit" value="Save"/>'      
      yield '</form>'
      yield '<form name="feed_time_form" action="cat_feeder" method="get" onSubmit="return checkFeedTime()">'
      yield '    Time of day to feed (hh:mm in 24 hour time) '
      yield '    <input type="text" name="feed_time" value="%s" size="15" maxlength="40"/>' % self.feed_time
      yield '    <input type="submit" value="Save"/>'      
      yield '</form>'
      yield '<form name="motor_time_form" action="cat_feeder" method="get" onSubmit="return checkMotorTime()">'
      yield '    Length of time (in seconds) to operate motor '
      yield '    <input type="text" name="motor_time" value="%s" size="2" maxlength="2"/>' % self.motor_time
      yield '    <input type="submit" value="Save"/>'
      yield '</form>'
      yield '<hr>'
      yield '<form name="mac_addr_form" action="cat_feeder" method="get" onSubmit="return checkMac()">'
      yield '    <p>MAC address'
      yield '    <input type="text" name="mac_addr" value="%s" size="30" maxlength="40">' % self.mac_addr
      yield '    <input type="submit" value="Save"></p>'
      yield '</form>'
      yield self.footer()
   index.exposed = True


   def cat_feeder(self,time=None,motor_time=None,mac_addr=None,feed=None,feed_time=None):
      yield self.header()
      if feed:
          yield 'Feed commenced'
      if time:
          yield 'Time set: %s<br>' % time
          self.time = time
      if feed_time:
          yield 'Feed Time set: %s<br>' % feed_time
          self.feed_time = feed_time
      if motor_time:
          yield 'Motor time set: %s<br>' % motor_time
          self.motor_time = motor_time
      if mac_addr:
          yield 'MAC address set: %s<br>' % mac_addr
          self.mac_addr = mac_addr
      yield self.footer()
   cat_feeder.exposed = True

   def other_cgi(self,Name=None,Sex=None):
       yield "Ok"
   other_cgi.exposed = True;

   def status_shtml(self):
      yield self.header()
      yield '<p>status page</p>'
      yield self.footer()
   status_shtml.exposed = True

   def header(self):
      header_text = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">'
      header_text += '<html><head><title>The Hartman\'s IPv6 cat feeder!</title>'
      header_text += '<link rel="stylesheet" type="text/css" href="/style.css"><link rel="icon" href="wifi.png" type="image/png">'
      header_text += '<script>'

      header_text += 'function checkMac() {'
      header_text += ' var valid_addr=/^[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}$/;'
      header_text += ' if (valid_addr.test(document.mac_addr_form.mac_addr.value)) {'
      header_text += '  var agree=confirm("Are you sure you want to change the MAC address");'
      header_text += '  if (agree) {'
      header_text += '   document.mac_addr_form.mac_addr.value = document.mac_addr_form.mac_addr.value.replace(/:/g,"");'
      header_text += '   return true;'
      header_text += '  } else {'
      header_text += '   return false;'
      header_text += '  }'
      header_text += ' } else {'
      header_text += '  alert("Please enter a valid 8 octet number for the mac address");'
      header_text += '  return false;'
      header_text += ' }'
      header_text += '}'

      header_text += 'function checkTOD() {'
      header_text += ' var valid_time=/^[0-9]{1,2}:[0-9]{2}$/;'
      header_text += ' if (!valid_time.test(document.time_form.time.value)) {'
      header_text += '  alert("Please enter a valid time in xx:xx format");'
      header_text += '  return false;'
      header_text += ' } else {'
      header_text += '  document.time_form.time.value = document.time_form.time.value.replace(/:/g,"");'
      header_text += '  return true;'
      header_text += ' }'
      header_text += '}'

      header_text += 'function checkFeedTime() {'
      header_text += ' var valid_time=/^[0-9]{1,2}:[0-9]{2}$/;'
      header_text += ' if (!valid_time.test(document.feed_time_form.feed_time.value)) {'
      header_text += '  alert("Please enter a valid time in xx:xx format");'
      header_text += '  return false;'
      header_text += ' } else {'
      header_text += '  document.feed_time_form.feed_time.value = document.feed_time_form.feed_time.value.replace(/:/g,"");'
      header_text += '  return true;'
      header_text += ' }'
      header_text += '}'

      header_text += 'function checkMotorTime(motor_time) {'
      header_text += ' var valid_motor_time=/^[0-9]$/;'
      header_text += ' if (!valid_motor_time.test(document.motor_time_form.motor_time.value)) {'
      header_text += '  alert("Please enter a single digit for the motor run time");'
      header_text += '  return false;'
      header_text += ' } else {'
      header_text += '  return true;'
      header_text += ' }'
      header_text += '}'

      header_text += '</script>'
      header_text += '</head>'
      header_text += '<body bgcolor="#474747" text="black">'
      header_text += '  <div class="menublock">'
      header_text += '    <div class="menu">'
      header_text += '      <p class="border-title">Status</p>'
      header_text += '      <p class="menu">'
      header_text += '	<a href="/">Main Page</a><br>'
      header_text += '	<a href="status.shtml">Status</a><br>'
      header_text += '  </div>'
      header_text += '  </div>'
      header_text += '  <div class="contentblock">'
      header_text += '    <p class="border-title">Welcome to the Hartman\'s IPv6 cat feeder!</p>'
      return header_text

   def footer(self):
      footer_text = '</div></body></html>'
      return footer_text

conf = { 'global' : {
              "tools.sessions.on": True, 
              "tools.sessions.timeout": 5 },
   '/favicon.ico': {
       'tools.staticfile.on': True, 
       'tools.staticfile.filename': '/media/av/ep/6loWpan/contiki-2.x/examples/webserver-ipv6-cat_feeder/cat_feeder/wifi.png'},
   '/style.css': {
       'tools.staticfile.on': True, 
       'tools.staticfile.filename': '/media/av/ep/6loWpan/contiki-2.x/examples/webserver-ipv6-cat_feeder/cat_feeder/style.css'},
  }
conf['global']['server.socket_host'] = '192.168.0.69'
conf['global']['server.socket_port'] = 8080
conf['global']['log.screen'] = True
conf['global']['log.access_file'] = "/tmp/cherry_access.log"
conf['global']['log.error_file'] = "/tmp/cherry_error.log"
cherrypy.quickstart(renderpage(), '/', config=conf)
