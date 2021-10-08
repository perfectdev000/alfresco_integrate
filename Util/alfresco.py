import requests
import json
from base64 import b64encode
import urllib.parse
from django.core.files.storage import FileSystemStorage
from zipfile import ZipFile
# from Util import google_sheets
import os


defSite = {
    'role': 'SiteManager',
    'visibility': 'PUBLIC',
    'guid': 'b4cff62a-664d-4d45-9302-98723eac1319',
    'description': 'This is a Sample Alfresco Team site.',
    'id': 'swsdp',
    'preset': 'site-dashboard',
    'title': 'Sample: Web Site Design Project'
}

host = 'http://localhost:8080/'
base_url = 'http://localhost:8080/alfresco/api/-default-/public/alfresco/versions/1/'
admin_name = 'admin'
admin_password = 'Alfresco'
user_password = ''
user_name = ''

host = 'http://35.178.166.45'
base_url = 'http://35.178.166.45/alfresco/api/-default-/public/alfresco/versions/1/'
admin_name = 'admin'
admin_password = 'i-0c09541dcba022c1e'
user_password = 'preset-alfresco-2020'

def makeAuthHeader(admin, admin_pass):
    userAndPass = b64encode(bytes('{}:{}'.format(admin, admin_pass), 'ascii')).decode('ascii')
    headers = {'Authorization': 'Basic %s' % userAndPass, 'content-type': 'application/json',
               'Accept': '*/*', 'Connection': 'keep-alive'}
    # print(headers)
    return headers


def makeAdminHeader(user, password):
    return makeAuthHeader(user, password)


def createPerson(username, email, password):
    print('============== alfresco : createPerson ============')
    headers = makeAdminHeader(admin_name, admin_password)
    headers['Accept'] = 'application/json'
    payload = {}
    payload['id'] = username
    payload['firstName'] = 'first'
    payload['lastName'] = 'last'
    payload['email'] = email
    payload['password'] = password
    url = base_url + 'people'
    r = requests.request('POST', url, headers=headers, data = json.dumps(payload))
    return r


def registerToSite(userData):
    print('============== alfresco : registerToSite ============')
    global user_name
    global user_password
    url = base_url + 'sites/' + defSite['id'] + '/members'
    body = [
        {
            'role': 'SiteCollaborator',
            'id': userData['id']
        }
    ]
    headers = makeAdminHeader(admin_name, admin_password)
    r = requests.post(url, data=json.dumps(body), headers=headers)
    return r


def getAllSiteNodes():
    print('============== alfresco : getAllSiteNodes ============')
    url = host + '/alfresco/service/slingshot/doclib/doclist/node/site/' + defSite['id'] + '/documentlibrary/'
    headers = makeAdminHeader(admin_name, admin_password)
    r = requests.get(url, headers=headers)
    dict_result = r.json()
    return r

def findNodesFromHome(keyword, user_name, user_password):
    print('============== alfresco : findNodesFromHome ============')
    url = base_url + 'queries/nodes'
    headers = makeAdminHeader(user_name, user_password)
    params = {
        'term': keyword,
        'rootNodeId': '-my-'
    }
    r = requests.get(url, headers=headers, params=params)
    dict_result = r.json()
    return dict_result


def getUserHomeDirectory(request, user_name, user_password):
    # dict_user = json.loads(request.user.serialize())[0]['fields']
    url = base_url + 'nodes/-root-/children?relativePath=User Homes/' + user_name + '&include=properties'
    headers = makeAdminHeader(user_name, user_password)
    r = requests.get(url, headers=headers)
    print('============== alfresco : getUserHomeDirectory -> url : ', url)
    children = r.json()
    return children['list']['entries']


def getUserHome(request, user_name, user_password):
    print('============== alfresco : getUserHome ============')
    url = base_url + 'nodes/-root-?relativePath=User Homes/' + user_name + '&include=properties'
    headers = makeAdminHeader(user_name, user_password)
    r = requests.get(url, headers=headers)
    children = r.json()
    return children['entry']


def getFolderChild(node_id, user_name, user_password):
    print('============== alfresco : getFolderChild ============')
    url = base_url + 'nodes/' + node_id + '/children?include=properties'
    headers = makeAdminHeader(user_name, user_password)
    r = requests.get(url, headers=headers)
    children = r.json()
    return children['list']['entries']


def createFolder(node_id, name, user_name, user_password):
    url = base_url + 'nodes/' + node_id + '/children'
    # url = 'http://35.178.166.45/alfresco/api/-default-/public/alfresco/versions/1/nodes/7cdee468-7261-4642-bf11-5b75e863a3dc/children'
    headers = makeAdminHeader(user_name, user_password)
    print('============== alfresco : createFolder ============')
    body = {
        'name': str(name),
        'nodeType': 'cm:folder'
    }
    r = requests.post(url, data=json.dumps(body), headers=headers)
    return r


def createFile(node_id, name, file, user_name, user_password):
    url = base_url + 'nodes/' + node_id + '/children'
    print('==== alfresco : createFile ====== url :', url)
    userAndPass = b64encode(bytes('{}:{}'.format(user_name, user_password), 'ascii')).decode('ascii')
    headers = {'Authorization': 'Basic %s' % userAndPass}
    try:
        files = [
            ('filedata', file.file.getvalue())
        ]
    except:
        files = [
            ('filedata', file.file)
        ]
    payload = {
        'name': name,
        'nodeType': 'cm:content',
        'overwrite':'true'
    }
    r = requests.request('POST', url, headers=headers, data = payload, files = files)
    print(url, headers, payload)
    # print(r)
    result = r.json()
    created_id = result['entry']['id']
    # createSharedLink(created_id, user_name, user_password)
    return result

def update_file(data, user_name, user_password):
    print('============== alfresco : update_file ============')
    url = base_url + 'nodes/' + data['parent_id'] + '/children'
    userAndPass = b64encode(bytes('{}:{}'.format(user_name, user_password), 'ascii')).decode('ascii')
    headers = {
        'Authorization': 'Basic %s' % userAndPass
    }
    f= open(data['filename'],'w+')
    f.write(data['file_content'].replace('\r',''))
    f.close()
    file_content = open(data['filename'], 'rb')
    files = [
        ('filedata', (data['filename'], file_content))
    ]
    payload = {
        'name': data['filename'] ,
        'nodeType': 'cm:content',
        'overwrite':'true'
    }
    r = requests.request('POST', url, headers=headers, data = payload, files = files)
    file_content.close()
    # print(url)
    # print(headers)
    # print(payload)
    # print(files)
    # print(r, r.headers)
    os.remove(data['filename'])
    result = r.json()
    # created_id = result['entry']['id']
    # createSharedLink(created_id, user_name, user_password)
    return result

def upload_url_document(node_id, url_file, user_name, user_password):
    print('============== alfresco : upload_url_document ============')
    r = requests.get(url_file)
    url_document = user_name + '.zip'
    if r.headers['Content-type'] == 'application/zip' :
        open(url_document, 'wb').write(r.content)
        with ZipFile(url_document, 'r') as zipObj:
            listOfFileNames = zipObj.namelist()
            zipObj.extractall()
            url = base_url + 'nodes/' + node_id + '/children'
            print('===== url : ', url)
            userAndPass = b64encode(bytes('{}:{}'.format(user_name, user_password), 'ascii')).decode('ascii')
            headers = {'Authorization': 'Basic %s' % userAndPass}
            for filename in listOfFileNames :
                try:
                    if (filename[-1:] == '/') : continue
                    file_content = open(filename, 'rb')
                    files = [
                        ('filedata', (filename, file_content))
                    ]
                    payload = {
                        'name': filename.split('/')[-1],
                        'nodeType': 'cm:content',
                        'cm:description' : 'url document upload'
                    }
                    r = requests.request('POST', url, headers=headers, data = payload, files = files)
                    file_content.close()
                    print(filename, r, r.headers)
                    os.remove(filename)
                except:
                    pass
        for filename in listOfFileNames :
            try:
                if (filename[-1:] == '/') :
                    os.rmdir(filename)
            except Exception as e:
                print(str(e))
                pass
        os.remove(url_document)
    result = []

    # result = r.json()
    # created_id = result['entry']['id']
    # createSharedLink(created_id)
    return result


def createSharedLink(node_id, user_name, user_password):
    print('============== alfresco : createSharedLink ============')
    url = base_url + 'shared-links'
    print('===== url : ', url)
    headers = makeAdminHeader(user_name, user_password)
    data = {
        'nodeId': node_id
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print(r.json())
    shared_link_id = r.json()['entry']['id']
    return shared_link_id

def getFileContent(node_id, user_name, user_password):
    print('============== alfresco : getFileContent ============')
    # http://localhost:8080/alfresco/api/-default-/public/alfresco/versions/1/nodes/3d061c1a-752c-44b7-a21d-1a494ce8459e/content
    # http://localhost:8080/alfresco/api/-default-/public/alfresco/versions/1/nodes/d8f561cc-e208-4c63-a316-1ea3d3a4e10e/content
    url = base_url + 'nodes/' +node_id +'/content'
    print( url)
    headers = makeAdminHeader(user_name, user_password)
    headers.pop('content-type', None)
    r = requests.get(url, headers=headers)
    print(r.headers)
    resp = r.text
    # print(r.text, r.content)
    return resp

def create_google_id(node_id, filename, user_name, user_password):
    print('============== alfresco : create_google_id ============')
    # http://localhost:8080/alfresco/api/-default-/public/alfresco/versions/1/nodes/d8f561cc-e208-4c63-a316-1ea3d3a4e10e/content
    # url = base_url + 'nodes/' +node_id +'/content'
    # headers = makeAdminHeader(user_name, user_password)
    # headers.pop('content-type', None)
    # try:
    #     r = requests.get(url, headers=headers)
    #     open(filename, 'wb').write(r.content)
    #     id = google_sheets.create_sheet(filename)
    #     print('id:',id)
    #     google_sheets.push_sheet(filename, id)
    #     return id
    # except Exception as e:
    #     print(str(e))
    #     return ""

def getNode(node_id, user_name, user_password):
    print('============== alfresco : getNode ============')
    url = base_url + 'nodes/' + node_id
    print(url)
    headers = makeAdminHeader(user_name, user_password)
    r = requests.get(url, headers=headers)
    resp = r.json()
    return resp['entry']

def getTags(node_id, user_name, user_password):
    print('============== alfresco : getTags ============')
    url = base_url + 'nodes/' + node_id + '/tags'
    print('===== url : ', url)
    headers = makeAdminHeader(user_name, user_password)
    r = requests.get(url, headers=headers).json()
    return r['list']['entries']


def putTag(node_id, tag, user_name, user_password):
    print('============== alfresco : putTag ============')
    url = base_url + 'nodes/' + node_id + '/tags'
    headers = makeAdminHeader(user_name, user_password)
    body = {'tag': tag}
    r = requests.post(url, data=json.dumps(body), headers=headers).json()
    return r


def getRating(request, node_id, user_name, user_password):
    print('============== alfresco : getRating ============')
    url = base_url + 'nodes/' + node_id + '/ratings'
    headers = makeAdminHeader(user_name, user_password)
    print(url)
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        resp = r.json()
        return resp['list']['entries']
    else:
        return []


def putRating(user_name, user_password,  node_id, rating):
    print('============== alfresco : putRating ============')
    url = base_url + 'nodes/' + node_id + '/ratings'
    headers = makeAdminHeader(user_name, user_password)
    if rating == 100:
        body = {
            'id': 'likes',
            'myRating': True
        }
        r = requests.post(url, data=json.dumps(body), headers=headers)
        return r
    elif rating == 200:
        r = requests.delete(url+'/likes', headers=headers)
        return r
    else:
        body = {
            'id': 'fiveStar',
            'myRating': int(rating)
        }
        headers = makeAdminHeader(admin_name, admin_password)
        r = requests.post(url, data=json.dumps(body), headers=headers)
        return r

def getFavorites(request, node_id, user_name, user_password):
    print('============== alfresco : getRating ============')
    url = base_url + 'people/' + user_name + '/favorites/' + node_id
    headers = makeAdminHeader(user_name, user_password)
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return 1
    else:
        return 0

def putFavorites(user_name, user_password,  node_id, favo):
    print('============== alfresco : putFavorites ============')
    headers = makeAdminHeader(user_name, user_password)
    if favo :
        url = base_url + 'people/' + user_name + '/favorites/'
        body = {
            'target':{
                'file' : { 'guid' : node_id }
                }
        }
        r = requests.post(url, data=json.dumps(body), headers=headers)
        print(r)
        return r
    else:
        url = base_url + 'people/' + user_name + '/favorites/' + node_id
        r = requests.delete(url, headers=headers)
        print(r)
        return r
def favorites_list(user_name, user_password):
    print('============== alfresco : favorites_list ============')
    headers = makeAdminHeader(user_name, user_password)
    url = base_url + 'people/' + user_name + '/favorites/'
    r = requests.get(url, headers=headers)
    print(r.json()['list']['entries'])
    return r

def getDetailedData(entries, user_name, user_password):
    print('============== alfresco : getDetailedData ============')
    for item in entries:
        item['tag'] = getTags(item['entry']['id'],user_name, user_password)
        # item['rating'] = getRating(item['entry']['id'],user_name, user_password)
    return entries


def deleteNode(node_id, user_name, user_password):
    print('============== alfresco : deleteNode ============')
    url = base_url + 'nodes/' + node_id
    print('===== url : ', url)
    headers = makeAdminHeader(user_name, user_password)
    r = requests.delete(url, headers=headers)
    return r


def download_file(node_id, user_name, user_password):
    print('============== alfresco : download_file ============')
    # http://localhost:8080/alfresco/api/-default-/public/alfresco/versions/1/nodes/3d061c1a-752c-44b7-a21d-1a494ce8459e/content
    # http://localhost:8080/alfresco/api/-default-/public/alfresco/versions/1/nodes/d8f561cc-e208-4c63-a316-1ea3d3a4e10e/content
    url = base_url + 'nodes/' +node_id +'/content'
    print( url)
    headers = makeAdminHeader(user_name, user_password)
    headers.pop('content-type', None)
    r = requests.get(url, headers=headers)
    return r