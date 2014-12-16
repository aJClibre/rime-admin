#!/usr/local/bin/python
#
#
# Answers to the Ajax requests (POST and GET) from js/AdminLTE/dashboard.js
# Returns JSON
#
# text/plain par defaut et donc resultat en json attendu
# application/json et text/plain idem
#print "Content-Type: application/json\n"
# 
#
# test : $ curl http://emz.pont-entente.org/rime-admin/ajax/testPsyco.py -d '{"param": {"Hello":"World"}}'
# request : SELECT form_response, incident_title, incident_description, incident_date, location_name, latitude, longitude
#           FROM `form_response` AS r, `form_field` AS f, `incident` AS i, `location` AS l
#           WHERE r.form_field_id = f.id AND r.incident_id = i.id AND i.location_id = l.id 
#           AND field_name = 'NB de cas'

print

# http://webpython.codepoint.net/cgi_debugging
import cgitb
cgitb.enable()
import sys,cgi,json
# ajout des chemins vers les modules installes en local
sys.path.insert(0, "/home/users/k1013/.local/lib/python2.7/site-packages/")
import mysql.connector
from  mysql.connector import errorcode, InterfaceError

from config import BdD
#import simplejson


class SendResult(object):

    def __init__(self):

        self.result = {}
        self.result['success'] = True
        self.result['message'] = ""
        #result['keys'] = ",".join(params.keys())


    def addToData(self, datas, key):

        self.result[key] = {}
        self.result[key]['data'] = datas
    

    def sendIfError(self, errors):
        
        if errors :
            
            self.result['success'] = False
            self.result['message'] = errors


    def writeStdout(self, params):
        for k, v in params.items():
            self.result[k]['params'] = v
        sys.stdout.write(json.dumps(self.result,indent=1))
        sys.stdout.write("\n")
        sys.stdout.close()


class FactoryRequest(object):

    def __init__(self):

        self._champs = [form_response, incident_title, incident_description, incident_date, location_name, latitude, longitude]

    @property
    def request(self, request):
        
        return getattr(self, "_request", None)


    @request.setter
    def request(self, request):
        
        self._request = request


    def populateRequest(self, **data):
        
        self._request % data



class RequestBdD(object):

    def __init__(self, cursor):
                
        RequestBdD.cursor = cursor

    
    @property
    def error(self):
        return getattr(self, "_error", None)


    def prepareReq(self, req, params):
        
        return req % params

    
    def executeReq(self, req, params):

        self._request = self.prepareReq(req, params)

        try:
            RequestBdD.cursor.execute(self._request)
        except Exception, err:
            self._error = 'Error SQL request: \"%s\"' % err
   

    def resultAll(self):

        try : 
            return RequestBdD.cursor.fetchall()
        except InterfaceError :
            self._error = 'Error SQL request: InterfaceError'


    def resultOne(self):

        return RequestBdD.cursor.fetchone()



class ConnexionBdD(object):

    def __init__(self):
        
        self.database = BdD.database
        self.user = BdD.user
        self.password = BdD.password
        self.conne = None
        self.connexion()


    @property
    def cursor(self):
    
        return getattr(self, "_cursor", None)
    
    
    @property
    def error(self):
        
        return getattr(self, "_error", None)


    def connexion(self):
        
        try:
            self.conne =  mysql.connector.connect(database=self.database, user=self.user, password=self.password)
            # Open a cursor to perform database operations
            self._cursor = self.conne.cursor()

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                self._error = "Something is wrong with your user name or password"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                self._error = "Database does not exists"
            else:
                self._error = 'Error Connexion: \"%s\"' % err


    def closeConnexion(self):
        
        if self._cursor:
            self._cursor.close()

        if self.conne: 
            self.conne.close()

    


# fonction de connexion a la BdD
def conn():

    # Connect to an existing database
    conne = ConnexionBdD()

    # POST parameters from appli.js
    params = cgi.FieldStorage()
    
    requests_params = {}
    
    # from string params to requests_params dictionnary
    for k in params.keys() :
        request_name, b = k.split("[")
        
        if not requests_params.has_key(request_name): 
            requests_params[request_name] = {}

        request_value, c = b.split("]")

        requests_params[request_name][request_value] = params.getvalue(k)
    
    request = RequestBdD(conne.cursor)

    send = SendResult()

    query = ("SELECT %(fields_select)s "
               "FROM form_response AS r, form_field AS f, incident AS i, location AS l "
               "WHERE r.form_field_id = f.id AND r.incident_id = i.id AND i.location_id = l.id "
               "AND field_name = '%(fields_where)s'") # 'NB de cas'

    
    for k,v in requests_params.items() :
        
        request.executeReq(query, v)
   
        send.sendIfError(request.error)
        
        result = request.resultAll()

        send.addToData(result, k)

    conne.closeConnexion()

    send.writeStdout(requests_params)


# connexion function call
conn()

