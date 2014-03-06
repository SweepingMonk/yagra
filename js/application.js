function modify(event){
	sure = confirm("是否更改选中的头像为默认头像？");
	element = event.target;
	if(element instanceof HTMLDivElement){
		element = element.firstChild
	}
	if(sure){
		default_img = document.getElementById("info").getElementsByTagName("img")[0];
		menu_img = document.getElementById("mainmenu").getElementsByTagName("img")[0];
		select_img = element.src;
		menu_img.src = select_img;
		default_img.src = select_img;
		imgname = select_img.substring(select_img.lastIndexOf("/"));
		images_div = document.getElementById("images");
		for (var i=0; i < images_div.children.length; i++) {
			image = images_div.children[i];
			if(image.className == "image default"){
				image.className = "image"
			}
		}
		element.parentNode.className = "image default";
		xmlhttp = new XMLHttpRequest();
		xmlhttp.open("GET", "/ajaxchangeimg" + imgname, true);
		xmlhttp.send(null);
	} 
}

function popMenu(){
	submenu = document.getElementById("submenu");
	submenu.style.display = "block";
}

function hidenMenu(){
	submenu = document.getElementById("submenu");
	submenu.style.display = "none";
}

function ready(){
	images_div = document.getElementById("images");
	if(images_div){
		for (var i = images_div.children.length - 1; i >= 0; i--) {
			images_div.children[i].onclick = modify
		}
	}
	
	mainmenu = document.getElementById("mainmenu");
	for (var i = 0, len = mainmenu.children.length; i < len; i++) {
		if (mainmenu.children[i].className == "subnav") {
			mainmenu.children[i].onmouseover = popMenu;
			mainmenu.children[i].onmouseout = hidenMenu;
		}
	}
}


document.addEventListener('DOMContentLoaded', ready, false);
