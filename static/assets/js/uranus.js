/**
 * Created by hui on 17-7-1.
 */
//获取页面input标签的name和value
// function getInputData() {
//     var data = {};
//     var inputList = $('.content input');
//     for (var i = 0; i < inputList.length; i++) {
//         var input = inputList.get(i);
//
//         var inputValue = $(input).val() || "";
//         if (inputValue === "") {
//             return false;
//         }
//         data[$(input).attr('name')] = inputValue;
//     }
//     return data;
//
//
//
// }

function getInputData() {
    var formData = new FormData();
    var inputList = $('.content input');
    for (var i = 0; i < inputList.length; i++) {
        var input = inputList.get(i);
        if ($(input).attr('type') === 'file') {
            if(!input.files[0]){
                return false;
            }
            formData.append($(input).attr('name'), input.files[0])
        } else {
            var inputValue = $(input).val() || "";
            if (inputValue === "") {
                return false;
            }
            // alert($(input).attr('name') + ':' + inputValue);
            formData.append($(input).attr('name'), inputValue);
        }
    }
    return formData;
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


function getFormData(inputData, selectData) {
    var formData = inputData;
    for(var key in selectData){
        formData.append(key, selectData[key]);
    }
    return formData;
}
//整合input与select的数据
// function getPostData(inputData, selectData) {
//     var postData = {};
//     for (var key in inputData) {
//         postData[key] = inputData[key];
//     }
//     for (key in selectData) {
//         postData[key] = selectData[key];
//     }
//     return postData;
//
// }
//点击触发ajax
function submitClickWithoutFile(postUrl, modalShowText) {
    var inputData = getInputData();
    if (!inputData) {
        $('.modal-body').text('数据不完整，请重新填写！');
        $('#myModal').modal('show');
        return;
    }
    var selectData = getSelectData();
    var postData = getPostData(inputData, selectData);
    $.ajax(postUrl, {
        method: 'post',
        data: postData,
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

function submitClickWithFile(postUrl, modalShowText) {
    var inputData = getInputData();
    var selectData = getSelectData();
    if (!inputData) {
        $('.modal-body').text('数据不完整，请重新填写！');
        $('#myModal').modal('show');
        return;
    }
    var postData = getFormData(inputData,selectData);

    $.ajax(postUrl,
        {
            type: 'POST',
            cache: false,
            data: postData,
            processData: false,
            contentType: false,
            success: function (data) {
                data = $.parseJSON(data);
                var success_info = data['success'] || "";
                var error_message = data['error_message'] || "";
                debugger;
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

function submitClick(postUrl, modalShowText) {
    if($('input[type=file]')){
        submitClickWithFile(postUrl, modalShowText);
    }else{
        submitClickWithoutFile(postUrl, modalShowText);
    }
}

