/**
 * Created by hui on 17-7-1.
 */
//获取页面input标签的name和value
function getInputData() {
    var data = {};
    var inputList = $('.content input');
    for (var i = 0; i < inputList.length; i++) {
        var input = inputList.get(i);
        var inputValue = $(input).val() || "";
        if(inputValue == ""){
            return false;
        }
        data[$(input).attr('name')] = inputValue;
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
        if(selectValue == ""){
            return false;
        }
        data[$(select).attr('name')] = selectValue;
    }
    return data;
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
// }

function getPostData() {
    var inputData = getInputData();
    if(!inputData){
        $('.modal-body').text('数据不完整，请重新填写！');
        $('#myModal').modal('show');
    }
    var selectData = getSelectData();
    //如果页面没有select，则selectData为空，如果有select，则会有默认值，
    //所以不需要也不应该判断selectData
    // if(!selectData){
    //     $('.modal-body').text('数据不完整，请重新填写！');
    //     $('#myModal').modal('show');
    // }
    var postData = {};
    for (var key in inputData) {
        postData[key] = inputData[key];
    }
    for (key in selectData) {
        postData[key] = selectData[key];
    }
    return postData;

}
//点击触发ajax
function submitClick(postUrl, modalShowText, forwardUrl) {
    var postData = getPostData();
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
                    window.location = forwardUrl;
                });
            } else {
                $('.modal-body').text(error_message);
                $('#myModal').modal('show');
            }
        }
    });
}