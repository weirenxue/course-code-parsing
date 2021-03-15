$(function() {
    $('#classCode-1, #classCode-2').on('input', function(){
        let s = "";
        let trs = [];
        let course = [];
        let cursor
        course.push(parseCourseCode($('#classCode-1')[0].value));
        course.push(parseCourseCode($('#classCode-2')[0].value));
        for(let i = 0; i < defineCode.length; i++){
            let code1 = course[0][defineCode[i].name];
            let code2 = course[1][defineCode[i].name];
            let tr = $(document.createElement('tr'));
            let desc1 = getMeaning(defineCode[i].name, course[0]) || '?';
            let desc2 = getMeaning(defineCode[i].name, course[1]) || '?';
            
            tr.append($(document.createElement('td')).text("(" + defineCode[i].range + ") " + defineCode[i].name));
            tr.append($(document.createElement('td')).text(code1 ? code1 + "  (" + desc1 + ")" : ''));
            tr.append($(document.createElement('td')).text(code2 ? code2 + "  (" + desc2 + ")" : ''));

            let code1Len = $('#classCode-1')[0].value.length;
            let code2Len = $('#classCode-2')[0].value.length;
            if (code1 !== code2 && (code1Len != 0 && code2Len != 0)) {
                tr.addClass('bg-danger')
            }
            trs.push(tr);
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
    function getMeaning(cateName, parsedCourse){
        let desc;
        let code = parsedCourse[cateName];
        let normalCode = ['課程類型', '群別代碼', '科別代碼', '班群', '課程類別', '開課方式', '科目屬性', '領域名稱']
        if (normalCode.includes(cateName) && codeMap[cateName] !== undefined){
            desc = codeMap[cateName][code] ? codeMap[cateName][code] : null;
            if (cateName === '班群' && desc === null) {
                if (code == 0) {
                    desc = '不分班群'
                } else if (code.charCodeAt() >= 65 && code.charCodeAt() <= 90){
                    desc = '各校自定義班群'
                }
            }
        } else if (cateName === '科目名稱代碼') {
            let mapArray = codeMap[cateName][code];
            console.log(code,mapArray)
            if (mapArray === undefined){
                desc = null;
            } else {
                element = mapArray.find(x => 
                    x['課程類別'] === parsedCourse['課程類別'] && 
                    x['科目屬性'] === parsedCourse['科目屬性'] && 
                    x['領域名稱'] === parsedCourse['領域名稱']
                );
                if (element === undefined){
                    desc = null;
                } else {
                    desc = element['Desc'];
                }
            }
        } else if (cateName === '適用入學年度') {
            desc = code + '學年度入學學生適用';
        } else if (cateName === '校代碼') {
            desc = schoolMap[code];
        }
        return desc;
    }
    function parseCourseCode(CourseCode){
        let course = {};
        let cursor = 0;
        for(let i = 0; i < defineCode.length; i++){
            course[defineCode[i].name] = CourseCode.substr(cursor, defineCode[i].len);
            cursor += defineCode[i].len;
        }
        return course;
    }
});


