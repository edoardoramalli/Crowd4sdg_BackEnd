var file
var configSet = {method: "", csv_url: "", col_name: "", filters:[], confidence_thresholds:[] }

/* Copyright 2012-2013 Daniel Tillin -- csvToArray v2.1 (Unminifiled for development) -- http://code.google.com/p/csv-to-array/ */
String.prototype.csvToArray = function (o) {
    var od = {
        'fSep': ',',
        'rSep': '\n',
        'quot': '"',
        'head': false,
        'trim': false
    }
    if (o) {
        for (var i in od) {
            if (!o[i]) o[i] = od[i];
        }
    } else {
        o = od;
    }
    var a = [
        ['']
    ];
    for (var r = f = p = q = 0; p < this.length; p++) {
        switch (c = this.charAt(p)) {
            case o.quot:
                if (q && this.charAt(p + 1) == o.quot) {
                    a[r][f] += o.quot;
                    ++p;
                } else {
                    q ^= 1;
                }
                break;
            case o.fSep:
                if (!q) {
                    if (o.trim) {
                        a[r][f] = a[r][f].replace(/^\s\s*/, '').replace(/\s\s*$/, '');
                    }
                    a[r][++f] = '';
                } else {
                    a[r][f] += c;
                }
                break;
            case o.rSep.charAt(0):
                if (!q && (!o.rSep.charAt(1) || (o.rSep.charAt(1) && o.rSep.charAt(1) == this.charAt(p + 1)))) {
                    if (o.trim) {
                        a[r][f] = a[r][f].replace(/^\s\s*/, '').replace(/\s\s*$/, '');
                    }
                    a[++r] = [''];
                    a[r][f = 0] = '';
                    if (o.rSep.charAt(1)) {
                        ++p;
                    }
                } else {
                    a[r][f] += c;
                }
                break;
            default:
                a[r][f] += c;
        }
    }
    if (o.head) {
        a.shift()
    }
    if (a[a.length - 1].length < a[0].length) {
        a.pop()
    }
    return a;
}

/********** load CSV locally **********/
$('#load-csv').change(function () {
    let i = $(this).prev('label').clone();
    file = $('#load-csv')[0].files[0];
    $(this).prev('label').text(file.name);
    if (file) {
        let reader = new FileReader();
        reader.addEventListener('load', function (e) {
            let text = e.target.result;
            firstRow = text.csvToArray()[0];
            createDropDown(firstRow)
        });
        reader.addEventListener('error', function () {
            alert('Error : Failed to read file');
        });
        reader.readAsText(file);
    }
})

/* create the column names dropdown list */
function createDropDown(inputList) {
    $("div[id='columnNameListParent']").removeClass('d-none')
    deletChild('columnNameList')
    var dropdown = $('#columnNameList')
    dropdown.append($('<option>').attr({ value:'none', label:'Choose a column'}))
    inputList.forEach(element => {
        var entry = $('<option>').attr({ value:element, label:element})
        dropdown.append(entry)
    });
    $("div[id='filterSelection']").removeClass('d-none')
    $("div[id='submitSection']").removeClass('d-none')
}

/********** main selection **********/
$('select').change(function() {
    var selectedValue = $(this).val()
    if (selectedValue == 'methodGET') {
        configSet.method = 'GET'
        // Hide ALL
        $("div[class='row']").addClass('d-none')
        
        //Show GET
        $("div[id='csvLinkSection']").removeClass('d-none')
        $("div[id='columnNameboxParent']").removeClass('d-none')
        $("div[id='filterSelection']").removeClass('d-none')
        $("div[id='submitSection']").removeClass('d-none')
        
    } else if (selectedValue == 'methodPOST') {
        configSet.method = 'POST'
        //Hide ALL
        $("div[class='row']").addClass('d-none')

        //Show POST
        $("div[id='csvFileSection']").removeClass('d-none')
    }
    else if (selectedValue == 'removeAll'){
        $("div[class='row']").addClass('d-none')
    }
});

/* remove children of an element specified by element ID */
function deletChild(id_element) {
    var e = document.querySelector("#" + id_element);
    var child = e.firstElementChild;
    while (child) {
        e.removeChild(child);
        child = e.lastElementChild;
    }
}

/********** URL and path **********/
$('.urls').change(function() {
    var value = $(this).val()
    configSet.csv_url = value
});

/********** column Name **********/
$('.columns').change(function() {
    var value = $(this).val()
    configSet.col_name = value
});

/**********  filters **********/
$('#filter1').change(function() {
    var value = $(this).val()
    configSet.filters[0] = value
})
$('#filter2').change(function() {
    var value = $(this).val()
    configSet.filters[1] = value
})
$('#filter3').change(function() {
    var value = $(this).val()
    configSet.filters[2] = value
})

/**********  thresholds **********/
$('#threshold1').change(function() {
    var value = $(this).val()
    configSet.confidence_thresholds[0] = value
})
$('#threshold2').change(function() {
    var value = $(this).val()
    configSet.confidence_thresholds[1] = value
})
$('#threshold3').change(function() {
    var value = $(this).val()
    configSet.confidence_thresholds[2] = value
})

function urlMaker(){
    url_string = ""
    
    // adding the first character
    url_string = url_string.concat("?")
    
    // concatinating the filternames
    configSet.filters.forEach(element => {
        url_string = url_string.concat('filter_name_list=',element,'&')
    });

    // concatinating the thresholds
    configSet.confidence_thresholds.forEach(element => {
        url_string = url_string.concat('confidence_threshold_list=',element,'&')
    });

    // remove the extra & sign in the loop
    url_string = url_string.slice(0, -1)

    // url_string = url_string.concat('column_name=',configSet.col_name,'&')
    // url_string = url_string.concat('csv_url=',configSet.csv_url)
    return url_string
}

/**********  submit button **********/
$("button").click(function(){
    if (configSet.method == 'GET') {
        $.get("https://131.175.120.2:7777/Filter/API/filterImageURL"+urlMaker(), {column_name : configSet.col_name, csv_url : configSet.csv_url}, function(data, status){ alert("Data: " + data + "\nStatus: " + status) })
    } else if (configSet.method == 'POST'){
        // $.post("https://131.175.120.2:7777/Filter/API/filterImage", {name: "a", set: "b"}, function(data, status){ alert("Data: " + data + "\nStatus: " + status) })
    }
  });
