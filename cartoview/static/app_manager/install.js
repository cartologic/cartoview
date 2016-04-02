$("#btn-install-app").click(function(event) {
	event.preventDefault();
	$('#ct-install-result').empty().append(msg_div('Installing application, Please wait!','info loading'));
	var formData = new FormData($('#form-install-app')[0]);
	//data = {name:'test_install'};
     var pleaseWaitDiv = $('<div class="modal" id="pleaseWaitDialog" data-backdrop="static" data-keyboard="false"><div class="modal-body" style="margin: 20% 50%;"><img src="'+ loading_gif_src+'"/></div></div>');
    pleaseWaitDiv.modal();
	$.ajax({
        type: 'POST',
        //contentType: 'application/json',
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
		url: ajax_install_app_url,
        success: function(res, status, jqXHR) {
        	if(res.success){
                $.each(res.log, function(index, log) {
                     msg_div(log,'info','#ct-install-result');
                });
                $.each(res.warnings, function(index, warning) {
                     msg_div(warning,'warning','#ct-install-result');
                });
                $('#btn-show-install').show();
                $('#ct-install').hide();
                msg_div('Restarting the server, Please wait!','info loading', '#ct-install-result');
                window.setTimeout(function(){get_installed_app_info(res.app_name);}, 5000);
            }
            else{
                $('#ct-install-result').empty()
                $.each(res.errors, function(index, err) {
                     msg_div(err,'danger','#ct-install-result');
                });
                pleaseWaitDiv.hide();
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            $('#ct-install-result').empty()
            msg_div(jqXHR.responseJSON.error_message,'danger','#ct-install-result');
            msg_div(jqXHR.responseJSON.traceback,'danger','#ct-install-result');
            pleaseWaitDiv.hide();
        },
        xhr: function() {  // Custom XMLHttpRequest
            var myXhr = $.ajaxSettings.xhr();
            if(myXhr.upload){ // Check if upload property exists
                myXhr.upload.addEventListener('progress',progressHandlingFunction, false); // For handling the progress of the upload
            }
            return myXhr;
        }
    }); // end $.ajax()
});
function get_installed_app_info(app_name){
    $.ajax({
        dataType: "json",
        url: home_url + "apps/rest/app_manager/app/",
        data:{
            name:app_name,
            format: 'json'
        },
        success:function(res){
        	location.reload(true);
            if(res.error){
                msg_div('************* cannot get app info **********','error','#ct-install-result');
                msg_div(res.error,'error','#ct-install-result');
            }
            else{
                msg_div('App installation success!','success','#ct-install-result');
                var tr =$("<tr>")
                tr.appendTo('#table-apps').setTemplateElement("app-row-template").processTemplate(res.objects[0]);
                var a = $('.btn-uninstall-app',tr);
                a.attr('href', a.attr('href').replace('APP_NAME',res.objects[0].name)).click(uninstall_app);
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            setTimeout(function(){
                get_installed_app_info(app_name);
            },1000);
        }
    });
}
$('#btn-show-install').click(function(event) {
    $('#btn-show-install').hide()
    $('#ct-install').show()
});
$('#btn-hide-install').click(function(event) {
    $('#btn-show-install').show()
    $('#ct-install').hide()
});
function uninstall_app(event) {
    var row = $(this).parents('tr');
    event.preventDefault();
    if(confirm('Uninstall this app? This action cannot be reversed.')){
        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: $(this).attr('href'),
            processData: false,
            success: function(res, status, jqXHR) {
                if(res.success){
                    $('#ct-install-result').empty().append(msg_div('Uninstallation success!','success'));
                    row.remove()
                }
                else{
                    $('#ct-install-result').empty()
                    $.each(res.errors, function(index, err) {
                         msg_div(err,'danger','#ct-install-result');
                    });
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log(jqXHR);
                msg_div(jqXHR,'danger','#ct-install-result');

            }
        }); // end $.ajax()
    }
}
$(".btn-uninstall-app").click(uninstall_app);

function progressHandlingFunction(e){
    if(e.lengthComputable){
        $('progress').attr({value:e.loaded,max:e.total});
    }
}
$('#file-app').change(function(){
    var file = this.files[0];
    var name = file.name;
    var size = file.size;
    var type = file.type;
    //Your validation
});
function msg_div(msg,cls,ct){
    var html = '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + msg;
    var ct_msg = $('<div>').addClass('alert alert-dismissable alert-' + cls).html(html);
    if(ct) ct_msg.appendTo(ct)
    return ct_msg;
}
//===========================================================================================================================
     $(".up").click(function(e) {
        var current = $('#app_'+$(e.target).data('app_id')+'_row');
        var prev =  current.prev();
         $.ajax({
         url:app_manager_base_url+'moveup/'+$(e.target).data('app_id'),
         success:function(res){
             prev.before(current);
         }

         });
      });

      $(".down").click(function(e) {
        var current = $('#app_'+$(e.target).data('app_id')+'_row');
        var next = current.next();
        var currentId = current.attr('id');
        $.ajax({
         url:app_manager_base_url+ 'movedown/'+$(e.target).data('app_id'),
         success:function(res){
            next.after(current);
         }

         });

      });


      $(".app_state").click(function(e) {
        var current = $('#app_'+$(e.target).data('app_id')+'_row');
        var state_button = $(this);
        if (state_button.hasClass('deactivate'))
         {
         $.ajax({
         url:app_manager_base_url+'deactivate/'+$(e.target).data('app_id')+'/',
         success:function(res){
             state_button.addClass('activate').removeClass('deactivate');
             state_button.addClass('btn-info').removeClass('btn-warning');

             state_button.text('Resume')
         }

         });
         }
         else if (state_button.hasClass('activate'))
         {
          $.ajax({
         url:app_manager_base_url+'activate/'+$(e.target).data('app_id')+'/',
         success:function(res){
             state_button.addClass('deactivate').removeClass('activate');
             state_button.addClass('btn-warning').removeClass('btn-info');
             state_button.text('Deactivate')
         }

         });
         }
      });
//===================================================









  var menu_apps = document.getElementById("menu_apps");

var non_menu_apps = document.getElementById("non_menu_apps");

new Sortable(menu_apps, {
				group: "apps",
			});


new Sortable(non_menu_apps, {
    group: "apps",	});
var menu_apps = [];
var non_menu_apps = [];


 $("#order").click(function (e) {
     $(this).css('display', 'none');
            $('#loading_image').show();

    $('#menu_apps').children().each(function() {
      var $this = $(this);
      var item = { id: $this.data('id'), name: $this.data('name') };

      menu_apps.push(item);
    });

    $('#non_menu_apps').children().each(function() {
      var $this = $(this);
      var item = { id: $this.data('id'), name: $this.data('name') };

      non_menu_apps.push(item);
    });
    var apps = {menu_apps : menu_apps , non_menu_apps:non_menu_apps}
    apps_json = JSON.stringify (apps);
    $.ajax({
            type: "POST",
            url: save_app_orders_url,
            data: {'apps':apps_json  ,  'csrfmiddlewaretoken':csrf_token },
            dataType: "json",
            success: function(response) {location.reload();},
            error: function(rs, e) {

            }
        });

  });
//==============================================================================================================================


