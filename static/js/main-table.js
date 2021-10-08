$(document).ready(function () {
    $(".dropdown-item").click(function( event ) {
        localStorage.setItem("parent_ID", $('#modal_folder_id').val());
    });
    path = window.location.pathname
    console.log("==============main table js loaded===============")
    if(path.includes('add_file')){
        localStorage.setItem('save_home', "true")
    }
    if(path.includes('add_url_file')){
        localStorage.setItem('save_home', "true")
    }
    $(document).on('click', '#upload-file-btn', function( event ) {
        console.log("**** upload-processing *****")
        $('.loading-upload-processing').css('display','block')
        // $('#select_files_of_project_modal').modal('hide')
        $( "#upload-file").submit();
    })
    setupMainTable()
    setupRating()
    setupTagging()
    setupFileManager()
    setCSRFToken()
    loadData()
});
function loadData(){
    if(localStorage.getItem("save_home") == 'true'){
        id = localStorage.getItem("parent_ID");
        localStorage.removeItem("parent_ID");
        $('.loading-main-table').show();
        $.ajax({
            type: "GET",
            url: "/dashboard/main-table/" + id,
            contentType: 'application/json;charset=utf-8',
            dataType: 'text',
            success : function(data) {
                $('#main-table').html(data)
                setupMainTable()
                refresh_bottom_panel(null)
                $('.loading-main-table').show()
            }, error: function(err){
                console.log(err)
                $('.loading-main-table').show()
            }
        });
    }else{
        $('.loading-main-table').hide()
    }
    localStorage.setItem('save_home', "false")
}
function setupPreview(){
    var id = $("#preview_link_id").val()
    console.log("============setting up preview===============", id)
    // var src = "http://localhost:8080/alfresco/api/-default-/public/alfresco/versions/1/shared-links/" + id + "/content?attachment=false"
    // var src = "http://35.178.166.45:8080/alfresco/api/-default-/public/alfresco/versions/1/shared-links/" + id + "/content?attachment=false"
    console.log("======src======", id)
    $(".iframe-preview").attr('src', id)
}
function setupTagging(){
    console.log("========set up tagging============")
    $('#btn-add-tag').on('click', function(){
        new_tag = $('#input-new-tag').val()
        console.log("========tagging============", new_tag)
        if(new_tag){
            ele = $('<div class="tag"></div>')
            ele.html(new_tag)
            $('#tag-box').append(ele)
            $('#input-new-tag').val('')
            node_id = $('#node_id').val()
            $.ajax({
                type: "GET",
                url: "/dashboard/post-tag/" + node_id + "/" + new_tag,
                contentType: 'application/json;charset=utf-8',
                dataType: 'text',
                success : function(data) {
                    console.log("tag created")
                }, error: function(err){
                    console.log(err)
                }
            });
        }else{
            return
        }
    })
}
function refresh_filemanager(parent_id){
    console.log(parent_id)
    $.ajax({
        type: "GET",
        url: "/dashboard/file-manager/" + parent_id,
        contentType: 'application/json;charset=utf-8',
        dataType: 'text',
        success : function(data) {
            $('#modal-wrapper').html(data)
            console.log("====success updating file manager ====", data)
            setupFileManager()
        }, error: function(err){
            console.log(err)
        }
    });
}
function create_folder(parent_id, name){
    $.ajax({
        type: "GET",
        url: "/dashboard/create-folder/" + parent_id + "/" + name,
        contentType: 'application/json;charset=utf-8',
        dataType: 'text',
        success : function(data) {
             console.log("====success creating folder====", data)
             refresh_main_table(parent_id)
             refresh_filemanager(parent_id)
         }, error: function(err){
             console.log(err)
         }
    });
}
function setupFileManager(){
    let selected_file_id = null
    refresh_bottom_panel(null)
    $('.filemanager-item').on('click', function(){
        $('.filemanager-item').removeClass('text-primary')
        $(this).addClass('text-primary')
        selected_file_id = $(this).data('id')
        console.log("========selected========", selected_file_id)
    })

    $('.filemanager-file-delete').on('click', function(){
        files = $('.f-manager-del-check')
        len = $('.f-manager-del-check').length
        list = []
        for(let i=0; i<len; i++){
            me = files.eq(i)
            if(me.prop('checked')){
                console.log("===============",me.parent().data('id'))
                list.push(me.parent().data('id'))
            }
            folder = $('#modal_folder_id').val()
            refresh_filemanager(folder)
        }
        $.ajax({
            type: "POST",
            url: "/dashboard/file-manager/delete-files/",
            data: JSON.stringify({"nodes": list}),
            contentType: 'application/json;charset=utf-8',
            dataType: 'text',
            success : function(data) {
                 console.log("====success open file ====", data)
             }, error: function(err){
                 console.log(err)
             }
        });
    })

    $('.item-folder').on('dblclick', function(e){
        $('.loading-preprocess').css('display','block')
        $('.loading_background').css('display','block')
        refresh_filemanager($(this).data('id'))
        // refresh_main_table($(this).data('id'))
    })
    function openFileInManager(id){
        $('#folderModal').modal('hide')
        $.ajax({
            type: "GET",
            url: "/dashboard/file-manager/open-file/" + id,
            contentType: 'application/json;charset=utf-8',
            dataType: 'text',
            success : function(data) {
                console.log("====success open file ====", data)
                // if (JSON.parse(data)['document type']=='text/plain')
                // {
                //     id = JSON.parse(data)['private_link_id']
                //     pid = JSON.parse(data)['parent_id']
                //     name = JSON.parse(data)['name']
                //     var src = "/dashboard/edit-txt-file/"+ id + "/" + name + "/" + pid
                //     console.log("============",src, "=============")
                //     window.location.href = src
                // }
                // else if (JSON.parse(data)['document type'].includes('spreadsheet') || JSON.parse(data)['document type'].includes('ms-excel'))
                // {
                //     id = JSON.parse(data)['private_link_id']
                //     pid = JSON.parse(data)['parent_id']
                //     name = JSON.parse(data)['name']
                //     google_id=JSON.parse(data)['google_id']
                //     var src = "/dashboard/update-google-document/"+ google_id + "/" + name + "/" + pid
                //     window.location.href = src
                //     console.log("============",src, "=============")
                //     var src = "https://docs.google.com/spreadsheets/d/" + google_id + "/edit"
                //     window.open(src)
                // }
                // else
                // {
                    id = JSON.parse(data)['link_id']
                    // var src = "http://localhost:8080/alfresco/api/-default-/public/alfresco/versions/1/shared-links/" + id + "/content?attachment=false"
                    // var src = "http://35.178.166.45:8080/alfresco/api/-default-/public/alfresco/versions/1/shared-links/" + id + "/content?attachment=false"
                    window.open(id)
                // }
            }, error: function(err){
                console.log(err)
            }
        });
    }
    $('.item-file').on('dblclick', function(e){
        var node_id = $(this).data('id');
        folder_id = $('#modal_folder_id').val()
        refresh_main_table(folder_id);
        openFileInManager(node_id)
    })

    $('.filemanager-up-arrow').on('click', function(){
        parent_id = $('#modal_parent_id').val()
        console.log("up-folder : ", parent_id)
        $('.loading-preprocess').css('display','block')
        $('.loading_background').css('display','block')
        refresh_filemanager(parent_id)
        // refresh_main_table(parent_id)
    })

    $('#open_folder_btn').on('click', function(){
        $('.project-multiview-content').hide()
        $('.loading-upload-and-preprocess').css('display','block')
        $('.content').show()
        if(selected_file_id){
            openFileInManager(selected_file_id)
        }else{
            folder_id = $('#modal_folder_id').val()
            localStorage.setItem('last_opened_folder',folder_id)
            refresh_main_table(folder_id);
        }

    })

    $('#btn_create_folder').on('click', function(){
        folder_id = $('#modal_folder_id').val()
        folder_name = $('#input_folder_name').val()
        if(folder_name && folder_id){
            create_folder(folder_id, folder_name)
        }
        else{
            alert('invalid input')
            return
        }
    })
}
function setupMainTable(){
    $(".main-table-item").on('click', function(){
        id = $(this).data('id')
        console.log("---main_table_item---", id)
        $(".loading-upload-and-preprocess").css('display','block')
        refresh_bottom_panel(id)
    })
    $(".close-file-menu").on('click', function(){
        refresh_main_table(null)
        localStorage.setItem('save_home','false')
    })
    $(".recent-open-folder").on('click', function(){
        id = localStorage.getItem('last_opened_folder')
        $(".loading-upload-and-preprocess").css('display','block')
        refresh_main_table(id)
        localStorage.setItem('save_home','true')
    })
}

function postRating(rating){
    node_id = $('#node_id').val()
    $.ajax({
        type: "GET",
        url: "/dashboard/post-rating/" + node_id + "/" + rating,
        contentType: 'application/json;charset=utf-8',
        dataType: 'text',
        success : function(data) {
            console.log("====success rating====", data)
            $(".loading-upload-and-preprocess").css('display','none')
        }, error: function(err){
            console.log(err)
            $(".loading-upload-and-preprocess").css('display','none')
        }
    });
}

function postFavorites(favo){
    node_id = $('#node_id').val()
    console.log("====== postFavorites==========", favo, node_id)
    $.ajax({
        type: "GET",
        url: "/dashboard/post-favorites/" + node_id + "/" + favo,
        contentType: 'application/json;charset=utf-8',
        dataType: 'text',
        success : function(data) {
            console.log("====success rating====", data)
            $(".loading-upload-and-preprocess").css('display','none')
        }, error: function(err){
            console.log(err)
            $(".loading-upload-and-preprocess").css('display','none')
        }
    });
}

function setupRating(){
        console.log("===========set up rating===================")
        children = $(".star-rating").children('span')
        myRating = parseInt($("#my_rating").val())
        for (var i = 0; i < children.length; i++) {
            children.eq(i).removeClass()
            if(i <= myRating){
                children.eq(i).addClass("fa fa-star")
            }else{
                children.eq(i).addClass("fa fa-star-o")
            }

            children.eq(i).on('click', function(){
                rate = parseInt($(this).data('rating'))
                postRating(rate)
                console.log("=======rate=====", rate)
                for (var j = 0; j < children.length; j++) {
                    var currentChild = children.eq(j);
                    child = currentChild
                    index = parseInt(child.data('rating'))
                    console.log("=========index===========", index)
                    child.removeClass()
                    if (index <= rate){
                        child.addClass("fa fa-star")
                    }else{
                        child.addClass("fa fa-star-o")
                    }
                }
            })

        }

        $('.like-bt').on('click', function(){
            console.log("===========setupLike============")
            $(".loading-upload-and-preprocess").css('display','block')
            $(this).removeClass('like-bt-empty')
            $(this).removeClass('like-bt-full')
            if ($(this).data('status') == "empty"){
                $(this).addClass('like-bt-full')
                $(this).data('status','full')
                $(this).css("color", "blue");
                postRating(100)
            }else{
                $(this).addClass('like-bt-empty')
                $(this).data('status','empty')
                $(this).css("color", "black");
                postRating(200)
            }
        })

        $('.favorites-bt').on('click', function(){
            console.log("===========setupFavorites============")
            $(this).removeClass('favorites-bt-empty')
            $(this).removeClass('favorites-bt-full')
            $(".loading-upload-and-preprocess").css('display','block')
            if ($(this).data('status') == "empty"){
                $(this).addClass('favorites-bt-full')
                $(this).data('status','full')
                $(this).css("color", "orange");
                postFavorites(1);
            }else{
                $(this).addClass('favorites-bt-empty')
                $(this).data('status','empty')
                $(this).css("color", "black");
                postFavorites(0);
            }
        })
}
function refresh_bottom_panel(id)  {
    if (id==null){
        $('#bottom-panel').html('')
        $(".iframe-preview").attr('src', '')
        return
    }
    $.ajax({
        type: "GET",
        url: "/dashboard/bottom-panel/" + id,
        contentType: 'application/json;charset=utf-8',
        dataType: 'text',
        success : function(data) {
            $('#bottom-panel').html(data)
            setupPreview()
            setupRating()
            setupTagging()
            $(".loading-upload-and-preprocess").css('display','none')
            console.log("---main_table_item---", id)
        }, error: function(err){
            console.log(err)
            $('#bottom-panel').html('')
            $(".iframe-preview").attr('src', '')
        }
    });
}

function refresh_main_table(id)  {
    if(id==null){
        $('#main-table').html('')
         setupMainTable()
         refresh_bottom_panel(null)
    }else{
        $('.loading-main-table').show()
        $.ajax({
            type: "GET",
            url: "/dashboard/main-table/" + id,
            contentType: 'application/json;charset=utf-8',
            dataType: 'text',
            success : function(data) {
                $('#main-table').html(data)
                setupMainTable()
                refresh_bottom_panel(null)
                $('.loading-main-table').hide()
                $('.loading-upload-and-preprocess').css('display','none')
             }, error: function(err){
                console.log(err)
                $('.loading-main-table').hide()
             }
        });
    }


}

function setCSRFToken() {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
   });
}

