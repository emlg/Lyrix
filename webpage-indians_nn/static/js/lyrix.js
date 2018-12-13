function queryNN(){
  /*var input = document.getElementById("input").value;*/
  /*console.log($('form').serialize());*/
	console.log("Entered JavaScript")
	$.ajax({
		url: '/predict',
    cache : false,
		data: $('form').serialize(),
		type: 'POST',
		success: function(response){
			/*console.log("success " +response);*/
      update_data(response);
		},
		error: function(error){
      console.log(error);
		}
	});

}

function update_data(pred){
  /*console.log("Exited queryNN()");*/
  document.getElementById("prediction").innerHTML = "We predicted the score : "+ pred;
}
