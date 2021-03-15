defineCode = [
    {
        "name": "適用入學年度",
        "len": 3
    },
    {
        "name": "校代碼",
        "len": 6
    },
    {
        "name": "課程類型",
        "len": 1
    },
    {
        "name": "群別代碼",
        "len": 2
    },
    {
        "name": "科別代碼",
        "len": 3
    },
    {
        "name": "班群",
        "len": 1
    },
    {
        "name": "課程類別",
        "len": 1
    },
    {
        "name": "開課方式",
        "len": 1
    },
    {
        "name": "科目屬性",
        "len": 1
    },
    {
        "name": "領域名稱",
        "len": 2
    },
    {
        "name": "科目名稱代碼",
        "len": 2
    }
]

function codeRange() {
    let cursor = 1;
    for(let i = 0; i < defineCode.length; i++){
        defineCode[i].range = defineCode[i].len == 1 ? `${cursor}`  : `${cursor}-${cursor + defineCode[i].len-1}`;
        cursor += defineCode[i].len;
    }
}
codeRange();

schoolMap = {};
codeMap = {};

$.ajax({
    url : './schoolCodeMap.json',
    cache : false, 
    async : false,
    type : "GET",
    dataType : 'json',
    success : function (result) {
        console.log(result)
        schoolMap = result;
    }
});

$.ajax({
    url : './codeMap.json',
    cache : false, 
    async : false,
    type : "GET",
    dataType : 'json',
    success : function (result) {
        console.log(result)
        codeMap = result;
    }
});