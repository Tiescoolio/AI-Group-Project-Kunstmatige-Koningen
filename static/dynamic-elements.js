// TODO: expand upon this function, displaying dynamic shopping cart elements in HTML.
function update_dynamic_shopping_cart(data){
	shopdata = JSON.parse(data);
	$("#shopping-cart-count").html(" ("+shopdata.itemcount+")");
}

$(document).ready(function() {
	
	$("a[function=add-to-shopping-cart]").click(function(event){
		$.ajax({url:"/add-to-shopping-cart/"+$(this).attr("productid"), method:"POST"}).done(update_dynamic_shopping_cart);
		event.preventDefault();
	});

	$("a[function=show-sessionbar-dynamic]").click(function(event){
		$("#sessionbar-static").attr("style","display:none");
		$("#sessionbar-dynamic").attr("style","");
		event.preventDefault();
	});

	$("a[function=show-sessionbar-static]").click(function(event){
		$("#sessionbar-dynamic").attr("style","display:none");
		$("#sessionbar-static").attr("style","");
		event.preventDefault();
	});

	$("[function=change-profile-id]").click(function(event){ 
		$.ajax({url:"/change-profile-id", method:"POST", data:{"session_id":$("input#profile-id-input").val()}}).done(function(){ location.reload(); });
		event.preventDefault();
	});
	
	$.ajax({url:"/dynamic-shopping-cart", method:"POST"}).done(update_dynamic_shopping_cart);
	
	$("select#pagination-select").change(function(){ 
		$.ajax({url:"/producten/pagination-change/"+$(this).val(), method:"POST"}).done(function(data){ 
			window.location.href = data;
		});
	});

/*
	$(".menuitem").hover(function(){
		$("#"+$(this).attr("dropdown")).attr("style","display:block");
	}, function(){
		$("#"+$(this).attr("dropdown")).attr("style","display:none");
	});
*/
/*
	$("#menuwrapper").hover(function(event){
		var target = $( event.target );
		$(".menudropdown").attr("style","display:none");
		if(target.attr('dropdown')){
			$("#"+target.attr("dropdown")).attr("style","display:block");
		}
	}, function(){
		$(".menudropdown").attr("style","display:none");
	})
*/
	$(".menuitem").hover(function(){
		$(".menudropdown").attr("style","display:none");
		$("#"+$(this).attr("dropdown")).attr("style","display:block");
	}, function(){});

	$("#menuwrapper").hover(function(event){}, function(){
		$(".menudropdown").attr("style","display:none");
	})

});