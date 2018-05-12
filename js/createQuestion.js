count = 0;
total = 0;

function check(){
    var flag = 1;
    var title = document.getElementsByName("title")[0].value;
    var des = document.getElementsByName("des")[0].value;
    var questions = document.getElementsByClassName("qdiv");
    var array = [];
    var time = document.getElementsByName("time")[0].value;
    var c = document.getElementsByName("category")[0];
    var category = c.options[c.selectedIndex].value;
    var mark = document.getElementsByName("mark")[0].value;
    var questionnaire = {};

    if(title == ""){
        alert("Title must be filled out");
    }
    else{
        if(des == ""){
            des = title;
        }
        var i;
        for(i=0;i<count;i++){
            var dict = {};
            var qt = questions[i].getElementsByTagName("div")[0].getElementsByTagName("input")[0].value;
            if(qt == ""){
                alert("All Questions must be filled out");
                break;
            }
            dict["question"] = qt;
            var type = questions[i].getElementsByTagName("div")[0].getElementsByTagName("select")[0];
            var type1 = type.options[type.selectedIndex].value;
            dict["type"] = type1;
            if(type1 == "mc" || type1 == "checkbox" || type1 == "dropdown"){
                var j;
                var len = questions[i].getElementsByTagName("div").length;
                var answers = [];
                for(j=1;j<len;j++){
                    var ans = questions[i].getElementsByTagName("div")[j].getElementsByTagName("input")[0].value;
                    if(ans == ""){
                        alert("All choice must be filled out");
                        flag = 0;
                        break;
                    }
                    answers.push(ans);
                }
                if(flag == 1){
                    dict["answer"] = answers;
                    array.push(dict);
                }
            }
            else if(type1 == "ratingscale"){
                var table = questions[i].getElementsByTagName("div")[1].getElementsByTagName("input");
                var label = [];
                if(table[0].value == "" || table[1].value == ""){
                    alert("All label must be filled out");
                    flag = 0;
                    break;
                }
                label.push(table[0].value);
                label.push(table[1].value);
                dict["label"] = label;
                var scale = [];
                scale.push(table[2].value);
                scale.push(table[3].value);
                dict["scale"] = scale;
                array.push(dict);
            }
            else{
                array.push(dict);
            }
            if(flag == 0){
                break;
            }
        }
        if(flag == 1){
            if(time == ""){
                alert("Closed Time must be filled out");
            }
            //send
            else{
                questionnaire["title"] = title;
                questionnaire["description"] = des;
                questionnaire["question"] = array;
                questionnaire["time"] = time;
                questionnaire["category"] = category;
                questionnaire["mark"] = mark;
                questionnaire["num"] = count;

                var $form = $("<form action='/cgi-bin/checkQuestion.py' method='post'></form>");
                var $t = $("<input type='text' name='data'>");
                $t.val(JSON.stringify(questionnaire));
                $form.append($t);
                $(document.body).append($form);
                $form.submit();
            }
        }
    }
}

function dela(obj){
    var div = $(obj).parent();
    var next1 = div.next()[0];
    if(next1.nodeName == "DIV"){
        var next2 = div.next().next()[0];
        if(next2.nodeName == "DIV"){
            div.remove();
        }
        else{
            var prev1 = div.prev()[0];
            if(prev1.nodeName == "DIV"){
                div.remove();
            }
            else{
                alert("You must have at least two options!");
            }
        }
    }
    else{
        var prev1 = div.prev()[0];
        if(prev1.nodeName == "DIV"){
            var prev2 = div.prev().prev()[0];
            if(prev2.nodeName == "DIV"){
                div.remove();
            }
            else{
                alert("You must have at least two options!");
            }
        }
    }
}

function addmc(obj){
    var option = "<input class='input1' type ='text'></input>";
    var btn = "<button class='del' id='del' onClick='dela(this)'><h2>X</h2></button>";
    var div = "<div>" +  option + btn + "</div>";
    $(div).insertBefore($(obj));
}

function choice(){
    var div = "<div>";
    var option = "<input class='input1' type ='text'></input>";
    var btn = "<button class='del' id='del' onClick='dela(this)'><h2>X</h2></button>";
    div = div + option + btn + "</div>";
    return div;
}

function delq(obj){
    if(count == 1){
        alert("You must have at least one question!");
    }
    else{
        var div = $(obj).parent().parent();
        count = count - 1;
        div.remove();
        markchange();
    }
}

function change(obj){
    var a = obj.options[obj.selectedIndex].value;
    var div = $(obj).parent();
    var parent = div.parent();
    var next1 = div.next();
    var i;
    while(1){
        next1.remove();
        if(parent.children().last().is(div)){
            break;
        }
        next1 = div.next();
    }
    if(a == "mc" || a == "checkbox" || a == "dropdown"){
        $("<h4>Option</h4>").insertAfter(parent.children().last());
        var question = choice();
        $(question).insertAfter(parent.children().last());
        $(question).insertAfter(parent.children().last());
        var add = "<button class='add' id='add' onClick='addmc(this)'><h2>+</h2></button>";
        $(add).insertAfter(parent.children().last());
    }
    if(a == "ratingscale"){
        var div1 = "<div style='justify-content: center;'>";
        var table = "<table><tr>"+
                    "<td>Label</td><td><input class='input3' type ='text' name='label'></input></td>"+
                    "<td></td><td><input class='input3' type ='text' name='question'></input></td>"+
                    "</tr>"+
                    "<tr>"+
                    "<td>Scale</td><td><input class='input3' type ='number' name='scale' value=0></input></td>"+
                    "<td>to</td><td><input class='input3' type ='number' name='scale' value=5></input></td>"+
                    "</tr></table>";
        div1 = div1 + table + "</div>";
        $(div1).insertAfter(div);
    }
}

function addquestion(){
    var hr = document.getElementById("hr");
    var div = "<div class='qdiv'><hr>";
    var btn = "<button class='delq' onClick='delq(this)'>Delete</button>";
    div = div + "<h4>Question" + btn + "</h4>";
    var option = "<select class='input2' name='type' onchange='change(this)'>";
    option = option + "<option value='mc' selected='selected'>Multiple choice</option>";
    option = option + '<option value="checkbox">Checkboxes</option>';
    option = option + '<option value="dropdown">Dropdown</option>';
    option = option + '<option value="ratingscale">Rating scale</option>';
    option = option + '<option value="shortq">Short Question</option>';
    option = option + '<option value="longq">Long Question</option>';
    option = option + '</select>';
    var name = "<div><input class='input1' type ='text' name='question'></input>" + option + "</div>";
    div = div + name;
    div = div + "<h4>Option</h4>"
    var question = choice();
    div = div + question + question;
    var add = "<button class='add' id='add' onClick='addmc(this)'><h2>+</h2></button>";
    div = div + add;
    div = div + "</div>";
    $(div).insertBefore($(hr));
    count = count + 1;
    markchange();
}

function markchange(){
    var extra = document.getElementsByName("mark")[0].value;
    total = 3 * count + parseInt(extra);
    var mark = document.getElementById("total");
    mark.innerText = "Total Mark: " + total;
    $(mark).append('<button disabled title="Total mark = 3*number of question + extra mark">?</button>');
}

document.addEventListener("DOMContentLoaded", function(event){
    addquestion();
    var x = document.getElementById('plus');
    x.addEventListener('click', addquestion);
    var y = document.getElementsByClassName('qs')[0];
    y.addEventListener('click', check);
    var extra = document.getElementsByName("mark")[0];
    extra.addEventListener('change', markchange);
});
