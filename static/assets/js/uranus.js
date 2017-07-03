/**
 * Created by hui on 17-7-1.
 */

function getInputData() {
    var formData = new FormData();
    var inputList = $('.content input');
    for (var i = 0; i < inputList.length; i++) {
        var input = inputList.get(i);
        if ($(input).attr('type') === 'file') {
            if ($(input).is(':required') && !input.files[0]) {
                return false;
            }
            formData.append($(input).attr('name'), input.files[0])
        } else {
            var inputValue = $(input).val() || "";
            if ($(input).is(':required') && inputValue === "") {
                // alert($(input).attr('name') + ':' + inputValue);
                return false;
            }
            // alert($(input).attr('name') + ':' + inputValue);
            formData.append($(input).attr('name'), inputValue);
        }
    }
    // for(var v of formData.values()){
    //         alert(v);
    // }
    return formData;
}

//获取页面textarea标签数据
function getTextareaData() {
    var data = {};
    var textList = $('.content textarea');
    for (var i = 0; i < textList.length; i++) {
        var text = textList.get(i);
        var textValue = $(text).val() || "";
        if ($(text).is(':required') && textValue === "") {
            // alert($(text).attr('name'));
            return false;
        }
        // alert($(text).attr('name') + ':' + textValue);
        data[$(text).attr('name')] = textValue;
    }

    return data;
}
//获取页面select标签的name和value
function getSelectData() {
    var data = {};
    var selectList = $('.content select');
    for (var i = 0; i < selectList.length; i++) {
        var select = selectList.get(i);
        var selectValue = $(select).val() || "";
        if (selectValue === "") {
            return false;
        }
        data[$(select).attr('name')] = selectValue;
    }
    return data;
}


function getFormData(inputData, selectData, textData) {
    var formData = inputData;
    for (var key in selectData) {
        formData.append(key, selectData[key]);
    }
    // var textData = getTextareaData();
    for (var key in textData) {
        formData.append(key, textData[key]);
    }
    // for(var v of formData.values()){
    //     alert(v);
    // }
    return formData;
}

//点击触发ajax
function submitClick(postUrl, modalShowText) {
    var inputData = getInputData();
    var selectData = getSelectData();
    if (!inputData) {
        $('.modal-body').text('数据不完整，请重新填写！');
        $('#myModal').modal('show');
        return;
    }
    var textData = getTextareaData();
    if ($('.content textarea') && !textData) {
        $('.modal-body').text('数据不完整，请重新填写！');
        $('#myModal').modal('show');
        return;
    }
    var postData = getFormData(inputData, selectData, textData);

    $.ajax(
        {
            url: postUrl,
            type: 'POST',
            cache: false,
            data: postData,
            processData: false,
            contentType: false,
            success: function (data) {
                data = $.parseJSON(data);
                var success_info = data['success'] || "";
                var error_message = data['error_message'] || "";
                if (success_info) {
                    $('.modal-body').text(modalShowText);
                    $('#myModal').modal('show');
                    $('#confirm-btn').click(function () {
                        window.location = data['forward_url'];
                    });
                } else {
                    $('.modal-body').text(error_message);
                    $('#myModal').modal('show');
                }

            }
        });
}

//删除提示
function onDeleteMessage(deleteUrl) {
    var handleDeleteUrl = deleteUrl;
    // alert('url:' + handleDeleteUrl);
    $('#confirm-btn').click(function () {
        $.ajax({
            url: handleDeleteUrl,
            type: 'GET',
            data: {},
            success: function (data) {
                data = $.parseJSON(data);
                if (data['success']) {
                    $('.modal-body').text('删除成功！');
                    $('#confirm-btn').css('display', 'none');
                    $('#confirm-not-btn').text('确定');
                    $('#myModal').modal('show');
                    $('#confirm-not-btn').click(function () {
                        window.location.reload();
                    });
                }
            }
        });
    });

    $('#myModalLabel').text('删除');
    $('.modal-body').text('确认删除？');
    $('#confirm-btn').text('是');
    $('#confirm-not-btn').css('display', '');
    $('#confirm-not-btn').text('否');
    $('#myModal').modal('show');

    return false;
}
