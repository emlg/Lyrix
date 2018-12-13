function query(){
	/*console.log($('form').serialize());*/
	$.ajax({
		url: '/create',
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


function update_data(swap){
	swap = swap.replace(/'/g, '"')
  console.log(swap);
	swap = JSON.parse(swap)
	lyrics = document.getElementById("in_lyrics").value.split(" ")
	for(var i=0; i < lyrics.length; i++){
		if (Object.keys(swap).includes(lyrics[i])){
			lyrics[i] = '<b>' + swap[lyrics[i]] + '</b>';
		}
	}
  document.getElementById("new_lyrics").innerHTML = lyrics.join(" ");
}
