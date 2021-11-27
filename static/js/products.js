//on search form submit
$("#search-form").submit(function(e) {
	e.preventDefault();
	var query = $("#search-form input").val().toLowerCase();

	$(".product").hide();
	$(".product").each(function() {
		var model = $(this).model.toLowerCase(),
		    status = $(this).status.toLowerCase(),
			category = $(this).category.toLowerCase();

		if (model.indexOf(query) > -1 || status.indexOf(query) > -1 || category.indexOf(query) > -1) {
			$(this).show();
		}
	});
});

//var data = [
//	{
//		"model" = {{ productItem[0] }',
//		"category": "Technology",
//		"price": "$280",
//		"status": "Available",
//		"image": "/static/img/portfolio/oculus-quest-2.jpg"
//	}
//];
//

//
//for (var i in '{{ allProducts|safe }}') {
//	var model = '{{ allProducts[0] }}',
//		category = data[i].category,
//		price = data[i].price,
//		status = data[i].status,
//		rawPrice = price.replace("$",""),
//		rawPrice = parseInt(rawPrice.replace(",","")),
//		image = data[i].image;
//
//
//    //create product cards
//    products += "<div class='col-sm-4 product' data-model='" + model + "' data-category='" + category + "' data-price='" + rawPrice + "' data-status='" + status + "'><div class='product-inner text-center'><img src='" + image + "'><br />Model: " + model + "<br />Category: " + category + "<br />Price: " + price + "<br />Status: " + status + "</div></div>";		models += "<option value='" + model + "'>" + model + "</option>";
//
//
//
//    var model = document.getElementById('model');
//    var category = document.getElementById('category');
//    var price = document.getElementById('price');
//    var status = document.getElementById('status');
//
//    var categories = "Technology","Clothing", "Home Appliances", "Vehicle Accessories";
//    var statues = "Auction", "Reported", "Sold", "Unsold";
//
//    //create dropdown of category
//    if (categories.indexOf("<option value='" + category + "'>" + category + "</option>") == -1) {
//        categories += "<option value='" + category + "'>" + category + "</option>";
//    }
//
//    //create dropdown of status
//    if (statuses.indexOf("<option value='" + status + "'>" + status + "</option>") == -1) {
//        statuses += "<option value='" + status + "'>" + status + "</option>";
//    }
//
//
////$("#products").html(products);
////$(".filter-model").append(models);
//$(".filter-category").append(categories);
//$(".filter-status").append(statuses);
//
//
//var filtersObject = {};
//
////on filter change
//$(".filter").on("change",function() {
//	var filterName = $(this).data("filter"),
//		filterVal = $(this).val();
//
//	if (filterVal == "") {
//		delete filtersObject[filterName];
//	} else {
//		filtersObject[filterName] = filterVal;
//	}
//
//	var filters = "";
//
//	for (var key in filtersObject) {
//	  	if (filtersObject.hasOwnProperty(key)) {
//			filters += "[data-"+key+"='"+filtersObject[key]+"']";
//	 	}
//	}
//
//	if (filters == "") {
//		$(".product").show();
//	} else {
//		$(".product").hide();
//		$(".product").hide().filter(filters).show();
//	}
//});


