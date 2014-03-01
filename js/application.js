function modify(event){
	m = confirm("是否更改选中的头像为默认头像？");
	element = event.target;
	if(m){
		default_img = document.getElementById("info").getElementsByTagName("img")[0];
		select_img = element.src;
		default_img.src = select_img;
		imgname = select_img.substring(select_img.lastIndexOf("/"));
		images_div = document.getElementById("images");
		for (var i=0; i < images_div.childNodes.length; i++) {
			image = images_div.childNodes[i];
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

function ready(){
	images_div = document.getElementById("images");
	for (var i = images_div.childNodes.length - 1; i >= 0; i--) {
		images_div.childNodes[i].onclick = modify
	}
}

document.addEventListener('DOMContentLoaded', ready, false);
