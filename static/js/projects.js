$(document).ready(function () {
    $("#create_new_project").click(function( event ) {
        name = $('#project_name').val();
        if (name=="" || name=="Enter Project Name"){
            return
        }
        $.ajax({
            type: "GET",
            url: "/dashboard/project-name-check/" + name,
            contentType: 'application/json;charset=utf-8',
            dataType: 'text',
            success : function(data) {
                console.log("create_project_name:",data)
                if (data == "existed"){
                    // $("#new_project_model").modal('show')
                    $('.toast').toast({animation: false, delay: 3000});
                    $('.toast').toast('show');
                }
                else
                {
                    $("#new_project_model").modal('hide')
                    $('#created_project_name').val(data)
                    $('#select_files_of_project_modal').modal('show')
                }
            }, error: function(err){
                console.log(err)
                $('.loading-main-table').show()
            }
        });

    });
    $(".open-project-button").click(function( event ) {
        $.ajax({
            type: "GET",
            url: "/dashboard/project-list",
            contentType: 'application/json;charset=utf-8',
            dataType: 'text',
            success : function(data) {
                $('.project_list').html(data)
                $('#project_list_modal').modal('show')
            }, error: function(err){
                console.log(err)
                $('.loading-main-table').show()
            }
        });
    });
    $(document).on('click', '.custom-item-li', function( event ) {
        file = $(this).data('file')
        project = $(this).data('project')
        console.log("-----custom-item-li clicked------", "/dashboard/preview-file/"+ project + "/" + file)
        $.ajax({
            type: "GET",
            url: "/dashboard/preview-file/"+ project + "/" + file,
            contentType: 'application/json;charset=utf-8',
            dataType: 'text',
            success : function(data) {
                $(".iframe-preview").attr('src', data)
            }, error: function(err){
                console.log(err)
                $('.loading-main-table').show()
            }
        });
    })
    $(document).on('click', '#select-file-form-submit', function( event ) {
        console.log("**** select-file-form-submit *****")
        $('.loading-upload-and-preprocess').css('display','block')
        $('#select_files_of_project_modal').modal('hide')
        $( "#select-files-of-project-form" ).submit();
        console.log("--submit----")
    })
    setupProjectFilemodal()
});

function selected_project(project_name){
    $.ajax({
        type: "GET",
        url : "http://localhost:8000/dashboard/project-multifile-view/" + project_name,
        url : "http://3.10.217.151:8000/dashboard/project-multifile-view/" + project_name,
        contentType: 'application/json;charset=utf-8',
        dataType: 'text',
        success : function(data) {
            $('#project_list_modal').modal('hide')
            $('.project-multiview-content').html(data)
            $('.project-multiview-content').show()
            $('.content').hide()
        }, error: function(err){
            console.log(err)
        }
    });
}
function setupProjectFilemodal(){
    $("#select_files_of_project").click(function( event ) {
        console.log("-------clicked create-project-buttuon------")
        $('.loading-main-table').show()
        var nodes = [];
        $.each($("input[class='select_file_project_check']:checked"), function(){
            nodes.push($(this).data('nid'));
        });
        nodearray=nodes.join("'.'")
        created_project_name = $('#created_project_name').text()

        $('#select_files_of_project_modal').modal('hide')
        if (nodearray != "") {
            $.ajax({
                type: "GET",
                url: "/dashboard/download-file-from-alfresco/" + nodearray + "/" + created_project_name,
                contentType: 'application/json;charset=utf-8',
                dataType: 'text',
                success : function(data) {
                    console.log("====success downloads ====")
                    $.ajax({
                        type: "GET",
                        url : "http://localhost:8000/dashboard/project-multifile-view/" + created_project_name,
                        url : "http://3.10.217.151:8000/dashboard/project-multifile-view/" + created_project_name,
                        contentType: 'application/json;charset=utf-8',
                        dataType: 'text',
                        success : function(data) {
                            $('.project-multiview-content').html(data)
                            $('.project-multiview-content').show()
                            $('.content').hide()
                        }, error: function(err){
                            console.log(err)
                        }
                    });
                    $('.loading-main-table').hide()
                }, error: function(err){
                    console.log("----download error :", err)
                    $('.loading-main-table').hide()
                }
            });
        }
    });
    $('.select-files-project-up-arrow').on('click', function(){
        parent_id = $('#project_file_modal_parent_id').val()
        refresh_project_file_manager(parent_id)
    })
    $('.folder-item-of-project').on('dblclick', function(e){
        refresh_project_file_manager($(this).data('id'))
    })
}
function refresh_project_file_manager(parent_id){
    console.log(parent_id)
    $.ajax({
        type: "GET",
        url: "/dashboard/select-files-of-project/" + parent_id,
        contentType: 'application/json;charset=utf-8',
        dataType: 'text',
        success : function(data) {
            $('.select-files-of-project-wraper').html(data)
            setupProjectFilemodal()
        }, error: function(err){
            console.log(err)
        }
    });
}
