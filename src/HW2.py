__author__ = 'brianuosseph'
import sys
import math
from PIL import Image
from numpy import *

# Completed:
#   xyz (required)
#   trif (requried)
#   Per-pixel clipping (required)
#   color (required)
#   Depth buffer (required)
#   translate (required) [have one implementation that works, but not the best
#
#   cull    (+10)
#   scale   (+5)
#   trig    (+10)
#   rotate  (+5)
#   rotatec (+10)
#   scalec  (+10)
#
# Need:
#   lookat (required)
#   ortho (required)
#   frustum (required)
#   50% extra

class Vertex():
    def __init__(self, _x, _y, _z):
        self.x = _x
        self.y = _y
        self.z = _z
        self.w = 1.
        self.r = 255.
        self.g = 255.
        self.b = 255.
        #self.vector = array([_x, _y, _z, 1.]).reshape(4,1)

    def x(self):
        return (self.x)     # used to divide by w

    def setX(self, x):
        self.x = x

    def y(self):
        return (self.y)     # used to divide by w

    def setY(self, y):
        self.y = y

    def z(self):
        return (self.z)     # used to divide by w

    def setZ(self, z):
        self.z = z

    def w(self):
        return self.w

    def setW(self, w):
        self.w = w

    def vector(self):
        #return self.vector
        vector = array([self.x, self.y, self.z, self.w]).reshape(4,1)
        return vector

    def vector3(self):
        vector = array([self.x, self.y, self.z]).reshape(3,1)
        return vector

    def printVertexInfo(self):
        print "<"+str(self.x)+", "+str(self.y)+", "+str(self.z)+", "+str(self.w)+">"
        #print self.vector

    def setR(self, r):
        self.r = r

    def setG(self, g):
        self.g = g
    def setB(self, b):
        self.b = b

def trif(i1, i2, i3):
    vList = [i1, i2, i3]
    vList.sort(key=lambda v: v.y)   # vList[0] is highest screen; vList[2] is lowest on screen
    #for v in vList :
    #    print v.printVertexInfo()
    #    print str(convertToXPixel(v.x))+" "+str(convertToYPixel(v.y))

    # If direction is positive, vertices are listed counter clockwise
    if cull:
        edge1 = (vList[1].x - vList[0].x)*(vList[1].y + vList[0].y)
        edge2 = (vList[2].x - vList[1].x)*(vList[2].y + vList[1].y)
        edge3 = (vList[0].x - vList[2].x)*(vList[0].y + vList[2].y)
        direction = edge1 + edge2 + edge3
        if direction > 0:
            # Divide by x,y,z by w
            if vList[0].y - vList[2].y != 0:
                if vList[1].y - vList[2].y == 0:

                    if convertToXPixel(vList[1].x) < convertToXPixel(vList[2].x):
                        leftSlope =  float( convertToXPixel(vList[1].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[1].y) - convertToXPixel(vList[0].y) )
                        rightSlope =  float( convertToXPixel(vList[2].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[0].y) )

                        leftX = convertToXPixel(vList[0].x)
                        rightX = convertToXPixel(vList[0].x)

                    else:
                        rightSlope =  float( convertToXPixel(vList[1].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[1].y) - convertToXPixel(vList[0].y) )
                        leftSlope =  float( convertToXPixel(vList[2].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[0].y) )

                        rightX = convertToXPixel(vList[0].x)
                        leftX = convertToXPixel(vList[0].x)


                    #leftSlope =  float( convertToXPixel(vList[1].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[1].y) - convertToXPixel(vList[0].y) )
                    #rightSlope =  float( convertToXPixel(vList[2].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[0].y) )
                    #
                    #leftX = convertToXPixel(vList[0].x)
                    #rightX = convertToXPixel(vList[0].x)

                    # Per-Pixel Clipping
                    ax = convertToXPixel(vList[0].x)
                    ay = convertToYPixel(vList[0].y)
                    bx = convertToXPixel(vList[1].x)
                    by = convertToYPixel(vList[1].y)
                    cx = convertToXPixel(vList[2].x)
                    cy = convertToYPixel(vList[2].y)
                    totalArea = math.fabs(float(ax*(by-cy) + bx*(cy-ay) + cx*(ay-by))/2.)
                    z1 = vList[0].z
                    z2 = vList[1].z
                    z3 = vList[2].z

                    for y in range(convertToYPixel(vList[0].y), convertToYPixel(vList[1].y)):
                        leftX = float(leftX) + leftSlope
                        rightX = float(rightX) + rightSlope
                        for x in range(int(leftX), int(rightX)):
                            # Interpolate z throughout triangle
                            abpArea = math.fabs(float(ax*(by-y) + bx*(y-ay) + x*(ay-by))/2.)
                            apcArea = math.fabs(float(ax*(y-cy) + x*(cy-ay) + cx*(ay-y))/2.)
                            pbcArea = math.fabs(float(x*(by-cy) + bx*(cy-y) + cx*(y-by))/2.)

                            alpha1 = pbcArea/totalArea # for z1
                            alpha2 = apcArea/totalArea # for z2
                            alpha3 = abpArea/totalArea # for z3

                            z = alpha1*z1 + alpha2*z2 + alpha3*z3

                            if x < 0 or x > WIDTH-1 or y < 0 or y > HEIGHT-1:
                                pass
                            elif z < 0. or z > 1.:
                                pass
                            else:
                                if (z < zbuffer[x][y]):
                                    image.putpixel((x,y), getCurrentColor())
                                    zbuffer[x][y] = z

                elif vList[0].y - vList[1].y == 0:
                    print "Triangle has flat top"

                    if convertToXPixel(vList[0].x) < convertToXPixel(vList[1].x):
                        leftSlope =  float( convertToXPixel(vList[2].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[0].y) )
                        rightSlope =  float( convertToXPixel(vList[2].x) - convertToXPixel(vList[1].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[1].y) )
                        leftX = convertToXPixel(vList[0].x)
                        rightX = convertToXPixel(vList[1].x)

                    else:
                        leftSlope =  float( convertToXPixel(vList[2].x) - convertToXPixel(vList[1].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[1].y) )
                        rightSlope =  float( convertToXPixel(vList[2].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[0].y) )
                        leftX = convertToXPixel(vList[1].x)
                        rightX = convertToXPixel(vList[0].x)

                    # Per-Pixel Clipping of Z:
                    ax = convertToXPixel(vList[0].x)
                    ay = convertToYPixel(vList[0].y)
                    bx = convertToXPixel(vList[1].x)
                    by = convertToYPixel(vList[1].y)
                    cx = convertToXPixel(vList[2].x)
                    cy = convertToYPixel(vList[2].y)
                    totalArea = math.fabs(float(ax*(by-cy) + bx*(cy-ay) + cx*(ay-by))/2.)
                    z1 = vList[0].z
                    z2 = vList[1].z
                    z3 = vList[2].z

                    for y in range(convertToYPixel(vList[0].y), convertToYPixel(vList[2].y)):
                        leftX = float(leftX) + leftSlope
                        rightX = float(rightX) + rightSlope

                        for x in range(int(leftX), int(rightX)):
                            # Interpolate z throughout triangle
                            abpArea = math.fabs(float(ax*(by-y) + bx*(y-ay) + x*(ay-by))/2.)
                            apcArea = math.fabs(float(ax*(y-cy) + x*(cy-ay) + cx*(ay-y))/2.)
                            pbcArea = math.fabs(float(x*(by-cy) + bx*(cy-y) + cx*(y-by))/2.)

                            alpha1 = pbcArea/totalArea # for z1
                            alpha2 = apcArea/totalArea # for z2
                            alpha3 = abpArea/totalArea # for z3

                            z = alpha1*z1 + alpha2*z2 + alpha3*z3

                            if x < 0 or x > WIDTH-1 or y < 0 or y > HEIGHT-1:
                                pass
                            elif z < 0. or z > 1.:
                                pass
                            else:
                                if (z < zbuffer[x][y]):
                                    print str(x)+", "+str(y)+", "+str(z)
                                    image.putpixel((x,y), getCurrentColor())
                                    zbuffer[x][y] = z
                else:
                    print "Arbitrary triangle"
                    if convertToXPixel(vList[1].x) <= convertToXPixel(vList[0].x):
                        leftSlope =  float( convertToXPixel(vList[1].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[1].y) - convertToXPixel(vList[0].y) )
                        rightSlope =  float( convertToXPixel(vList[2].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[0].y) )
                        #print str(slope1)+" "+str(slope2)
                        leftX = convertToXPixel(vList[0].x)
                        rightX = convertToXPixel(vList[0].x)
                        #print str(x1)+" "+str(x2)
                    else:
                        rightSlope =  float( convertToXPixel(vList[1].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[1].y) - convertToXPixel(vList[0].y) )
                        leftSlope =  float( convertToXPixel(vList[2].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[0].y) )
                        #print str(slope1)+" "+str(slope2)
                        leftX = convertToXPixel(vList[0].x)
                        rightX = convertToXPixel(vList[0].x)
                        #print str(x1)+" "+str(x2)


                    # Per-Pixel Clipping of Z:
                    ax = convertToXPixel(vList[0].x)
                    ay = convertToYPixel(vList[0].y)
                    bx = convertToXPixel(vList[1].x)
                    by = convertToYPixel(vList[1].y)
                    cx = convertToXPixel(vList[2].x)
                    cy = convertToYPixel(vList[2].y)
                    totalArea = math.fabs(float(ax*(by-cy) + bx*(cy-ay) + cx*(ay-by))/2.)
                    z1 = vList[0].z
                    z2 = vList[1].z
                    z3 = vList[2].z

                    for y in range(convertToYPixel(vList[0].y), convertToYPixel(vList[1].y)):
                        leftX = float(leftX) + leftSlope
                        rightX = float(rightX) + rightSlope
                        for x in range(int(leftX), int(rightX)):
                            # Interpolate z throughout triangle
                            abpArea = math.fabs(float(ax*(by-y) + bx*(y-ay) + x*(ay-by))/2.)
                            apcArea = math.fabs(float(ax*(y-cy) + x*(cy-ay) + cx*(ay-y))/2.)
                            pbcArea = math.fabs(float(x*(by-cy) + bx*(cy-y) + cx*(y-by))/2.)

                            alpha1 = pbcArea/totalArea # for z1
                            alpha2 = apcArea/totalArea # for z2
                            alpha3 = abpArea/totalArea # for z3

                            z = alpha1*z1 + alpha2*z2 + alpha3*z3

                            if x < 0 or x > WIDTH-1 or y < 0 or y > HEIGHT-1:
                                pass
                            elif z < 0. or z > 1.:
                                pass
                            else:
                                if (z < zbuffer[x][y]):
                                    image.putpixel((x,y), getCurrentColor())
                                    zbuffer[x][y] = z

                    midXPixel = int( convertToXPixel(vList[0].x) + ( ( (float(convertToXPixel(vList[1].y)- convertToXPixel(vList[0].y))) / (float(convertToXPixel(vList[2].y) - convertToXPixel(vList[0].y))) ) * (float(convertToXPixel(vList[2].x) - convertToXPixel(vList[0].x))) ) )

                    if convertToXPixel(vList[1].x) <= convertToXPixel(vList[0].x):
                        leftSlope =  float( convertToXPixel(vList[2].x) - convertToXPixel(vList[1].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[1].y) )
                        leftX = convertToXPixel(vList[1].x)
                        rightX = midXPixel
                    else:
                        rightSlope = float( convertToXPixel(vList[2].x) - convertToXPixel(vList[1].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[1].y) )
                        rightX = convertToXPixel(vList[1].x)
                        leftX = midXPixel

                    for y in range(convertToYPixel(vList[1].y), convertToYPixel(vList[2].y)):
                        leftX = float(leftX) + leftSlope
                        rightX = float(rightX) + rightSlope

                        for x in range(int(leftX), int(rightX)):
                            # Interpolate z throughout triangle
                            abpArea = math.fabs(float(ax*(by-y) + bx*(y-ay) + x*(ay-by))/2.)
                            apcArea = math.fabs(float(ax*(y-cy) + x*(cy-ay) + cx*(ay-y))/2.)
                            pbcArea = math.fabs(float(x*(by-cy) + bx*(cy-y) + cx*(y-by))/2.)

                            alpha1 = pbcArea/totalArea # for z1
                            alpha2 = apcArea/totalArea # for z2
                            alpha3 = abpArea/totalArea # for z3

                            z = alpha1*z1 + alpha2*z2 + alpha3*z3

                            if x < 0 or x > WIDTH-1 or y < 0 or y > HEIGHT-1:
                                pass
                            elif z < 0. or z > 1.:
                                pass
                            else:
                                if (z < zbuffer[x][y]):
                                    image.putpixel((x,y), getCurrentColor())
                                    zbuffer[x][y] = z
            else :
                #print "Triangle has no height. Not drawing it."
                pass
        else:
            pass
    else:
        # Divide by x,y,z by w
        if vList[0].y - vList[2].y != 0:
            print "Draw the triangle"

            if vList[1].y - vList[2].y == 0:
                print "Triangle has flat bottom"
                slope1 =  float( convertToXPixel(vList[1].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[1].y) - convertToXPixel(vList[0].y) )
                slope2 =  float( convertToXPixel(vList[2].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[0].y) )
                #print str(slope1)+" "+str(slope2)

                x1 = convertToXPixel(vList[0].x)
                x2 = convertToXPixel(vList[0].x)
                #print str(x1)+" "+str(x2)


                # Per-Pixel Clipping of Z:
                ax = convertToXPixel(vList[0].x)
                ay = convertToYPixel(vList[0].y)
                bx = convertToXPixel(vList[1].x)
                by = convertToYPixel(vList[1].y)
                cx = convertToXPixel(vList[2].x)
                cy = convertToYPixel(vList[2].y)
                totalArea = math.fabs(float(ax*(by-cy) + bx*(cy-ay) + cx*(ay-by))/2.)
                z1 = vList[0].z
                z2 = vList[1].z
                z3 = vList[2].z

                w1 = vList[0].w
                w2 = vList[1].w
                w3 = vList[2].w

                for y in range(convertToYPixel(vList[0].y), convertToYPixel(vList[1].y)):
                    x1 = float(x1) + slope1
                    x2 = float(x2) + slope2
                    #print str(int(x1))+" "+str(int(x2))
                    for x in range(int(x1), int(x2)):
                        # Interpolate z throughout triangle
                        abpArea = math.fabs(float(ax*(by-y) + bx*(y-ay) + x*(ay-by))/2.)
                        apcArea = math.fabs(float(ax*(y-cy) + x*(cy-ay) + cx*(ay-y))/2.)
                        pbcArea = math.fabs(float(x*(by-cy) + bx*(cy-y) + cx*(y-by))/2.)

                        alpha1 = pbcArea/totalArea # for z1
                        alpha2 = apcArea/totalArea # for z2
                        alpha3 = abpArea/totalArea # for z3

                        z = alpha1*z1 + alpha2*z2 + alpha3*z3
                        w = alpha1*w1 + alpha2*w2 + alpha3*w3

                        #print "@("+str(x)+", "+str(y)+")\tZ: "+str(z)+"\tT: "+str(t)
                        if x < 0 or x > WIDTH-1 or y < 0 or y > HEIGHT-1:
                            pass
                        elif z < 0. or z > 1.:
                            pass
                        else:
                            #if clipplaneBool and dot(plane, array([x, y, z, w])) >= 0:
                            #    if (z < zbuffer[x][y]):
                            #        image.putpixel((x,y), getCurrentColor())
                            #        zbuffer[x][y] = z
                            #else:
                            if (z < zbuffer[x][y]):
                                image.putpixel((x,y), getCurrentColor())
                                zbuffer[x][y] = z


            elif vList[0].y - vList[1].y == 0:
                print "Triangle has flat top"
                #slope1 =  float( convertToXPixel(vList[2].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[0].y) )
                #slope2 =  float( convertToXPixel(vList[2].x) - convertToXPixel(vList[1].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[1].y) )
                #print str(slope1)+" "+str(slope2)

                if convertToXPixel(vList[0].x) < convertToXPixel(vList[1].x):
                    leftSlope =  float( convertToXPixel(vList[2].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[0].y) )
                    rightSlope =  float( convertToXPixel(vList[2].x) - convertToXPixel(vList[1].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[1].y) )
                    #print str(slope1)+" "+str(slope2)
                    leftX = convertToXPixel(vList[0].x)
                    rightX = convertToXPixel(vList[1].x)

                else:
                    leftSlope =  float( convertToXPixel(vList[2].x) - convertToXPixel(vList[1].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[1].y) )
                    rightSlope =  float( convertToXPixel(vList[2].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[0].y) )
                    #print str(slope1)+" "+str(slope2)
                    leftX = convertToXPixel(vList[1].x)
                    rightX = convertToXPixel(vList[0].x)


                #leftX = convertToXPixel(vList[0].x)
                #rightX = convertToXPixel(vList[1].x)
                #print str(x1)+" "+str(x2)

                # Per-Pixel Clipping of Z:
                #
                # Barycentric Interpolation
                # z = (%z1)z1 + (%z2)z2 + (%z3)z3
                # %z1 = Area of triangle (p, z2, z3) / total area
                # Area of triangle = (.5)|cross(p->z2, p->z3); where p->z2 means vector from p to z2
                ax = convertToXPixel(vList[0].x)
                ay = convertToYPixel(vList[0].y)
                bx = convertToXPixel(vList[1].x)
                by = convertToYPixel(vList[1].y)
                cx = convertToXPixel(vList[2].x)
                cy = convertToYPixel(vList[2].y)
                totalArea = math.fabs(float(ax*(by-cy) + bx*(cy-ay) + cx*(ay-by))/2.)
                z1 = vList[0].z
                z2 = vList[1].z
                z3 = vList[2].z

                w1 = vList[0].w
                w2 = vList[1].w
                w3 = vList[2].w

                for y in range(convertToYPixel(vList[0].y), convertToYPixel(vList[2].y)):
                    leftX = float(leftX) + leftSlope
                    rightX = float(rightX) + rightSlope
                    #print str(int(x1))+" "+str(int(x2))

                    for x in range(int(leftX), int(rightX)):
                        # Interpolate z throughout triangle
                        abpArea = math.fabs(float(ax*(by-y) + bx*(y-ay) + x*(ay-by))/2.)
                        apcArea = math.fabs(float(ax*(y-cy) + x*(cy-ay) + cx*(ay-y))/2.)
                        pbcArea = math.fabs(float(x*(by-cy) + bx*(cy-y) + cx*(y-by))/2.)

                        alpha1 = pbcArea/totalArea # for z1
                        alpha2 = apcArea/totalArea # for z2
                        alpha3 = abpArea/totalArea # for z3

                        z = alpha1*z1 + alpha2*z2 + alpha3*z3
                        w = alpha1*w1 + alpha2*w2 + alpha3*w3

                        #print "@("+str(x)+", "+str(y)+")\tZ: "+str(z)+"\tT: "+str(t)
                        if x < 0 or x > WIDTH-1 or y < 0 or y > HEIGHT-1:
                            pass
                        elif z < 0. or z > 1.:
                            pass
                        else:
                            #print dot(plane, array([x, y, z, w]))
                            #if clipplaneBool and dot(plane, array([x, y, z, w])) >= 0:
                            #    if (z < zbuffer[x][y]):
                            #        image.putpixel((x,y), getCurrentColor())
                            #        zbuffer[x][y] = z
                            #else:
                            if (z < zbuffer[x][y]):
                                image.putpixel((x,y), getCurrentColor())
                                zbuffer[x][y] = z

            else:
                print "Arbitrary triangle"
                if convertToXPixel(vList[1].x) <= convertToXPixel(vList[0].x):
                    leftSlope =  float( convertToXPixel(vList[1].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[1].y) - convertToXPixel(vList[0].y) )
                    rightSlope =  float( convertToXPixel(vList[2].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[0].y) )
                    #print str(slope1)+" "+str(slope2)
                    leftX = convertToXPixel(vList[0].x)
                    rightX = convertToXPixel(vList[0].x)
                    #print str(x1)+" "+str(x2)
                else:
                    rightSlope =  float( convertToXPixel(vList[1].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[1].y) - convertToXPixel(vList[0].y) )
                    leftSlope =  float( convertToXPixel(vList[2].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[0].y) )
                    #print str(slope1)+" "+str(slope2)
                    leftX = convertToXPixel(vList[0].x)
                    rightX = convertToXPixel(vList[0].x)
                    #print str(x1)+" "+str(x2)


                # Per-Pixel Clipping of Z:
                ax = convertToXPixel(vList[0].x)
                ay = convertToYPixel(vList[0].y)
                bx = convertToXPixel(vList[1].x)
                by = convertToYPixel(vList[1].y)
                cx = convertToXPixel(vList[2].x)
                cy = convertToYPixel(vList[2].y)
                totalArea = math.fabs(float(ax*(by-cy) + bx*(cy-ay) + cx*(ay-by))/2.)
                z1 = vList[0].z
                z2 = vList[1].z
                z3 = vList[2].z

                for y in range(convertToYPixel(vList[0].y), convertToYPixel(vList[1].y)):
                    leftX = float(leftX) + leftSlope
                    rightX = float(rightX) + rightSlope
                    #print str(int(x1))+" "+str(int(x2))
                    for x in range(int(leftX), int(rightX)):
                        # Interpolate z throughout triangle
                        abpArea = math.fabs(float(ax*(by-y) + bx*(y-ay) + x*(ay-by))/2.)
                        apcArea = math.fabs(float(ax*(y-cy) + x*(cy-ay) + cx*(ay-y))/2.)
                        pbcArea = math.fabs(float(x*(by-cy) + bx*(cy-y) + cx*(y-by))/2.)

                        alpha1 = pbcArea/totalArea # for z1
                        alpha2 = apcArea/totalArea # for z2
                        alpha3 = abpArea/totalArea # for z3

                        z = alpha1*z1 + alpha2*z2 + alpha3*z3

                        #print "@("+str(x)+", "+str(y)+")\tZ: "+str(z)+"\tT: "+str(t)
                        if x < 0 or x > WIDTH-1 or y < 0 or y > HEIGHT-1:
                            pass
                        elif z < 0. or z > 1.:
                            pass
                        else:
                            if (z < zbuffer[x][y]):
                                image.putpixel((x,y), getCurrentColor())
                                zbuffer[x][y] = z

                #print "Numerator: "+str((float(convertToXPixel(vList[1].y)- convertToXPixel(vList[0].y))))
                #print "Denominator: "+str((float(convertToXPixel(vList[2].y) - convertToXPixel(vList[0].y))))
                #print "Dividend: "+str((float(convertToXPixel(vList[1].y)- convertToXPixel(vList[0].y)))/(float(convertToXPixel(vList[2].y) - convertToXPixel(vList[0].y))))
                #print "Difference: "+str(float(convertToXPixel(vList[2].x) - convertToXPixel(vList[0].x)))
                #print "Product: "+str((float(convertToXPixel(vList[1].y)- convertToXPixel(vList[0].y)))/(float(convertToXPixel(vList[2].y) - convertToXPixel(vList[0].y))) * math.fabs(float(convertToXPixel(vList[2].x) - convertToXPixel(vList[0].x))))
                #print "Final: "+str( convertToXPixel(vList[0].x) + ((float(convertToXPixel(vList[1].y)- convertToXPixel(vList[0].y)))/(float(convertToXPixel(vList[2].y) - convertToXPixel(vList[0].y))) * math.fabs(float(convertToXPixel(vList[2].x) - convertToXPixel(vList[0].x)))))

                midXPixel = int( convertToXPixel(vList[0].x) + ( ( (float(convertToXPixel(vList[1].y)- convertToXPixel(vList[0].y))) / (float(convertToXPixel(vList[2].y) - convertToXPixel(vList[0].y))) ) * (float(convertToXPixel(vList[2].x) - convertToXPixel(vList[0].x))) ) )
                #print midXPixel

                if convertToXPixel(vList[1].x) <= convertToXPixel(vList[0].x):
                    #slope1 =  float( convertToXPixel(vList[2].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[0].y) )
                    leftSlope =  float( convertToXPixel(vList[2].x) - convertToXPixel(vList[1].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[1].y) )
                    #print str(slope1)+" "+str(slope2)
                    leftX = convertToXPixel(vList[1].x)
                    rightX = midXPixel
                else:
                    rightSlope = float( convertToXPixel(vList[2].x) - convertToXPixel(vList[1].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[1].y) )
                    rightX = convertToXPixel(vList[1].x)
                    leftX = midXPixel
                #x1 = convertToXPixel(vList[0].x)
                #x2 = convertToXPixel(vList[1].x)
                #print str(x1)+" "+str(x2)


                for y in range(convertToYPixel(vList[1].y), convertToYPixel(vList[2].y)):
                    leftX = float(leftX) + leftSlope
                    rightX = float(rightX) + rightSlope
                    #print str(int(x1))+" "+str(int(x2))
                    for x in range(int(leftX), int(rightX)):
                        # Interpolate z throughout triangle
                        abpArea = math.fabs(float(ax*(by-y) + bx*(y-ay) + x*(ay-by))/2.)
                        apcArea = math.fabs(float(ax*(y-cy) + x*(cy-ay) + cx*(ay-y))/2.)
                        pbcArea = math.fabs(float(x*(by-cy) + bx*(cy-y) + cx*(y-by))/2.)

                        alpha1 = pbcArea/totalArea # for z1
                        alpha2 = apcArea/totalArea # for z2
                        alpha3 = abpArea/totalArea # for z3

                        z = alpha1*z1 + alpha2*z2 + alpha3*z3

                        #print "@("+str(x)+", "+str(y)+")\tZ: "+str(z)+"\tT: "+str(t)
                        if x < 0 or x > WIDTH-1 or y < 0 or y > HEIGHT-1:
                            pass
                        elif z < 0. or z > 1.:
                            pass
                        else:
                            if (z < zbuffer[x][y]):
                                image.putpixel((x,y), getCurrentColor())
                                zbuffer[x][y] = z


        else :
            #print "Triangle has no height. Not drawing it."
            pass

# Viewport Transformation
def convertToXPixel(relativeX):
    x = relativeX + 1.
    x *= WIDTH/2
    return int(x)
# Viewport Transformation
def convertToYPixel(relativeY):
    y = relativeY +1
    y *= HEIGHT/2
    return int(y)

# Change to Zero Index for Vertex List
def getListIndex(oneIndex):
    if oneIndex < 0 :
        return oneIndex
    else :
        return oneIndex - 1

def getCurrentColor():
    r = int(currentColor[0]*255)
    g = int(currentColor[1]*255)
    b = int(currentColor[2]*255)
    return (r,g,b)

def normalize(vector):
    magnitude = math.sqrt((vector[0].item() * vector[0].item()) + (vector[1].item() * vector[1].item()) + (vector[2].item() * vector[2].item()))
    return array([vector[0].item()/magnitude, vector[1].item()/magnitude, vector[2].item()/magnitude])

def trig(i1, i2, i3, color1, color2, color3):
    vList = [i1, i2, i3]

    vList[0].r = color1[0]
    vList[0].g = color1[1]
    vList[0].b = color1[2]

    vList[1].r = color2[0]
    vList[1].g = color2[1]
    vList[1].b = color2[2]

    vList[2].r = color3[0]
    vList[2].g = color3[1]
    vList[2].b = color3[2]

    vList.sort(key=lambda v: v.y)   # vList[0] is highest screen; vList[2] is lowest on screen


    if vList[0].y - vList[2].y != 0:
        print "Draw the triangle"

        if vList[1].y - vList[2].y == 0:
            print "Triangle has flat bottom"
            slope1 =  float( convertToXPixel(vList[1].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[1].y) - convertToXPixel(vList[0].y) )
            slope2 =  float( convertToXPixel(vList[2].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[0].y) )
            #print str(slope1)+" "+str(slope2)

            x1 = convertToXPixel(vList[0].x)
            x2 = convertToXPixel(vList[0].x)
            #print str(x1)+" "+str(x2)


            # Per-Pixel Clipping of Z:
            ax = convertToXPixel(vList[0].x)
            ay = convertToYPixel(vList[0].y)
            bx = convertToXPixel(vList[1].x)
            by = convertToYPixel(vList[1].y)
            cx = convertToXPixel(vList[2].x)
            cy = convertToYPixel(vList[2].y)
            totalArea = math.fabs(float(ax*(by-cy) + bx*(cy-ay) + cx*(ay-by))/2.)
            z1 = vList[0].z
            z2 = vList[1].z
            z3 = vList[2].z

            r1 = vList[0].r
            r2 = vList[1].r
            r3 = vList[2].r

            g1 = vList[0].g
            g2 = vList[1].g
            g3 = vList[2].g

            b1 = vList[0].b
            b2 = vList[1].b
            b3 = vList[2].b


            for y in range(convertToYPixel(vList[0].y), convertToYPixel(vList[1].y)):
                x1 = float(x1) + slope1
                x2 = float(x2) + slope2
                #print str(int(x1))+" "+str(int(x2))
                for x in range(int(x1), int(x2)):
                    # Interpolate z throughout triangle
                    abpArea = math.fabs(float(ax*(by-y) + bx*(y-ay) + x*(ay-by))/2.)
                    apcArea = math.fabs(float(ax*(y-cy) + x*(cy-ay) + cx*(ay-y))/2.)
                    pbcArea = math.fabs(float(x*(by-cy) + bx*(cy-y) + cx*(y-by))/2.)

                    alpha1 = pbcArea/totalArea # for z1
                    alpha2 = apcArea/totalArea # for z2
                    alpha3 = abpArea/totalArea # for z3

                    z = alpha1*z1 + alpha2*z2 + alpha3*z3
                    r = alpha1*r1 + alpha2*r2 + alpha3*r3
                    g = alpha1*g1 + alpha2*g2 + alpha3*g3
                    b = alpha1*b1 + alpha2*b2 + alpha3*b3




                    #print "@("+str(x)+", "+str(y)+")\tZ: "+str(z)+"\tT: "+str(t)
                    if x < 0 or x > WIDTH-1 or y < 0 or y > HEIGHT-1:
                        pass
                    elif z < 0. or z > 1.:
                        pass
                    else:
                        if (z < zbuffer[x][y]):
                            image.putpixel((x,y), (int(r),int(g),int(b)))
                            zbuffer[x][y] = z

        elif vList[0].y - vList[1].y == 0:
            print "Triangle has flat top"
            slope1 =  float( convertToXPixel(vList[2].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[0].y) )
            slope2 =  float( convertToXPixel(vList[2].x) - convertToXPixel(vList[1].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[1].y) )
            #print str(slope1)+" "+str(slope2)

            x1 = convertToXPixel(vList[0].x)
            x2 = convertToXPixel(vList[1].x)
            #print str(x1)+" "+str(x2)

            # Per-Pixel Clipping of Z:
            #
            # Barycentric Interpolation
            # z = (%z1)z1 + (%z2)z2 + (%z3)z3
            # %z1 = Area of triangle (p, z2, z3) / total area
            # Area of triangle = (.5)|cross(p->z2, p->z3); where p->z2 means vector from p to z2
            ax = convertToXPixel(vList[0].x)
            ay = convertToYPixel(vList[0].y)
            bx = convertToXPixel(vList[1].x)
            by = convertToYPixel(vList[1].y)
            cx = convertToXPixel(vList[2].x)
            cy = convertToYPixel(vList[2].y)
            totalArea = math.fabs(float(ax*(by-cy) + bx*(cy-ay) + cx*(ay-by))/2.)
            z1 = vList[0].z
            z2 = vList[1].z
            z3 = vList[2].z

            r1 = vList[0].r
            r2 = vList[1].r
            r3 = vList[2].r

            g1 = vList[0].g
            g2 = vList[1].g
            g3 = vList[2].g

            b1 = vList[0].b
            b2 = vList[1].b
            b3 = vList[2].b

            for y in range(convertToYPixel(vList[0].y), convertToYPixel(vList[2].y)):
                x1 = float(x1) + slope1
                x2 = float(x2) + slope2
                #print str(int(x1))+" "+str(int(x2))

                for x in range(int(x1), int(x2)):
                    # Interpolate z throughout triangle
                    abpArea = math.fabs(float(ax*(by-y) + bx*(y-ay) + x*(ay-by))/2.)
                    apcArea = math.fabs(float(ax*(y-cy) + x*(cy-ay) + cx*(ay-y))/2.)
                    pbcArea = math.fabs(float(x*(by-cy) + bx*(cy-y) + cx*(y-by))/2.)

                    alpha1 = pbcArea/totalArea # for z1
                    alpha2 = apcArea/totalArea # for z2
                    alpha3 = abpArea/totalArea # for z3

                    z = alpha1*z1 + alpha2*z2 + alpha3*z3
                    r = alpha1*r1 + alpha2*r2 + alpha3*r3
                    g = alpha1*g1 + alpha2*g2 + alpha3*g3
                    b = alpha1*b1 + alpha2*b2 + alpha3*b3

                    #print "@("+str(x)+", "+str(y)+")\tZ: "+str(z)+"\tT: "+str(t)
                    if x < 0 or x > WIDTH-1 or y < 0 or y > HEIGHT-1:
                        pass
                    elif z < 0. or z > 1.:
                        pass
                    else:
                        if (z < zbuffer[x][y]):
                            image.putpixel((x,y), (int(r),int(g),int(b)))
                            zbuffer[x][y] = z
        else:
            print "Arbitrary triangle"
            if convertToXPixel(vList[1].x) <= convertToXPixel(vList[0].x):
                leftSlope =  float( convertToXPixel(vList[1].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[1].y) - convertToXPixel(vList[0].y) )
                rightSlope =  float( convertToXPixel(vList[2].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[0].y) )

                leftX = convertToXPixel(vList[0].x)
                rightX = convertToXPixel(vList[0].x)
            else:
                rightSlope =  float( convertToXPixel(vList[1].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[1].y) - convertToXPixel(vList[0].y) )
                leftSlope =  float( convertToXPixel(vList[2].x) - convertToXPixel(vList[0].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[0].y) )

                leftX = convertToXPixel(vList[0].x)
                rightX = convertToXPixel(vList[0].x)


            # Per-Pixel Clipping of Z:
            ax = convertToXPixel(vList[0].x)
            ay = convertToYPixel(vList[0].y)
            bx = convertToXPixel(vList[1].x)
            by = convertToYPixel(vList[1].y)
            cx = convertToXPixel(vList[2].x)
            cy = convertToYPixel(vList[2].y)
            totalArea = math.fabs(float(ax*(by-cy) + bx*(cy-ay) + cx*(ay-by))/2.)
            z1 = vList[0].z
            z2 = vList[1].z
            z3 = vList[2].z

            r1 = vList[0].r
            r2 = vList[1].r
            r3 = vList[2].r

            g1 = vList[0].g
            g2 = vList[1].g
            g3 = vList[2].g

            b1 = vList[0].b
            b2 = vList[1].b
            b3 = vList[2].b

            for y in range(convertToYPixel(vList[0].y), convertToYPixel(vList[1].y)):
                leftX = float(leftX) + leftSlope
                rightX = float(rightX) + rightSlope
                #print str(int(x1))+" "+str(int(x2))
                for x in range(int(leftX), int(rightX)):
                    # Interpolate z throughout triangle
                    abpArea = math.fabs(float(ax*(by-y) + bx*(y-ay) + x*(ay-by))/2.)
                    apcArea = math.fabs(float(ax*(y-cy) + x*(cy-ay) + cx*(ay-y))/2.)
                    pbcArea = math.fabs(float(x*(by-cy) + bx*(cy-y) + cx*(y-by))/2.)

                    alpha1 = pbcArea/totalArea # for z1
                    alpha2 = apcArea/totalArea # for z2
                    alpha3 = abpArea/totalArea # for z3

                    z = alpha1*z1 + alpha2*z2 + alpha3*z3

                    r = 255.*(alpha1*r1 + alpha2*r2 + alpha3*r3)
                    g = 255.*(alpha1*g1 + alpha2*g2 + alpha3*g3)
                    b = 255.*(alpha1*b1 + alpha2*b2 + alpha3*b3)

                    #print z1
                    #print z2
                    #print z3
                    #print "Final Z: "+str(z)
                    #print b1
                    #print b2
                    #print b3
                    #print "Final b: "+str(b)

                    #print "@("+str(x)+", "+str(y)+")\tZ: "+str(z)+"\tT: "+str(t)
                    if x < 0 or x > WIDTH-1 or y < 0 or y > HEIGHT-1:
                        pass
                    elif z < 0. or z > 1.:
                        pass
                    else:
                        if (z < zbuffer[x][y]):
                            if r < 0.:
                                r = 0.
                            if r > 255.:
                                r = 255.
                            if g < 0.:
                                g = 0.
                            if g > 255.:
                                g = 255.
                            if b < 0.:
                                b = 0.
                            if b > 255.:
                                b = 255.
                            image.putpixel((x,y), (int(r),int(g),int(b)))
                            zbuffer[x][y] = z

            midXPixel = int( convertToXPixel(vList[0].x) + ( ( (float(convertToXPixel(vList[1].y)- convertToXPixel(vList[0].y))) / (float(convertToXPixel(vList[2].y) - convertToXPixel(vList[0].y))) ) * (float(convertToXPixel(vList[2].x) - convertToXPixel(vList[0].x))) ) )

            if convertToXPixel(vList[1].x) <= convertToXPixel(vList[0].x):
                leftSlope =  float( convertToXPixel(vList[2].x) - convertToXPixel(vList[1].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[1].y) )
                leftX = convertToXPixel(vList[1].x)
                rightX = midXPixel
            else:
                rightSlope = float( convertToXPixel(vList[2].x) - convertToXPixel(vList[1].x) ) / float( convertToXPixel(vList[2].y) - convertToXPixel(vList[1].y) )
                rightX = convertToXPixel(vList[1].x)
                leftX = midXPixel

            for y in range(convertToYPixel(vList[1].y), convertToYPixel(vList[2].y)):
                leftX = float(leftX) + leftSlope
                rightX = float(rightX) + rightSlope
                for x in range(int(leftX), int(rightX)):
                    # Interpolate z throughout triangle
                    abpArea = math.fabs(float(ax*(by-y) + bx*(y-ay) + x*(ay-by))/2.)
                    apcArea = math.fabs(float(ax*(y-cy) + x*(cy-ay) + cx*(ay-y))/2.)
                    pbcArea = math.fabs(float(x*(by-cy) + bx*(cy-y) + cx*(y-by))/2.)

                    alpha1 = pbcArea/totalArea # for z1
                    alpha2 = apcArea/totalArea # for z2
                    alpha3 = abpArea/totalArea # for z3

                    z = alpha1*z1 + alpha2*z2 + alpha3*z3

                    r = alpha1*r1*255. + alpha2*r2*255. + alpha3*r3*255.
                    g = alpha1*g1*255. + alpha2*g2*255. + alpha3*g3*255.
                    b = alpha1*b1*255. + alpha2*b2*255. + alpha3*b3*255.

                    if x < 0 or x > WIDTH-1 or y < 0 or y > HEIGHT-1:
                        pass
                    elif z < 0. or z > 1.:
                        pass
                    else:
                        if (z < zbuffer[x][y]):
                            if r < 0.:
                                r = 0.
                            if r > 255.:
                                r = 255.
                            if g < 0.:
                                g = 0.
                            if g > 255.:
                                g = 255.
                            if b < 0.:
                                b = 0.
                            if b > 255.:
                                b = 255.
                            image.putpixel((x,y), (int(r),int(g),int(b)))
                            zbuffer[x][y] = z


    else :
        #print "Triangle has no height. Not drawing it."
        pass

def main():
    global TEXTFILE
    global FILENAME
    global WIDTH
    global HEIGHT
    global IDENTITY
    global image
    global vertex_list
    global vertex_colors
    global currentColor
    global zbuffer
    global transformBuffer
    global projectionBuffer
    global cull
    global clipplaneBool
    global plane


    if (sys.argv.__len__() < 2):
        print "Kinda need a textfile argument to write anything"
    else :
        TEXTFILE = sys.argv[1]
        if (TEXTFILE.isspace() or not TEXTFILE):
            print "How about you give me a textfile to read"
        else:
            vertex_list = []
            vertex_colors = []
            with open(TEXTFILE, 'r') as input:
                for line in input:
                    args = line.split()
                    if args[0].__eq__("png"):
                        WIDTH = int(args[1])
                        HEIGHT = int(args[2])
                        FILENAME = args[3]
                        IDENTITY = array([[ 1., 0., 0., 0.], [ 0., 1., 0., 0.], [ 0., 0., 1., 0.], [ 0., 0., 0., 1.]])
                        currentColor = [float(1.0), float(1.0), float(1.0)]

                        image = Image.new("RGBA", (WIDTH, HEIGHT))
                        zbuffer = ones((WIDTH, HEIGHT))
                        transformBuffer = IDENTITY.copy()
                        projectionBuffer = IDENTITY.copy()
                        cull = None
                        clipplaneBool = None
                        plane = array([0., 0., 0., 0.])

                    elif args[0].__eq__("xyz"):
                        x = float(args[1])
                        y = float(args[2])
                        z = float(args[3])

                        v = Vertex(x, y, z)
                        vertex_list.append(v)

                    elif args[0].__eq__("trif"):
                        # Apply and clear transformBuffer to all given vertices
                        # ******************** Works for translate **********************
                        #while len(transformBuffer) > 0:
                        #    matrix = transformBuffer.pop()
                        #    #print matrix
                        #    for v in vertex_list:
                        #        result = dot(matrix,array([v.x, v.y, v.z, v.w]).reshape(4,1))
                        #        #print "["+str(result[0].item())+", "+str(result[1].item())+", "+str(result[2].item())+", "+str(result[3].item())+"]"
                        #        v.setX(result[0].item())
                        #        v.setY(result[1].item())
                        #        v.setZ(result[2].item())
                        #        v.setW(result[3].item())

                        # Retrieve vertices used for drawing triangle
                        index1 = getListIndex(int(args[1]))
                        index2 = getListIndex(int(args[2]))
                        index3 = getListIndex(int(args[3]))

                        v1 = vertex_list[index1]
                        v2 = vertex_list[index2]
                        v3 = vertex_list[index3]

                        vList = [v1, v2, v3]
                        for v in vList:
                            matrix = transformBuffer
                            result = dot(matrix,array([v.x, v.y, v.z, v.w]).reshape(4,1))
                            #print "["+str(result[0].item())+", "+str(result[1].item())+", "+str(result[2].item())+", "+str(result[3].item())+"]"
                            v.setX(result[0].item())
                            v.setY(result[1].item())
                            v.setZ(result[2].item())
                            v.setW(result[3].item())

                        # Applies to all vertices (Last working approach)
                        #for v in vertex_list:
                        #    matrix = transformBuffer
                        #    result = dot(matrix,array([v.x, v.y, v.z, v.w]).reshape(4,1))
                        #    #print "["+str(result[0].item())+", "+str(result[1].item())+", "+str(result[2].item())+", "+str(result[3].item())+"]"
                        #    v.setX(result[0].item())
                        #    v.setY(result[1].item())
                        #    v.setZ(result[2].item())
                        #    v.setW(result[3].item())


                        #for v in vList:
                        #    vector = v.vector3()
                        #    normalized = normalize(vector)
                        #    v.setX(normalized[0].item())
                        #    v.setY(normalized[1].item())
                        #    v.setZ(normalized[2].item())

                        trif(vList[0], vList[1], vList[2])

                    elif args[0].__eq__("color"):       # doesn't clamp color range
                        currentColor[0] = float(args[1])
                        currentColor[1] = float(args[2])
                        currentColor[2] = float(args[3])
                        #print str(getCurrentColor())
                        #currentColor = setCurrentColor(r,g,b)
                        vertex_colors.append(currentColor[:])
                        #print vertex_colors

                    elif args[0].__eq__("translate"):
                        #apply translation to all vertices in buffer (don't reverse)
                        dx = float(args[1])
                        dy = float(args[2])
                        dz = float(args[3])

                        matrix = IDENTITY.copy()
                        matrix[0][3] = dx
                        matrix[1][3] = dy
                        matrix[2][3] = dz
                        #print matrix

                        transformBuffer = matrix
                        #print transformBuffer

                        #transformBuffer.append(matrix[:].copy())
                        #print transformBuffer

                    elif args[0].__eq__("lookat"):
                        eyeIndex = getListIndex(int(args[1]))
                        centerIndex = getListIndex(int(args[2]))

                        eye = vertex_list[eyeIndex]
                        center = vertex_list[centerIndex]
                        upx = float(args[3])
                        upy = float(args[4])
                        upz = float(args[5])

                        # Create F and UP
                        bigF = array([center.x - eye.x, center.y - eye.y, center.z - eye.z])
                        bigUp = array([upx, upy, upz])

                        # Normalize F and UP
                        f = normalize(bigF)
                        up = normalize(bigUp)
                        #print "LookAt"

                        # Find s and u
                        s = cross(f, up)
                        #print s
                        sNorm = normalize(s)
                        #print sNorm
                        u = cross(sNorm, f) # already normalized

                        # Construct M matrix
                        matrix = IDENTITY.copy()
                        matrix[0][0] = sNorm[0].item()
                        matrix[0][1] = sNorm[1].item()
                        matrix[0][2] = sNorm[2].item()
                        matrix[1][0] = u[0].item()
                        matrix[1][1] = u[1].item()
                        matrix[1][2] = u[2].item()
                        matrix[2][0] = -(f[0].item())
                        matrix[2][1] = -(f[1].item())
                        matrix[2][2] = -(f[2].item())

                        eyeTranslation = IDENTITY.copy()
                        eyeTranslation[0][3] = -1. * eye.x
                        eyeTranslation[1][3] = -1. * eye.y
                        eyeTranslation[2][3] = -1. * eye.z

                        final = dot(matrix, eyeTranslation)

                        transformBuffer = dot(final, transformBuffer)
                        print transformBuffer

                        #print matrix
                        #transformBuffer.append(matrix[:].copy())
                        #transformBuffer.append(eyeTranslation[:].copy())

                    elif args[0].__eq__("ortho"):
                        left = float(args[1])
                        right = float(args[2])
                        bottom = float(args[3])
                        top = float(args[4])
                        n = float(args[5])
                        farVal = float(args[6])
                        nearVal = 2.*n - farVal

                        tx = -1. * ((right+left)/(right-left))
                        ty = -1. * ((top+bottom)/(top-bottom))
                        tz = -1. * ((farVal+nearVal)/(farVal-nearVal))

                        matrix = IDENTITY.copy()
                        matrix[0][0] = 2./(right-left)
                        matrix[1][1] = 2./(top-bottom)
                        matrix[2][2] = 2./(farVal-nearVal)
                        matrix[0][3] = tx
                        matrix[1][3] = ty
                        matrix[2][3] = tz

                        transformBuffer = matrix
                        print transformBuffer

                        #transformBuffer.append(matrix[:].copy())

                    elif args[0].__eq__("frustum"):
                        left = float(args[1])
                        right = float(args[2])
                        bottom = float(args[3])
                        top = float(args[4])
                        nearVal = float(args[5])
                        farVal = float(args[6])

                        a = (right+left)/(right-left)
                        b = (top+bottom)/(top-bottom)
                        c = -1.*((farVal+nearVal)/(farVal-nearVal))
                        d = -1.*((2.*farVal*nearVal)/(farVal-nearVal))

                        matrix = array([[((2.*nearVal)/(right-left)), 0., a, 0.],[0., ((2.*nearVal)/(top-bottom)), b, 0.],[0., 0., c, d],[0., 0., -1., 0.]])

                        transformBuffer = matrix
                        print transformBuffer

                        #transformBuffer.append(matrix[:].copy())

                    elif args[0].__eq__("rotatex"):
                        #apply translation to all vertices in buffer (don't reverse)
                        degrees = float(args[1])
                        radians = degrees * (math.pi/180.)

                        matrix = IDENTITY.copy()
                        matrix[1][1] = math.cos(radians)
                        matrix[1][2] = -1. * math.sin(radians)
                        matrix[2][1] = math.sin(radians)
                        matrix[2][2] = math.cos(radians)
                        #print "Degrees: "+str(degrees)
                        #print "Radians: "+str(radians)
                        #print matrix

                        transformBuffer = dot(matrix, transformBuffer)
                        #print transformBuffer

                        #transformBuffer.append(matrix[:].copy())
                        #print transformBuffer

                    elif args[0].__eq__("rotatey"):
                        #apply translation to all vertices in buffer (don't reverse)
                        degrees = float(args[1])
                        radians = degrees * (math.pi/180.)

                        matrix = IDENTITY.copy()
                        matrix[0][0] = math.cos(radians)
                        matrix[0][2] = math.sin(radians)
                        matrix[2][0] = -1. * math.sin(radians)
                        matrix[2][2] = math.cos(radians)
                        #print matrix

                        transformBuffer = dot(matrix, transformBuffer)
                        #print transformBuffer

                        #transformBuffer.append(matrix[:].copy())
                        #print transformBuffer

                    elif args[0].__eq__("rotatez"):
                        #apply translation to all vertices in buffer (don't reverse)
                        degrees = float(args[1])
                        radians = degrees * (math.pi/180.)

                        matrix = IDENTITY.copy()
                        matrix[0][0] = math.cos(radians)
                        matrix[0][1] = -1. * math.sin(radians)
                        matrix[1][0] = math.sin(radians)
                        matrix[1][1] = math.cos(radians)
                        #print matrix

                        transformBuffer = dot(matrix, transformBuffer)
                        #print transformBuffer

                        #transformBuffer.append(matrix[:].copy())
                        #print transformBuffer

                    elif args[0].__eq__("rotate"):
                        #apply translation to all vertices in buffer (don't reverse)
                        degrees = float(args[1])
                        radians = degrees * (math.pi/180.)
                        axisx = float(args[2])
                        axisy = float(args[3])
                        axisz = float(args[4])

                        c = math.cos(radians)
                        s = math.sin(radians)

                        vector = normalize(array([axisx,axisy,axisz]))
                        x = vector[0].item()
                        y = vector[1].item()
                        z = vector[2].item()

                        matrix = IDENTITY.copy()
                        matrix[0][0] = (x*x)*(1.-c) + c
                        matrix[0][1] = (x*y)*(1.-c) - (z*s)
                        matrix[0][2] = (x*z)*(1.-c) + (y*s)

                        matrix[1][0] = (y*x)*(1.-c) + (z*s)
                        matrix[1][1] = (y*y)*(1.-c) + c
                        matrix[1][2] = (y*z)*(1.-c) - (x*s)

                        matrix[2][0] = (z*x)*(1.-c) - (y*s)
                        matrix[2][1] = (z*y)*(1.-c) + (x*s)
                        matrix[2][2] = (z*z)*(1.-c) + c
                        #print matrix

                        transformBuffer = dot(matrix, transformBuffer)
                        #transformBuffer.append(matrix[:].copy())

                    elif args[0].__eq__("rotatec"):
                        degrees = float(args[1])
                        radians = degrees * (math.pi/180.)
                        axisx = float(args[2])
                        axisy = float(args[3])
                        axisz = float(args[4])
                        index1 = getListIndex(int(args[5]))
                        v1 = vertex_list[index1]

                        # Translate v1 to origin
                        toOrigin = IDENTITY.copy()
                        toOrigin[0][3] = -1. * v1.x
                        toOrigin[1][3] = -1. * v1.y
                        toOrigin[2][3] = -1. * v1.z
                        #print toOrigin

                        # Rotate around origin
                        c = math.cos(radians)
                        s = math.sin(radians)

                        vector = normalize(array([axisx,axisy,axisz]))
                        x = vector[0].item()
                        y = vector[1].item()
                        z = vector[2].item()

                        rotate = IDENTITY.copy()
                        rotate[0][0] = (x*x)*(1.-c) + c
                        rotate[0][1] = (x*y)*(1.-c) - (z*s)
                        rotate[0][2] = (x*z)*(1.-c) + (y*s)

                        rotate[1][0] = (y*x)*(1.-c) + (z*s)
                        rotate[1][1] = (y*y)*(1.-c) + c
                        rotate[1][2] = (y*z)*(1.-c) - (x*s)

                        rotate[2][0] = (z*x)*(1.-c) - (y*s)
                        rotate[2][1] = (z*y)*(1.-c) + (x*s)
                        rotate[2][2] = (z*z)*(1.-c) + c
                        #print rotate

                        # Return vertex to original position
                        revert = IDENTITY.copy()
                        revert[0][3] = v1.x
                        revert[1][3] = v1.y
                        revert[2][3] = v1.z
                        #print revert

                        m1 = dot(rotate, toOrigin)
                        m2 = dot(revert, m1)
                        transformBuffer = dot(m2, transformBuffer)
                        #print transformBuffer

                        #transformBuffer.append(revert[:].copy())
                        #transformBuffer.append(rotate[:].copy())
                        #transformBuffer.append(toOrigin[:].copy())

                    elif args[0].__eq__("scale"):
                        #apply translation to all vertices in buffer (don't reverse)
                        sx = float(args[1])
                        sy = float(args[2])
                        sz = float(args[3])

                        matrix = IDENTITY.copy()
                        matrix[0][0] = sx
                        matrix[1][1] = sy
                        matrix[2][2] = sz
                        #print matrix

                        transformBuffer = dot(matrix, transformBuffer)
                        #print transformBuffer

                        #transformBuffer.append(matrix[:].copy())

                    elif args[0].__eq__("scalec"):
                        sx = float(args[1])
                        sy = float(args[2])
                        sz = float(args[3])
                        index1 = getListIndex(int(args[4]))
                        v1 = vertex_list[index1]

                        # Translate v1 to origin
                        toOrigin = IDENTITY.copy()
                        toOrigin[0][3] = -1. * v1.x
                        toOrigin[1][3] = -1. * v1.y
                        toOrigin[2][3] = -1. * v1.z
                        #print toOrigin

                        # Scale
                        scale = IDENTITY.copy()
                        scale[0][0] = sx
                        scale[1][1] = sy
                        scale[2][2] = sz
                        #print matrix

                        # Return vertex to original position
                        revert = IDENTITY.copy()
                        revert[0][3] = v1.x
                        revert[1][3] = v1.y
                        revert[2][3] = v1.z
                        #print revert

                        m1 = dot(scale, toOrigin)
                        m2 = dot(revert, m1)
                        transformBuffer = dot(m2, transformBuffer)
                        #print transformBuffer

                        #transformBuffer.append(revert[:].copy())
                        #transformBuffer.append(scale[:].copy())
                        #transformBuffer.append(toOrigin[:].copy())

                    elif args[0].__eq__("multmv"):
                        a1 = float(args[1])
                        a2 = float(args[2])
                        a3 = float(args[3])
                        a4 = float(args[4])
                        a5 = float(args[5])
                        a6 = float(args[6])
                        a7 = float(args[7])
                        a8 = float(args[8])
                        a9 = float(args[9])
                        a10 = float(args[10])
                        a11 = float(args[11])
                        a12 = float(args[12])
                        a13 = float(args[13])
                        a14 = float(args[14])
                        a15 = float(args[15])
                        a16 = float(args[16])

                        matrix = array([[a1, a2, a3, a4],[a5, a6, a7, a8],[a9, a10, a11, a12],[a13, a14, a15, a16]])
                        #matrix = array([[a1, a5, a9, a13],[a2, a6, a10, a14],[a3, a7, a11, a15],[a4, a8, a12, a16]])

                        transformBuffer = dot(transformBuffer, matrix)
                        print transformBuffer

                        #print matrix
                        #transformBuffer.append(matrix[:].copy())

                    elif args[0].__eq__("loadmv"):
                        a1 = float(args[1])
                        a2 = float(args[2])
                        a3 = float(args[3])
                        a4 = float(args[4])
                        a5 = float(args[5])
                        a6 = float(args[6])
                        a7 = float(args[7])
                        a8 = float(args[8])
                        a9 = float(args[9])
                        a10 = float(args[10])
                        a11 = float(args[11])
                        a12 = float(args[12])
                        a13 = float(args[13])
                        a14 = float(args[14])
                        a15 = float(args[15])
                        a16 = float(args[16])

                        matrix = array([[a1, a2, a3, a4],[a5, a6, a7, a8],[a9, a10, a11, a12],[a13, a14, a15, a16]])
                        #matrix = array([[a1, a5, a9, a13],[a2, a6, a10, a14],[a3, a7, a11, a15],[a4, a8, a12, a16]])

                        transformBuffer = dot(transformBuffer, matrix)
                        print transformBuffer

                        #print matrix
                        #transformBuffer.insert(len(transformBuffer), matrix[:].copy())


                    elif args[0].__eq__("trig"):
                        # Apply and clear transformBuffer to all given vertices
                        while len(transformBuffer) > 0:
                            matrix = transformBuffer.pop()
                            for v in vertex_list:
                                result = dot(matrix,array([v.x, v.y, v.z, v.w]).reshape(4,1))
                                v.setX(result[0].item())
                                v.setY(result[1].item())
                                v.setZ(result[2].item())
                                v.setW(result[3].item())

                        # Retrieve vertices used for drawing triangle
                        index1 = getListIndex(int(args[1]))
                        index2 = getListIndex(int(args[2]))
                        index3 = getListIndex(int(args[3]))

                        v1 = vertex_list[index1]
                        v2 = vertex_list[index2]
                        v3 = vertex_list[index3]

                        c1 = vertex_colors[index1]
                        c2 = vertex_colors[index2]
                        c3 = vertex_colors[index3]

                        print vertex_colors
                        print c1
                        print c2
                        print c3
                        trig(v1, v2, v3, c1, c2, c3)

                    elif args[0].__eq__("cull"):
                            cull = True
                    elif args[0].__eq__("clipplane"):
                        p1 = float(args[1])
                        p2 = float(args[2])
                        p3 = float(args[3])
                        p4 = float(args[4])

                        plane = array([p1, p2, p3, p4])
                        clipplaneBool = True
                        print plane
                    else:
                        print "You know I can't read circle!"
            image.save(FILENAME)

main()