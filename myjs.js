$(function() {
    $('#classCode-1, #classCode-2').on('input', function(){
        let s = "";
        let cursor = 0;
        let trs = [];
        for(let i = 0; i < defineCode.length; i++){
            if (i != 0){
                s += "\n"
            }
            let code1Len = $('#classCode-1')[0].value.length;
            let code2Len = $('#classCode-2')[0].value.length;

            let code1 = $('#classCode-1')[0].value.substr(cursor, defineCode[i].len);
            let code2 = $('#classCode-2')[0].value.substr(cursor, defineCode[i].len);
            let tr = $(document.createElement('tr'));
            tr.append($(document.createElement('td')).text(defineCode[i].name + "(" + defineCode[i].len + ")"));
            tr.append($(document.createElement('td')).text(code1));
            tr.append($(document.createElement('td')).text(code2));
            if (code1 !== code2 && (code1Len != 0 && code2Len != 0)) {
                tr.addClass('bg-danger')
            }
            trs.push(tr);
            s += defineCode[i].name + " : " + this.value.substr(cursor, defineCode[i].len);
            cursor += defineCode[i].len
        }
        $('tbody', '#ovTable').empty().append(trs);
    });
    $('#classCode-1, #classCode-2').on('input', function(){
        if(this.value.length == 23) {
            $('.alertMsg', $(this).parent()).addClass('d-none');
        } else {
            $('.alertMsg', $(this).parent()).removeClass('d-none');
        }
    });
});


