import os
from dotenv import load_dotenv

class EnvDetails:
  def __init__(self, e):
    self.env = e
    # Load environment configuration
    load_dotenv()

  def get_db_user(self):
    return os.getenv('{}_db_user'.format(self.env))

  def get_db_pass(self):
    return os.getenv('{}_db_pass'.format(self.env))

  def get_db_host(self):
    return os.getenv('{}_db_host'.format(self.env))

  def get_db_port(self):
    return os.getenv('{}_db_port'.format(self.env))

  def get_db_name(self):
    return os.getenv('{}_db_name'.format(self.env))

  def get_preservation_profile(self):
    return os.getenv('{}_preservation_profile'.format(self.env))

  def get_preservation_endpoint(self):
    return os.getenv('{}_preservation_endpoint'.format(self.env))

  def get_preservation_bucket(self):
    return os.getenv('{}_preservation_bucket'.format(self.env))


  def get_delivery_profile(self):
    return os.getenv('{}_delivery_profile'.format(self.env))

  def get_delivery_endpoint(self):
    return os.getenv('{}_delivery_endpoint'.format(self.env))

  def get_delivery_bucket(self):
    return os.getenv('{}_delivery_bucket'.format(self.env))

  def get_file_api(self, path):
    return os.getenv('{}_file_api'.format(self.env)).format(path)

  def get_s3pather(self, obj_urn, file_id):
    return os.getenv('{}_s3pather'.format(self.env)).format(obj_urn, file_id)

