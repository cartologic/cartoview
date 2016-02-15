/**
 * Created by kamal on 2/7/2016.
 */
$(function(){
    var current_maps_list = null;
    var selected_web_map_id = $('#id_app_instance_form-web_map_id').val();
    var numItemsPerPage = 6;
    function load_web_maps(page) {
        $('#loading_img').show();
        $('#maps-select').addClass("hide");
        $.ajax({
            url: MAP_LIST_REST_URL,
            cache: false,
            data: {
                limit: numItemsPerPage ,
                offset: numItemsPerPage * (page - 1)
            },
            success: function (maps_list) {
                $("#maps-from").text(maps_list.meta.offset + 1);
                $("#maps-to").text(maps_list.objects.length + maps_list.meta.offset);
                $("#maps-count").text(maps_list.meta.total_count);
                var numOfPages = Math.ceil(maps_list.meta.total_count / numItemsPerPage);
                $('#page-selection').bootpag({total: numOfPages, maxVisible: 5});
                current_maps_list = {};
                $('#maps-select').empty().removeClass("hide");
                $.each(maps_list.objects, function (i, map) {
                    var item = $('<option>')
                            .attr("data-img-src",map.thumbnail_url )
                            .attr("value",map.id)
                            .text(map.title);
                    current_maps_list[item.attr("value")] = map;
                    $('#maps-select').append(item);
                });
                var mapSelected = function(){

                  var selectedMap = current_maps_list[$("#maps-select").val()];
                    $('#id_app_instance-abstract').val(selectedMap.abstract);
                    $('#id_app_instance-title').val(selectedMap.title);
                    if(window.mapSelected){
                        window.mapSelected(selectedMap);
                    }
                };

                $("#maps-select").imagepicker({
                    hide_select: true,
                    show_label: true,
                    initialized:mapSelected,
                    selected:mapSelected
                });
                $(".image_picker_selector li").addClass("col-lg-4 col-md-6 col-xs-12");
                $('#loading_img').hide();
            }
        });
    }

    if(!IS_EDIT) {
        load_web_maps(1);

        if (selected_web_map_id) {
            $.ajax({
                url: "{% url 'arcportal_home' %}sharing/rest/content/items/" + selected_web_map_id,
                cache: false,
                success: function (web_map) {
                    $('#selected-map-img').attr("src", web_map.thumbnail);
                    $('#selected-map-label').text(web_map.title);
                }
            });
        }

        $('#page-selection').bootpag({
            total: 1 // TODO remove this hard coded number and use the number returned from the rest
        }).on("page", function (event, /* page number here */ num) {
            load_web_maps(num)
        });
    }
    //$("a[href='#tab_configuration']").on('shown.bs.tab', function (e) {
    //    $('#id_app_instance_form-config').next('.CodeMirror').get(0).CodeMirror.refresh()
    //});

});