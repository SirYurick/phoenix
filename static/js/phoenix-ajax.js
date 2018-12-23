$(document).ready(function() {
	$('#bonus').click(function(){
	var score;
	score = $(this).attr("score");
	$.get('/phoenix/get_bonus/', {score: score}, function(data){
		$('#score').html(data);
		$('#bonus').hide();
		});
	});

	$('#suggestion').keyup(function(){
		var query;
		query = $(this).val();
		$.get('/rango/suggest_category/', {suggestion: query}, function(data){
			$('#cats').html(data);
		})
	})

	$('.rango-add').click(function(){
		var catid = $(this).attr("data-catid");
		var url = $(this).attr("data-url");
		var title = $(this).attr("data-title");
		var me = $(this);
		$.get('/rango/auto_add_page/', {category_id: catid, url: url, title: title}, function(data){
			$('#pages').html(data);
			me.hide();
		})
	})

	$('.rango-del').click(function(){
		var pageid = $(this).attr("data-pageid");
		var catid = $(this).attr("data-catid");
		$.get('/rango/remove_page/', {page_id: pageid, cat_id: catid}, function(data){
			$('#pages').html(data);
		})
	})

});
