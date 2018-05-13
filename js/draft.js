var num_q;
var question;
var mytime;
function prepare(i, qt){
	num_q = i;
	question = JSON.parse(qt);
	//var questions = document.getElementsByClassName('qdiv');
	//var qt = questions[i].getElementsByTagName('div')[0].getElementsByTagName('input')[0].value;
	//console.log(JSON.parse(qt)[0]);
}

function settime(time){
	mytime = time;
	document.getElementsByName("time")[0].value = mytime;
}

document.addEventListener("DOMContentLoaded", function(event){
	var i;
	var btn = 0;
	for(i=0; i<num_q; i++){
		var questions = document.getElementsByClassName("qdiv");
		questions[i].getElementsByTagName("div")[0].getElementsByTagName("input")[0].value = question[i]["question"];
		var type = questions[i].getElementsByTagName("div")[0].getElementsByTagName("select")[0];
		var flag = 0;
		if(question[i]["type"] == "mc"){
			type.selectedIndex = 0;
			flag = 1;
		}
		else if(question[i]["type"] == "checkbox"){
			type.selectedIndex = 1;
			flag = 1;
			change(type);
		}
		else if(question[i]["type"] == "dropdown"){
			type.selectedIndex = 2;
			flag = 1;
			change(type);
		}
		else if(question[i]["type"] == "ratingscale"){
			type.selectedIndex = 3;
			flag = 2;
			change(type);
		}
		else if(question[i]["type"] == "shortq"){
			type.selectedIndex = 4;
			flag = 3;
			change(type);
		}
		else{
			type.selectedIndex = 5;
			flag = 3;
			change(type);
		}
		if(flag == 1){
			var num_a = question[i]["answer"].length - 2;
			var j;
			while(num_a > 0){
				var add = document.getElementsByClassName("add")[btn];
				add.click();
				num_a = num_a - 1;
			}
			btn = btn + 1;
			for(j=0;j<question[i]["answer"].length;j++){
				questions[i].getElementsByTagName("div")[j+1].getElementsByTagName("input")[0].value = question[i]["answer"][j];
			}
		}
		else if(flag == 2){
			var table = questions[i].getElementsByTagName("div")[1].getElementsByTagName("input");
			table[0].value = question[i]["label"][0];
			table[1].value = question[i]["label"][1];
			table[2].value = question[i]["scale"][0];
			table[3].value = question[i]["scale"][1];
		}
	}
});