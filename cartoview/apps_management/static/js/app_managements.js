$(document).ready(function () {
    $(".handler a").click(function () {
        var element = $(this);
        if ($(this).text() == "Install" || $(this).text() == "Update") {
            if (element.attr('disabled') == 'disabled') {

            }
            else {
                $.ajax({
                    type: "get",
                    url: "/apps_management/handle_install/" + element.attr("data-value"),
                    dataType: "json",
                    success: function (data) {
                        if (data.status == 1) {
                            bootbox.alert({
                                message: "<h3>Server message</h3><br><h5>" + data.message + "</h5>"
                            });
                        }
                        else if (data.status == 0) {
                            bootbox.confirm({
                                title: "<h3>Server Message</h3>",
                                message: "<i class=\"fa fa-question-circle\" aria-hidden=\"true\"></i> <b>" + data.message + "</b>",
                                buttons: {
                                    cancel: {
                                        label: '<i class="fa fa-times"></i> Cancel'
                                    },
                                    confirm: {
                                        label: '<i class="fa fa-check"></i> Confirm'
                                    }
                                },
                                callback: function (result) {
                                    if (result == true) {
                                        $.ajax({
                                            type: "GET",
                                            url: "/apps_management/confirm_installation/" + element.attr("data-value"),
                                            success: function (data) {
                                                if (data.status == "success") {
                                                    var dialog = bootbox.dialog({
                                                        message: '<p class="text-center">' + data.message + '</p>',
                                                        closeButton: false
                                                    });
                                                    setTimeout(function () {
                                                        dialog.modal('hide')
                                                    }, 3000);
                                                    element.text("Uninstall");
                                                    element.addClass('btn-danger').removeClass('btn-primary');
                                                }
                                                else if (data.status == "Msuccess") {
                                                    var dialog = bootbox.dialog({
                                                        message: '<p class="text-center">' + data.message + '</p>',
                                                        closeButton: false
                                                    });
                                                    setTimeout(function () {
                                                        dialog.modal('hide')
                                                    }, 3000);
                                                    element.text("Uninstall");
                                                    element.addClass('btn-danger').removeClass('btn-primary');
                                                    for (var i = 0; i < data.dep.length; i++) {
                                                        var el = $(".handler").find("[data-value='" + data.dep[i] + "']");
                                                        el.text("Uninstall");
                                                        el.addClass('btn-danger').removeClass('btn-primary');
                                                    }
                                                }
                                                else {
                                                    var dialog = bootbox.dialog({
                                                        message: '<p class="text-center" style="color: rgba(242,19,0,0.8);">' + data.message + '</p>',
                                                        closeButton: false
                                                    });
                                                    setTimeout(function () {
                                                        dialog.modal('hide')
                                                    }, 3000);
                                                }

                                            },
                                            error: function (xhr) {
                                                bootbox.alert({
                                                    message: 'Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText
                                                });

                                            }
                                        });
                                    }
                                }
                            });
                        }
                        else if (data.status == "error") {
                            $(".container").prepend("<div class=\"alert alert-danger alert-dismissable\">" + "<a href=\"#\" class=\"close\" data-dismiss=\"alert\" aria-label=\"close\">×</a><strong>" + data.message + "</strong>" + "</div>");
                        }
                        else {
                            $(".container").prepend("<div class=\"alert alert-info alert-dismissable\">" + "<a href=\"#\" class=\"close\" data-dismiss=\"alert\" aria-label=\"close\">×</a><strong>" + data.message + "</strong>" + "</div>");

                        }
                    },
                    error: function (xhr) {
                        alert('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText);
                    }
                });
            }

        }
        else if ($(this).text() == "Uninstall") {
            $.ajax({
                type: "get",
                url: "/apps_management/handle_uninstall/" + element.attr("data-value"),
                dataType: "json",
                success: function (data) {
                    var dialog = bootbox.dialog({
                        message: '<p class="text-center">' + data.message + '</p>',
                        closeButton: false
                    });
                    setTimeout(function () {
                        dialog.modal('hide')
                    }, 3000);
                    element.text("Install");
                    element.addClass('btn-primary').removeClass('btn-danger');
                },
                error: function (xhr) {
                    alert('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText);
                }
            });
        }
        return false
    })

});
