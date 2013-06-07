"""
For of Apurva Mehta's Python library for the crunchbase api.
Copyright (c) 2013 Jennifer Rubinovitz

"""

__author__  = 'Jennifer Rubinovitz'
__version__ = '0.1'


import urllib2
import urllib
import simplejson as json

API_BASE_URL = "http://api.crunchbase.com/"
API_VERSION  = "1"
API_URL      = API_BASE_URL + "v" + "/" + API_VERSION + "/"

class Crunchbase:

  def __init__(self, api_key):
    self.api_key = api_key
    return None

  def __webRequest(self, url):
    try:
      response = urllib2.urlopen(url)
      result = response.read()
      return result
    except urllib2.HTTPError as e:
      raise CrunchBaseError(e)

  def __getJsonData(self, namespace, query=""):
    url = API_URL + namespace + query + ".js?api_key="+ self.api_key
    response_dict = json.loads(self.__webRequest(url))
    return response_dict

  def getCompanyData(self, name):
    '''This returns the data about a company in JSON format.'''

    result = self.__getJsonData("company", "/%s" % name)
    return result

  def getPersonData(self, *args):
    '''This returns the data about a person in JSON format.'''

    result = self.__getJsonData("person", "/%s" % '-'.join(args).lower().replace(' ','-'))
    return result

  def getFinancialOrgData(self, orgName):
    '''This returns the data about a financial organization in JSON format.'''

    result = self.__getJsonData("financial-organization", "/%s" % orgName)
    return result

  def getProductData(self, name):
    '''This returns the data about a product in JSON format.'''

    result = self.__getJsonData("product", name)
    return result

  def getServiceProviderData(self, name):
    '''This returns the data about a service provider in JSON format.'''

    result = self.__getJsonData("service-provider", "/%s" % name)
    return result

  def listCompanies(self):
    '''This returns the list of companies in JSON format.'''

    result = self.__getJsonData("companies")
    return result

  def listPeople(self):
    '''This returns the list of people in JSON format.'''

    result = self.__getJsonData("people")
    return result

  def listFinancialOrgs(self):
    '''This returns the list of financial organizations in JSON format.'''

    result = self.__getJsonData("financial-organizations")
    return result

  def listProducts(self):
    '''This returns the list of products in JSON format.'''

    result = self.__getJsonData("products")
    return result

  def listServiceProviders(self):
    '''This returns the list of service providers in JSON format.'''

    result = self.__getJsonData("service-providers")
    return result

class CrunchBaseResponse(object):
  def __init__(self, **kwargs):
    self.__dict__.update(kwargs)

  def __repr__(self):
    return '%s(%r)' % (self.__class__.__name__, self.__dict__)

class CrunchBaseError(Exception):
  pass
