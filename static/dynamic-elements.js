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
	$.ajax({url:"/dynamic-shopping-cart", method:"POST"}).done(update_dynamic_shopping_cart);
	$("select#pagination-select").change(function(){ 
		$.ajax({url:"/producten/pagination-change/"+$(this).val(), method:"POST"}).done(function(data){ 
			window.location.href = data;
		});
	});
});