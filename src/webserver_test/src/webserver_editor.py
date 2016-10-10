#!/usr/bin/env python
import rospy,re
from navigation_api.msg import navigation_msg
from std_msgs.msg import String

lat=" "
long=" "
def string_parse(gps_str):
    global lat
    global lng
    lat=re.findall('(.*?)%',gps_str)
    lng=re.findall('%(.*?)@',gps_str)
    current_location_tuple = (float(lat[0]),float(lng[0]))
    return current_location_tuple

def heading_callback(data):
    f=open('/var/www/index.html')
    print "heading callback received"
#    if f.closed:	
    #print "heading me fclosed"
    lines = f.readlines()
    f.close()
    r=open('/var/www/index.html','w')
    r.writelines([item for item in lines[:-1]])
    r.close()
    w=open('/var/www/index.html','a')
    w.write("<b>Start point:</b>"+data.start_point+'<br>')
    w.write("<b>Destination:</b>"+data.destination+'<br>')
    w.write("<b>Target Heading:</b>"+str(data.target_heading)+'<br>')
    w.write('\n</body></html>')
    w.close()
""" else:
    while f.closed is 0:
    print "Hurry up, heading is waiting"
"""
def coord_callback(data):
    print "coord callback received"
    parsed=string_parse(data.data)
    f=open('/var/www/index.html')
   #if f.closed:
    #print "coord me fclosed"
    lines = f.readlines()
    f.close()
    r=open('/var/www/index.html','w')
    r.writelines([item for item in lines[:-1]])
    r.close()
    w=open('/var/www/index.html','a')
    w.write("<b>Current Destination: </b>"+str(parsed)+'<br>'+'<br>')
    w.write('\n</body></html>')
    w.close()

def initializer():
    rospy.init_node('webedit')
    rospy.Subscriber("gpsLocation", String, coord_callback)
    rospy.Subscriber("navigation_api_data",navigation_msg,heading_callback)
    rospy.spin()

if __name__ == '__main__':
    f=open('/var/www/index.html','w')
    f.write('<html><body><h1>Anveshan Data logging test</h1>\n')
    f.write('<br></body></html>')
    f.close()
    initializer()
