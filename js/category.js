function hide (elements) {
  elements = elements.length ? elements : [elements];
  for (var index = 0; index < elements.length; index++) {
    elements[index].style.display = 'none';
  }
}

function show (elements) {
  elements = elements.length ? elements : [elements];
  for (var index = 0; index < elements.length; index++) {
    elements[index].style.display = 'block';
  }
}


function art(){
	var art = document.getElementsByClassName("art");
	var business = document.getElementsByClassName("business");
	var education = document.getElementsByClassName("education");
	var engineering = document.getElementsByClassName("engineering");
	var science = document.getElementsByClassName("science");
	var social = document.getElementsByClassName("social");

	if(art.length != 0){
		show(art);
	}
	if(business.length != 0){
		hide(business);
	}
	if(education.length != 0){
		hide(education);
	}
	if(engineering.length != 0){
		hide(engineering);
	}
	if(science.length != 0){
		hide(science);
	}
	if(social.length != 0){
		hide(social);
	}
}


function business(){
	var art = document.getElementsByClassName("art");
	var business = document.getElementsByClassName("business");
	var education = document.getElementsByClassName("education");
	var engineering = document.getElementsByClassName("engineering");
	var science = document.getElementsByClassName("science");
	var social = document.getElementsByClassName("social");

	if(art.length != 0){
		hide(art);
	}
	if(business.length != 0){
		show(business);
	}
	if(education.length != 0){
		hide(education);
	}
	if(engineering.length != 0){
		hide(engineering);
	}
	if(science.length != 0){
		hide(science);
	}
	if(social.length != 0){
		hide(social);
	}
}


function education(){
	var art = document.getElementsByClassName("art");
	var business = document.getElementsByClassName("business");
	var education = document.getElementsByClassName("education");
	var engineering = document.getElementsByClassName("engineering");
	var science = document.getElementsByClassName("science");
	var social = document.getElementsByClassName("social");

	if(art.length != 0){
		hide(art);
	}
	if(business.length != 0){
		hide(business);
	}
	if(education.length != 0){
		show(education);
	}
	if(engineering.length != 0){
		hide(engineering);
	}
	if(science.length != 0){
		hide(science);
	}
	if(social.length != 0){
		hide(social);
	}
}


function engineering(){
	var art = document.getElementsByClassName("art");
	var business = document.getElementsByClassName("business");
	var education = document.getElementsByClassName("education");
	var engineering = document.getElementsByClassName("engineering");
	var science = document.getElementsByClassName("science");
	var social = document.getElementsByClassName("social");

	if(art.length != 0){
		hide(art);
	}
	if(business.length != 0){
		hide(business);
	}
	if(education.length != 0){
		hide(education);
	}
	if(engineering.length != 0){
		show(engineering);
	}
	if(science.length != 0){
		hide(science);
	}
	if(social.length != 0){
		hide(social);
	}
}


function science(){
	var art = document.getElementsByClassName("art");
	var business = document.getElementsByClassName("business");
	var education = document.getElementsByClassName("education");
	var engineering = document.getElementsByClassName("engineering");
	var science = document.getElementsByClassName("science");
	var social = document.getElementsByClassName("social");

	if(art.length != 0){
		hide(art);
	}
	if(business.length != 0){
		hide(business);
	}
	if(education.length != 0){
		hide(education);
	}
	if(engineering.length != 0){
		hide(engineering);
	}
	if(science.length != 0){
		show(science);
	}
	if(social.length != 0){
		hide(social);
	}	
}


function social(){
	var art = document.getElementsByClassName("art");
	var business = document.getElementsByClassName("business");
	var education = document.getElementsByClassName("education");
	var engineering = document.getElementsByClassName("engineering");
	var science = document.getElementsByClassName("science");
	var social = document.getElementsByClassName("social");

	if(art.length != 0){
		hide(art);
	}
	if(business.length != 0){
		hide(business);
	}
	if(education.length != 0){
		hide(education);
	}
	if(engineering.length != 0){
		hide(engineering);
	}
	if(science.length != 0){
		hide(science);
	}
	if(social.length != 0){
		show(social);
	}
}

function myfun(qid){
	var $form = $("<form action='/cgi-bin/printQuestion.py' method='post'</form>");
	var $t = $("<input type='text' name='qid'>");
	$t.val(qid);
	$form.append($t);
	$(document.body).append($form);
	$form.submit();
}


document.addEventListener("DOMContentLoaded", function(event){
	var art1 = document.getElementById("Art");
	art1.addEventListener('click', art);
	var business1 = document.getElementById("Business");
	business1.addEventListener('click', business);
	var education1 = document.getElementById("Education");
	education1.addEventListener('click', education);
	var engineering1 = document.getElementById("Engineering");
	engineering1.addEventListener('click', engineering);
	var science1 = document.getElementById("Science");
	science1.addEventListener('click', science);
	var social1 = document.getElementById("Social");
	social1.addEventListener('click', social);
});

