$(function(){
    $("*[name=join]").on('click', function() {
        obj = $(this);
        join_val = false
        if(obj.prop('checked')){
            join_val = true;
        }
        var data = {
            content_id : $('#content_id').val(),
            user_id : obj.val(),
            join : join_val
        };

        // 通信実行
        $.ajax({
            type:"post",                // method = "POST"
            url:"http://127.0.0.1:5002/update/",        // POST送信先のURL
            data:JSON.stringify(data),  // JSONデータ本体
            contentType: 'application/json', // リクエストの Content-Type
            dataType: "text",           // レスポンスをJSONとしてパースする
            success: function(json_data) {   // 200 OK時
                // JSON Arrayの先頭が成功フラグ、失敗の場合2番目がエラーメッセージ
                if (json_data != 'ok') {
                    $('#msg').html(json_data);
                }
            },
            error: function() {         // HTTPエラー時
                $('#msg').html("サーバーエラー");
            },
        });
        
    });
})