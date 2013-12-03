import requests

class Client(object):
  url = 'http://terramotus.aoneill.org'

  def __init__(self, mapDir = "", imageDir = ""):
    self.mapDir = mapDir
    self.imageDir = imageDir

  def send(self, name):
    path = self.mapDir + "/" if(self.mapDir) else ""
    path += name
    files = {"upload": open(path, 'r')}
    params = {"filename": name}
    r = requests.post(Client.url, files = files, params = params)
    sanitized = map(lambda elem : elem.encode("ascii","ignore"),
                    r.text.split("\n"))
    return sanitized

  def recv(self, name):
    path = self.mapDir + "/" if(self.mapDir) else ""
    path += name
    params = {"download": name}
    r = requests.post(Client.url, params = params)
    sanitized = map(lambda elem : elem.encode("ascii","ignore"),
                    r.text.split("\n"))

    filename = sanitized[0]
    data = sanitized[1:]
    f = open(path, "w+")
    for line in xrange(len(data)):
      out = data[line] + ("\n" if(line < len(data) - 1) else "")
      f.write(out) 
    f.close()

    return (filename, data)

  def removeExtension(self, name):
    return name[:len(name) - 4]

  def toImgPath(self, name):
    return "images/" + self.removeExtension(name)

  def getImg(self, name):
    r = requests.get(Client.url + "/" + self.toImgPath(name), stream=True)
    path = self.imageDir + "/" if(self.imageDir) else ""
    path += self.removeExtension(name) + ".png"
    f = open(path, "w+")
    for data in r.iter_content(chunk_size = 1024):
      if(data):
        f.write(data)
        f.flush()

    f.close()

  def getList(self, args = None):
    if(args is None): args = "empty"
    params = {"list": args}
    r = requests.post(Client.url, params = params)
    sanitized = map(lambda elem : elem.encode("ascii","ignore").strip(),
                    r.text.split(","))
    return sanitized
