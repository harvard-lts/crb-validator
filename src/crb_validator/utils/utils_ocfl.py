import requests

class OcflUtils:

  def __init__(self):
    self.s3lookupurl = "http://ltsds-cloud-prod-1.lib.harvard.edu:23097/api/lookup"

  def ocfl_path_to_object(self, ois_urn):
    """This method converts an OIS URN into the OCFL path for an Object
       Example input: urn-3:HUL.DRS.OBJECT:31852370"""

    nss = ois_urn.upper().split("OBJECT:")[1]
    reverse = nss[::-1]
    first = reverse[0:4] 
    second = reverse[4:8] 
    return f"%s/%s/%s" %(first, second, nss)

  # Not using in this project below 
  def ocfl_path_to_file(self, file_id):
    res = requests.get(f'{self.s3lookupurl}/{file_id}', timeout=2)
    json = res.json()
    if json['status'] != 200:
      json['fileID'] = file_id
      raise Exception("Error looking up OCFL path for: {}".format(str(json)))
    else:
      return json['NSSPath'], json['FileName']
