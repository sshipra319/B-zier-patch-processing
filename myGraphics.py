# Shipra Saini
# sxs2152
# 2018-12-04

#----------------------------------------------------------------------
# This code was originally created by Prof. Farhad Kamangar.
# It has been significantly modified and updated by Brian A. Dalio for
# use in CSE 4303 / CSE 5365 in the 2018 Fall semester.

import CohenSutherland
import ModelData
import BézierPatch

#----------------------------------------------------------------------
class cl_world :
  def __init__( self, objects = [], canvases = [] ) :
    self.objects = objects
    self.canvases = canvases

  def add_canvas( self, canvas ) :
    self.canvases.append( canvas )
    canvas.world = self

  def reset( self ) :
    self.objects = []
    for canvas in self.canvases :
      canvas.delete( 'all' )

  def create_graphic_objects( self, canvas, model, doClip, doPerspective, doEuler, resolution ) :
      
      self.model = model
      face = model.getFaces()
      patches = model.getPatches()
      vertices = model.getVertices()
      width = int(canvas.cget( "width" ))
      height = int(canvas.cget( "height" ))          
      viewport = model.getViewport()
      xmin = width*viewport[0]
      ymin = height*viewport[1] 
      xmax = width*viewport[2]
      ymax = height*viewport[3]
      portal = (xmin, ymin, xmax, ymax)
      
      for patch in patches:
          points = BézierPatch.resolve(resolution, patch, vertices)
          
          for row in range (0, resolution-1):
              rowStart = row * resolution            
              for column in range(0, resolution - 1):
                  here = rowStart + column
                  there = here + resolution            
                  triangleA = (points[here], points[there], points[there + 1])
                  triangleB = (points[there + 1], points[here + 1], points[here])
              
                  self.drawTriangle(canvas, triangleA, doClip, doPerspective, doEuler, portal)
                  self.drawTriangle(canvas, triangleB, doClip, doPerspective, doEuler, portal)
          
      for faces in face:
          vertex1 = model.getTransformedVertex(faces[0], doPerspective, doEuler)
          vertex2 = model.getTransformedVertex(faces[1], doPerspective, doEuler)
          vertex3 = model.getTransformedVertex(faces[2], doPerspective, doEuler)
          
          Vertices = (vertex1, vertex2, vertex3)
          
          self.drawTriangle(canvas, Vertices, doClip, doPerspective, doEuler, portal)          
          
#          if (doClip == True):  
#              
#              b1Code = CohenSutherland.clipLine(vertex1[0], vertex1[1], vertex2[0], vertex2[1], portal)
#              b2Code = CohenSutherland.clipLine(vertex2[0], vertex2[1], vertex3[0], vertex3[1], portal)
#              b3Code = CohenSutherland.clipLine(vertex3[0], vertex3[1], vertex1[0], vertex1[1], portal)
#              
#              if((b1Code[0]) == True):
#                  self.objects.append( canvas.create_line(b1Code[1], b1Code[2], b1Code[3], b1Code[4] ) )
#                  
#              if((b2Code[0]) == True):
#                  self.objects.append( canvas.create_line(b2Code[1], b2Code[2], b2Code[3], b2Code[4] ) )
#                  
#              if((b3Code[0]) == True):
#                  self.objects.append( canvas.create_line(b3Code[1], b3Code[2], b3Code[3], b3Code[4] ) )
#                  
#          else:
#              self.objects.append( canvas.create_line(vertex1[0], vertex1[1], vertex2[0], vertex2[1] ) )
#              self.objects.append( canvas.create_line(vertex2[0], vertex2[1], vertex3[0], vertex3[1] ) )
#              self.objects.append( canvas.create_line(vertex3[0], vertex3[1], vertex1[0], vertex1[1] ) )
      
    # 1. Create a line that goes from the upper left
    #    to the lower right of the canvas.s
#    self.objects.append( canvas.create_line(
#      0, 0, canvas.cget( 'width' ), canvas.cget( 'height' ) ) )

    # 2. Create a line that goes from the lower left
    #    to the upper right of the canvas.
#    self.objects.append( canvas.create_line(
#      canvas.cget( 'width' ), 0, 0, canvas.cget( 'height' ) ) )

    # 3. Create an oval that is centered on the canvas and
    #    is 50% as wide and 50% as high as the canvas.
#    self.objects.append( canvas.create_oval(
#      int( 0.25 * int( canvas.cget( 'width' ) ) ),
#      int( 0.25 * int( canvas.cget( 'height' ) ) ),
#      int( 0.75 * int( canvas.cget( 'width' ) ) ),
#      int( 0.75 * int( canvas.cget( 'height' ) ) ) ) )
  def drawTriangle(self, canvas, points, doClip, doPerspective, doEuler, portal):
      
      v1 = self.model.transformXYZ(points[0], doPerspective, doEuler)
      v2 = self.model.transformXYZ(points[1], doPerspective, doEuler)
      v3 = self.model.transformXYZ(points[2], doPerspective, doEuler)
      
      if (doClip == True):
          b1Code = CohenSutherland.clipLine(v1[0], v1[1], v2[0], v2[1], portal)
          b2Code = CohenSutherland.clipLine(v2[0], v2[1], v3[0], v3[1], portal)
          b3Code = CohenSutherland.clipLine(v3[0], v3[1], v1[0], v1[1], portal)
              
          if((b1Code[0]) == True):
             self.objects.append( canvas.create_line(b1Code[1], b1Code[2], b1Code[3], b1Code[4] ) )
                  
          if((b2Code[0]) == True):
              self.objects.append( canvas.create_line(b2Code[1], b2Code[2], b2Code[3], b2Code[4] ) )
                  
          if((b3Code[0]) == True):
             self.objects.append( canvas.create_line(b3Code[1], b3Code[2], b3Code[3], b3Code[4] ) )
                  
      else:
          self.objects.append( canvas.create_line(v1[0], v1[1], v2[0], v2[1] ) )
          self.objects.append( canvas.create_line(v2[0], v2[1], v3[0], v3[1] ) )
          self.objects.append( canvas.create_line(v3[0], v3[1], v1[0], v1[1] ) )
          
      
      
  def redisplay( self, canvas, event ) :
      pass
#    if self.objects :
#      canvas.coords(self.objects[ 0 ], 0, 0, event.width, event.height )
#      canvas.coords(self.objects[ 1 ], event.width, 0, 0, event.height )
#      canvas.coords(self.objects[ 2 ],
#        int( 0.25 * int( event.width ) ),
#        int( 0.25 * int( event.height ) ),
#        int( 0.75 * int( event.width ) ),
#        int( 0.75 * int( event.height ) ) )

#----------------------------------------------------------------------
