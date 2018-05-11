count = 1;

function validateForm(){
    var x = document.forms["myform"]["title"].value;
    if (x == ""){
        alert("Title must be filled out");
        return false;
    }
    x = document.forms["myform"]["time"].value;
    if (x == ""){
        alert("Closed Time must be filled out");
        return false;
    }
    x = document.forms["myform"]["mark"].value;
    if (x == ""){
        alert("Mark must be filled out");
        return false;
    }
}

function dela(obj){
    $(obj).parent().remove();
}

function addmc(obj){
    var option = "<input class='input1' type ='text' name='o'></input>";
    var btn = "<button class='del' id='del' onClick='dela(this)'><h2>X</h2></button>";
    var div = "<div>" +  option + btn + "</div>";
    $(div).insertBefore($(obj));
}

function mc(num){
    var hr = document.getElementById("div"+ num);
    var count1 = 1;
    var option = "<input class='input1' type ='text' name='o"+ count1 +"'></input>";
    var btn = "<button class='del' id='del' onClick='dela(this)'><h2>X</h2></button>";
    var div = "<div>" +  option + "</div>";
    var div1 = "<div><h4>Answer</h4>" + div;
    count1 = count1 + 1;
    option = "<input class='input1' type ='text' name='o"+ count1 +"'></input>";
    div = "<div>" +  option + "</div>";
    div1 = div1 + div;
    count1 = count1 + 1;
    var add = "<button class='del' id='add' onClick='addmc(this)'><h2>+</h2></button>";
    div1 = div1 + add;
    $(div1).insertAfter($(hr));
}

function addquestion(){
	var hr = document.getElementById("hr");
    var line = "<hr id=hr" + count + ">";
    $(line).insertBefore($(hr));
	$("<h4>Question</h4>").insertBefore($(hr));
    var option = "<select class='input2' name='type"+ count +"' form='myform'>";
    option = option + "<option value='mc' selected='selected'>Multiple choice</option>";
    option = option + '<option value="checkbox">Checkboxes</option>';
    option = option + '<option value="dropdown">Dropdown</option>';
    option = option + '<option value="ratingscale">Rating scale</option>';
    option = option + '<option value="shortq">Short Question</option>';
    option = option + '<option value="longq">Long Question</option>';
    option = option + '</select>';
	var name = "<div id='div" + count + "'><input class='input1' type ='text' name='question" + count + "'></input>" + option + "</div>";
    $(name).insertBefore($(hr));
    var t = document.getElementsByName('type'+count)[0];
    var o = t.options[t.selectedIndex].value;
    if(o == 'mc'){
        mc(count);
    }
    count = count + 1;
}

document.addEventListener("DOMContentLoaded", function(event){
    addquestion();
    var x = document.getElementById('plus');
    x.addEventListener('click', addquestion);
});
