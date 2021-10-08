from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files.base import ContentFile
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from product.forms import FileInputForm, RenameForm, SearchForm, UrlFileInputForm, Upload_files_from_alfresco_Form
from .models import Files_upload, Project_List, Project_file_List
import requests
import json
from pdf2image import convert_from_path, convert_from_bytes
from Util import alfresco
import os
import datetime
# from PIL import Image
# import pytesseract
import sys
# from pdf2image import convert_from_path
import os
import subprocess
import shutil

type_choices = {
    'csv': {'csv', 'xlsx', 'xls'},
    'pdf': {'pdf', 'txt'},
    'jpg': {'pdf', 'jpeg', 'jpg'},
    'jpeg': {'pdf', 'jpeg', 'jpg'},
}

main_table_data = {}
current_folder = ''

@login_required(login_url='/login/?next=dashboard')
def dashboard(request):
    print("=========== product -> dashboard(request) ===============")
    user_name = request.session['usr']
    user_password = request.session['pwd']
    print(user_name, user_password)
    global main_table_data
    sorted = False
    value = None
    is_old = 0
    data = Files_upload.objects.filter(user=request.user).order_by('name').all()
    form = SearchForm()
    if request.method == 'POST':
        is_old = 1
        form = SearchForm(request.POST or None)
        if form.is_valid():
            value = form.cleaned_data.get('search')
            data = data.filter(name__icontains=value)
    if request.GET.get('sorted'):
        # data = data.order_by('-date')
        sorted = True
    visible = False
    if request.session.get('visible', None) is not None:
        visible = request.session['visible']
        request.session['visible'] = False
    if request.session.get('folder', None) is not None:
        entries = alfresco.getFolderChild(request.session['folder'], user_name, user_password)
        folder = {'id': request.session['folder'], 'name': request.session['folder_name'], 'parentId': request.session['parent']}
    else:
        entries = alfresco.getUserHomeDirectory(request, user_name, user_password)
        folder = alfresco.getUserHome(request, user_name, user_password)
        request.session['folder'] = folder['id']
        request.session['parent'] = folder['parentId']
        request.session['folder_name'] = folder['name']
    node_entry = alfresco.getNode(folder['id'], user_name, user_password)
    print("dashboard-node_entry:", node_entry)
    data = alfresco.getDetailedData(entries, user_name, user_password)
    main_table_data = entries
    dashboard_method = False
    project_name =""
    project_file_list = []
    try:
        if request.session['dashboard'] == 'open_project':
            project_name = request.session['project_name']
            rows = Project_file_List.objects.filter(user=request.user, project_name = project_name)
            for row in rows :
                project_file_list.append(row.file_name)
            dashboard_method = True
            request.session['dashboard'] = 'main_dashboard'
    except:
        pass
    context = {'data': data, 'sorted': sorted, 'title': 'Sensai|Dashboard', 'value': value, 'visible':visible, 'entries': entries, 'parent_id': folder['parentId'], 'folder_id': folder['id'], 'folder_name': node_entry['name'], 'is_old': is_old, 'dashboard_method':dashboard_method, 'project_file_list':project_file_list,'project_name':project_name}
    return render(request, 'dashboard.html', context)

@login_required(login_url='/login/?next=dashboard')
def main_table(request, parent_id):
    user_name = request.session['usr']
    user_password = request.session['pwd']
    global main_table_data, current_folder
    if parent_id:
        entries = alfresco.getFolderChild(parent_id, user_name, user_password)
    node = alfresco.getNode(parent_id, user_name, user_password)
    request.session['folder'] = parent_id
    request.session['parent'] = node['parentId']
    html = render_to_string('layouts/data/data_list.html', {'sorted': sorted, 'visible':True, 'title': 'Sensai|Dashboard', "value": "value", 'entries': entries, 'folder_name': node['name'], 'parent_id': parent_id})
    main_table_data = entries
    return HttpResponse(html)

@login_required(login_url='/login/?next=dashboard')
def file_manager(request, parent_id):
    user_name = request.session['usr']
    user_password = request.session['pwd']
    global main_table_data
    print("=========== product -> file_manager(request, parent_id) ===============")
    if parent_id:
        entries = alfresco.getFolderChild(parent_id, user_name, user_password)

    node_entry = alfresco.getNode(parent_id, user_name, user_password)
    if "parentId" not in node_entry:
        node_entry['parentId'] = "-root-"

    folder = alfresco.getUserHome(request, user_name, user_password)
    if folder['parentId'] == node_entry['id']:
        return HttpResponse(status=500)
    print("=== filemanager:",entries)
    print("=== filemanager:",node_entry)
    html = render_to_string('product/partial/file-manager-modal.html',
                            {'entries': entries, 'parent_id': node_entry['parentId'], 'folder_name': node_entry['name'], 'folder_id': parent_id})
    main_table_data = entries
    return HttpResponse(html)

@login_required(login_url='/login/?next=dashboard')
def browser_open_file(request, node_id):
    global main_table_data
    user_name = request.session['usr']
    user_password = request.session['pwd']
    print("================ browser_open_file =================")
    node_entry = alfresco.getNode(node_id, user_name, user_password)
    print(node_entry)
    document_type = node_entry['content']['mimeType']
    print("document_type:",document_type)
    name = node_entry['name']
    # if "qshare:sharedId" not in node_entry['properties']:
    #     link_id = alfresco.createSharedLink(node_id, user_name, user_password)
    # else:
    #     link_id = node_entry['properties']["qshare:sharedId"]
    try:
        path = settings.MEDIA_ROOT+'/share'
        try:
            shutil.rmtree(path)
        except:
            pass
        response = alfresco.download_file(node_id, user_name, user_password)
        filepath = "share/{}".format(name)
        path = default_storage.save(filepath, ContentFile(response.content))
        link_id = default_storage.url(path)
    except :
        pass
    print("link_id --------->", link_id)
    private_link_id = node_entry['id']
    parent_id = node_entry['parentId']
    if ("spreadsheet" in str(document_type)) or ("ms-excel" in str(document_type)):
        google_id = alfresco.create_google_id(private_link_id, name, user_name, user_password)
    else:
        google_id = ""
    return JsonResponse({"private_link_id": private_link_id,"parent_id": parent_id,"link_id": link_id,"document type":document_type,"name":name,"google_id":google_id})

@login_required(login_url='/login/?next=dashboard')
def create_folder(request, parent_id, folder_name):
    alfresco.createFolder(parent_id, folder_name, request.session['usr'],request.session['pwd'])
    return JsonResponse({})

@login_required(login_url='/login/?next=dashboard')
def bottom_panel(request, node_id):
    print("======= Product  >  view  >  bottom_panel ========")
    user_name = request.session['usr']
    user_password = request.session['pwd']
    global main_table_data
    if node_id == "null":
        return HttpResponse('')

    for item in main_table_data:
        if node_id == item['entry']['id']:
            data = item['entry']
    print("----", data)
    tags = alfresco.getTags(node_id, user_name, user_password)
    ratings = alfresco.getRating(request, node_id, user_name, user_password)
    favorites = alfresco.getFavorites(request, node_id, user_name, user_password)
    # if "qshare:sharedId" in data['properties']:
    #     link_id = data['properties']['qshare:sharedId']
    #     print("--------already-link_id :",link_id)
    # else:
    #     link_id = alfresco.createSharedLink(node_id, user_name, user_password)
    #     print("--------new-link_id :",link_id)try:
    try:
        path = settings.MEDIA_ROOT+'/share'
        try:
            shutil.rmtree(path)
        except:
            pass
        response = alfresco.download_file(node_id, user_name, user_password)
        txt = response.headers['Content-Disposition']
        print(txt)
        filename = txt[22:txt.find('; filename*')-1]
        print(filename)
        filepath = "share/{}".format(filename)
        path = default_storage.save(filepath, ContentFile(response.content))
        link_id = default_storage.url(path)

        print("---link_id:", link_id)
    except Exception as e:
        print(str(e))
        pass
    unreadable = [
        "qshare:sharedId",
        "cm:likesRatingSchemeCount",
        "cm:lastThumbnailModification",
        "cm:taggable",
        "cm:fiveStarRatingSchemeCount",
        "cm:fiveStarRatingSchemeTotal",
        "cm:likesRatingSchemeTotal",
        "qshare:sharedBy"
    ]
    context = {"data": data, "tags": tags, "unreadable_keys": unreadable, 'link_id': link_id, 'ratings': ratings, 'favorites':favorites, 'five_number':range(1,6)}
    html = render_to_string('product/partial/bottom_panel.html', context=context)
    return HttpResponse(html)

@login_required(login_url='/login/?next=dashboard')
def post_rating(request, node_id, rating):
    print("====== post_rating =====: ")
    alfresco.putRating(request.session['usr'], request.session['pwd'] , node_id, rating)
    data = {
        'message': 'sucess'
    }
    return JsonResponse(data)

def post_favorites(request, node_id, favo):
    print("====== post_favorites =====: ")
    alfresco.putFavorites(request.session['usr'], request.session['pwd'] , node_id, favo)
    data = {
        'message': 'sucess'
    }
    return JsonResponse(data)

@login_required(login_url='/login/?next=dashboard')
def post_tag(request, node_id, tag):
    alfresco.putTag(node_id, tag, request.session['usr'],request.session['pwd'])
    data = {
        'message': 'sucess'
    }
    return JsonResponse(data)

@login_required(login_url='/login/')
def add_file(request, value):
    print("=============== product : add_file ==================")
    form = FileInputForm(initial={'user': request.user})
    print(request.FILES)
    print('request.user :',request.user)
    if value not in type_choices:
        print(value)
        raise form.ValueError('Invalid arguments')
    if request.method == "POST":
        form = FileInputForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('up_file')
            print(request.FILES)
            for file in files:
                value_type = str(file).split('.')[-1]
                name = str(file).split('/')[-1]
                if '.' not in str(file) or value_type not in type_choices[value]:
                    messages.error(request, f'Make sure your file contains {type_choices[value]}')
                    return HttpResponseRedirect(reverse('add_file', kwargs={'value': value}))
                Files_upload(user=request.user, up_file=file, data_type=value_type, name=name)
                print("============ post request session : ", request.session.get('folder', ''))
                alfresco.createFile(request.session.get('folder', ''), str(file), file, request.session['usr'],request.session['pwd'])
                request.session['visible']=True
            return redirect('dashboard')
        else:
            for error in form.errors:
                messages.error(request, error)
    context = {
        'form': form
    }
    return render(request, 'product/add_file.html', context)

@login_required(login_url='/login/')
def add_url_file(request):
    print("=============== product : add_url_file ==================")
    form = UrlFileInputForm(initial={'user': request.user})
    if request.method == "POST":
        form = UrlFileInputForm(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            url = data.get('from_url')
            user_name = request.session['usr']
            user_password = request.session['pwd']
            alfresco.upload_url_document(request.session.get('folder', ''), url, user_name,user_password)
            return redirect('dashboard')
        else:
            for error in form.errors:
                messages.error(request, error)
    context = {
        'form': form
    }
    return render(request, 'product/add_url_file.html', context)

@login_required(login_url='/login/')
def delete_files(request):
    payload = json.loads(request.body.decode('utf-8'))
    print("======== delete_files ===== payload", payload)
    for node in payload['nodes']:
        alfresco.deleteNode(node, request.session['usr'],request.session['pwd'])
        print("==== deleting node======", node)
    data = {
        'message': 'sucess'
    }
    return JsonResponse(data)

@login_required
def update_file(request):
    print("=============== product : update_file ==================")
    data = request.POST
    alfresco.update_file(data, request.session['usr'],request.session['pwd'])
    print(data)
    return dashboard(request)

@login_required
def open_file(request):
    files = Files_upload.objects.filter(user=request.user).all()
    file_name = {}
    for file in files:
        file_name[file.id] = str(file.up_file).split('/')[-1]
    context = {"files": files,
               'file_name': file_name}
    return render(request, 'product/open_file.html', context)

@login_required
def rename_file(request, pk):
    file = Files_upload.objects.get(pk=pk)
    if request.user == file.user:
        form = RenameForm()
        if request.method == "POST":
            form = RenameForm(request.POST or None)
            if form.is_valid():
                file.name = form.cleaned_data['new_name']
                file.save()
                return redirect('dashboard')
        return render(request, 'product/rename_file.html', {'form': form, 'file': file})
    else:
        return redirect('dashboard')


@login_required
def edit_txt_file(request, node_id,filename,parent_id):
    user_name = request.session['usr']
    user_password = request.session['pwd']
    content = alfresco.getFileContent(node_id, user_name, user_password)
    context = {"content": content,'filename': filename,'node_id': node_id,'parent_id': parent_id}
    print("======= product->view->edit_txt_file =======")
    print(context)
    return render(request, 'product/edit_txt_file.html', context)

@login_required
def update_google_document(request, google_id,filename,parent_id):
    # user_name = request.session['usr']
    # user_password = request.session['pwd']
    # content = alfresco.getFileContent(node_id, user_name, user_password)
    context = {'filename': filename,'google_id': google_id,'parent_id': parent_id}
    print("======= product->view->update_google_document =======")
    print(context)
    return render(request, 'product/update-google-document.html', context)

@login_required
def close(request):
    pass

@login_required
def open(request, pk):
    file = get_object_or_404(Files_upload, pk=pk)
    if file.data_type == 'pdf':
        pages = convert_from_path(f'{file.up_file}')
        for page in pages:
            page.save('images/out.jpg', 'JPEG')
    elif file.data_type in ('jpeg', 'jpg', 'png'):
        images = file.up_file
    else:
        images = ''
    data = {'images': images}
    return JsonResponse(data)


@login_required
def add_favorite(request, pk):
    file = Files_upload.objects.get(pk=pk)
    if file.user == request.user and file.favorite == False:
        file.favorite = True
        file.save()
    else:
        file.favorite = False
        file.save()
    return redirect('dashboard')

@login_required
def favorite_list(request):
    files = alfresco.favorites_list(request.session['usr'],request.session['pwd'])
    files = Files_upload.objects.filter(user=request.user, favorite=True).all()
    return render(request, 'product/favorite_files.html', {'files': files})

@login_required
def project_multifile_view(request, project_name):
    rows = Project_file_List.objects.filter(user=request.user, project_name = project_name)
    project_file_list=[]
    for row in rows :
        project_file_list.append(row.file_name)
    html = render_to_string('layouts/project-multifile-view.html', {'project_file_list':project_file_list,'project_name':project_name})
    return HttpResponse(html)

@login_required
def project_name_check(request, project_name):
    username = request.session['usr']
    exist = Project_List.objects.filter(project_name = project_name, user_name = username)
    if not (exist.count()>0):
        request.session['project_name'] = project_name
        return HttpResponse(project_name)
    else:
        # return HttpResponse(project_name)
        return HttpResponse("existed")

@login_required
def project_list(request):
    username = request.session['usr']
    rows = Project_List.objects.filter(user_name = username)
    name_list=[]
    for row in rows :
        name_list.append(row.project_name)
    html = render_to_string('product/partial/project-list-modal.html', {'project_list':name_list})
    return HttpResponse(html)

@login_required
def upload_file_from_alfresco(request):
    print("=====upload_file_from_alfresco====")
    username = request.session['usr']
    nodes =[]
    if request.method == "POST":
        project_name = request.POST['project_name']
        print("----project_name : ", project_name)
        try:
            for node in request.POST.getlist('id_checks'):
                nodes.append(node)
        except:
            pass
        x = datetime.datetime.now()
        project = Project_List( project_name = project_name, user_name = username, date = x.strftime("%x"))
        project.save()
        files = request.FILES.getlist('upload1')
        files.extend( request.FILES.getlist('upload2'))
        for file in files:
            value_type = str(file).split('.')[-1]
            name = str(file).split('/')[-1]
            Files_upload(user=request.user, up_file=file, data_type=value_type, name=name)
            response = alfresco.createFile(request.session.get('folder', ''), str(file), file, request.session['usr'],request.session['pwd'])
            nodes.append(response['entry']['id'])

    user_name = request.session['usr']
    user_password = request.session['pwd']
    for node in nodes :
        try:
            response = alfresco.download_file(node, user_name, user_password)
            txt = response.headers['Content-Disposition']
            filename = txt[22:txt.find('; filename*')-1]
            filetype = filename.split('.')[-1]
            filepath = "users/{}/{}/{}".format( request.user, project_name, filename)
            path = default_storage.save(filepath, ContentFile(response.content))
            fileurl = default_storage.url(path)
            new_row =  Project_file_List(user= request.user, project_name= project_name, file_name = filename, file_type = filetype, file_path = path, alfresco_id = node, file_url = fileurl)
            new_row.save()
        except:
            pass
    request.session['dashboard'] = 'open_project'
    request.session['project_name'] = project_name
    try:
        input = "{}/users/{}/{}".format(settings.MEDIA_ROOT, request.user, project_name )
        output = "{}/users/{}/{}/pre_output".format(settings.MEDIA_ROOT, request.user, project_name )
        # command = 'cmd /c "java -jar Tools\\PDFtoText.jar {} {}"'.format(input, output)
        command = "java -jar Tools/PDFtoText.jar {} {}".format(input, output)
        print("command1 : ", command)
        # return_code = os.system(command)
        return_code = subprocess.call(command, shell=True)
        print("====== convert_pdf_to_text_result :", return_code)
        #python correctSpellHyphen.py -i "D:\Medical Project\TextProcess\TextFile" -o "D:\Medical Project\TextProcess\PreprocessFile"
        input = "{}/users/{}/{}/pre_output".format(settings.MEDIA_ROOT, request.user, project_name )
        output = "{}/users/{}/{}/preprocess".format(settings.MEDIA_ROOT, request.user, project_name )
        # command = 'cmd /c "python Tools\\correctSpellHyphen.py -i {} -o {}"'.format(input, output)
        command = "python Tools/correctSpellHyphen.py -i {} -o {}".format(input, output)
        print("command2 : ", command)
        return_code = subprocess.call(command, shell=True)
        # return_code = os.system(command)
        print("====== return_code2 :", return_code)
        #python preprocess.py -i "D:\Medical Project\TextProcess\TextFile" -o "D:\Medical Project\TextProcess\PreprocessFile"
        input = "{}/users/{}/{}/preprocess".format(settings.MEDIA_ROOT, request.user, project_name )
        output = "{}/users/{}/{}/txtOutput".format(settings.MEDIA_ROOT, request.user, project_name )
        # command = 'cmd /c "python Tools\\preprocess.py -i {} -o {}"'.format(input, output)
        command = "python Tools/preprocess.py -i {} -o {}".format(input, output)
        print("command3 : ", command)
        return_code = subprocess.call(command, shell=True)
        # return_code = os.system(command)
        print("====== return_code3 :", return_code)
    except Exception as e:
        print('Preprocess error:', str(e))
    return redirect('/dashboard')

@login_required
def preview_file(request, project, file):
    print("==========proview_file ==========", project, file)
    rows = Project_file_List.objects.filter(user = request.user, project_name = project, file_name = file)
    row = rows[0]
    url = ""
    type = row.file_type

    if ('pdf' in type) :
        url = row.file_url
    elif ('jpg' in type) or ('jpeg' in type) or ('png' in type) :
        url = row.file_url
    elif 'doc' in type :
        url = row.file_url
    else:
        url = row.file_url
    print("===== preview_file : ", url)
    print(url)
    return HttpResponse(url)

@login_required(login_url='/login/?next=dashboard')
def select_files_of_project(request, parent_id):
    user_name = request.session['usr']
    user_password = request.session['pwd']
    project_name = request.session['project_name']
    global main_table_data
    print("=========== product -> file_manager(request, parent_id) ===============")
    if parent_id:
        entries = alfresco.getFolderChild(parent_id, user_name, user_password)

    node_entry = alfresco.getNode(parent_id, user_name, user_password)
    if "parentId" not in node_entry:
        node_entry['parentId'] = "-root-"

    folder = alfresco.getUserHome(request, user_name, user_password)
    if folder['parentId'] == node_entry['id']:
        return HttpResponse(status=500)
    html = render_to_string('product/partial/select-files-of-project-modal.html', {'entries': entries, 'parent_id': node_entry['parentId'], 'folder_id': parent_id, 'project_name':project_name})
    return HttpResponse(html)
