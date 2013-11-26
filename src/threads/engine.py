import threading
import Queue

import ode
import time

from src.threads.resources import car

class Worker(threading.Thread):
  UPS = 30.0

  def getDepthData(self):
    if(not(self.queue.empty())):
      self.dataPlane = self.queue.get()

  # Collision callback
  def near_callback(self, args, obj1, obj2):
    # Check if the objects do collide
    contacts = ode.collide(obj1, obj2)
  
    # Create contact joints
    (world, contactGroup) = args
  
    for contact in contacts:
      contact.setBounce(0.2)
  
      # Friction
      contact.setMu(5000)
  
      # Create a joint between them to repel
      joint = ode.ContactJoint(world, contactGroup, contact)
      joint.attach(obj1.getBody(), obj2.getBody())
  
  def initODE(self):
    self.world = ode.World()
    self.world.setGravity((0, 0, -9.81))
    self.world.setERP(0.2)
    self.world.setCFM(1E-5)
  
    self.collisionSpace = ode.Space()
  
    meshData = ode.TriMeshData()
    meshData.build(self.dataPlane.toRawVertices(),
                     self.dataPlane.toTriangleIndexes())
    self.ground = ode.GeomTriMesh(meshData, self.collisionSpace)
    self.ground.setPosition((-self.dataPlane.width / 2.0, 
                             -self.dataPlane.height / 2.0, 0))
  
    self.contacts = ode.JointGroup() 
    self.car = car.Car(self.world, self.collisionSpace)

  def createSphere(self, world, collisionSpace, x, y, z, r, mass):
    sphereBody = ode.Body(world)

    M = ode.Mass()
    M.setSphereTotal(mass, r)
    M.mass = mass

    sphereBody.setMass(M)
    sphereBody.setPosition((x, y, z))

    sphereGeom = ode.GeomSphere(collisionSpace, r)
    sphereGeom.setBody(sphereBody)

    return (sphereBody, sphereGeom)

  def __init__(self, queue):
    self.depthData = None
    self.car = None
    self.queue = queue
    self.getDepthData()

    self.exit = False
    self.paused = True
    threading.Thread.__init__(self)

  def run(self):
    self.initODE()
    simTimeStep = 1.0 / Worker.UPS

    while(not(self.exit)):
      if(not(self.paused)):
        self.collisionSpace.collide((self.world, self.contacts),
                                      self.near_callback)
        self.world.step(simTimeStep)
        time.sleep(simTimeStep)

        self.contacts.empty()
      else:
        time.sleep(simTimeStep)

  def stop(self):
    self.exit = True
