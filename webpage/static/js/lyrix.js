$(document).ready(function() {

    $("#genre_1").change(function() {
        var val = $(this).val();
        if (val == "rock") {
            $("#song").html("<option value=0>Far From Heroes, 'The tallest tale'</option><option value=1>Blue Cheer, 'Girl next door'</option><option value=2>Blitzkid, 'Making a monster'</option><option value=3>Feeder, 'Save us'</option><option value=4>The cult, 'A flower in the desert'</option>");
        } else if (val == "pop") {
            $("#song").html("<option value=0>item2: test 1</option><option value=1>item2: test 2</option>");

        } else if (val == "classical") {
            $("#song").html("<option value=0>item3: test 1</option><option value=1>item3: test 2</option>");

        } else if (val == "jazz") {
            $("#song").html("<option value=0>item4: test 1</option><option value=1>item4: test 2</option>");

        } else if (val == "electronic") {
            $("#song").html("<option value=0>item5: test 1</option><option value=1>item5: test 2</option>");

        }
    });
});

function query_muse(){
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

var lyrics_base = ['where can we go what can we do<br>we re lost alone removed confused<br>let down and torn apart<br>seek knowledge from the heart<br>rework the illustrations we are a new creation<br>searching for the tower where the bells ring on the hour<br>where the present and the future don t look sour<br>we re telling everyone we know so we can say that everybody knows<br>can t feed a hungry mouth when it s closed<br>teach lies why try<br>give up give in<br>pretend turn heads<br>keep up sink in<br>misguided from the start<br>seek wisdom from the heart<br>you can try your best to please us<br>we ll bite the hand that feeds us<br>just when our time was running out and patience wearing thin<br>we start again where to begin<br>there s room for many more if you can fit into the mold<br>but don t come in go chase the wind',
'sitin  by the tv sittin  drinkin  my wine<br>my friends all say that i m wasting time<br>i m gonna wait right here just to get the right meat<br>i been waiting for hours i can wait all week<br>i m not talkin   bout love<br>not talkin   bout war<br>get what i need from the girl next door<br>been watchin  cartoons on the tv screen<br>what i m looking for is long and lean<br>a ticket to ride i want my feet in the air<br>i m gonna tell my baby that i just don t care<br>i m not talkin   bout love<br>not talkin   bout war<br>get what i need from the girl next door<br>yeah get what i need oh yeah oh<br>been runnin  down the scene with my gasoline<br>i m feeling nasty and mighty mean<br>said outta my way cause i m runnin  hot<br>i got to show my baby just what i got<br>i m not talkin   bout love<br>not talkin   bout war<br>take what i need from the girl next door<br>i m not talkin   bout love<br>not talkin   bout war<br>take what i need from the girl next door<br>i m not talkin   bout love<br>not talkin   bout war<br>get what i need from the girl next door<br>yeah i get what i need from that mojo yeah<br>oh',
'born into this world the sum parts of a man<br>created through experiments from scientific hands<br>and though i live and breathe i cannot understand<br>with the mind of a child if this is what they planned<br>look upon me then hide away your face<br>i am unlike you yet still i need a place<br>within society where i can still be safe<br>from all the ignorance of the human race<br>i can try i still don t know why<br>they wanna lock me away<br>from all i ve seen it makes no sense to me<br>they make a monster everyday<br>they make a monster everyday<br>they make a monster everyday<br>they make a monster everyday<br>they make a monster everyday',
'face against the ground<br>torn but you can stand<br>your will is strong but you have now<br>i know you can save us<br>faith is on your side<br>fears you can t deny<br>it s burned a hole right through your soul<br>but i know you can save us<br>save us now<br>don t say goodbye<br>i know you can save us<br>don t wave goodbye<br>but nothing can break us<br>don t say goodbye<br>i know you can save us<br>you can bring us back again<br>born to be as one<br>turn to face the sun<br>your will is strong but you have now<br>i know you can save us<br>save us now<br>don t say goodbye<br>i know you can save us<br>don t wave goodbye<br>but nothing can break us<br>don t say goodbye<br>i know you can save us<br>you can bring us back again<br>you can bring us back again<br>face against the ground<br>torn but you can stand<br>your will is strong but you have now<br>i know you can save us<br>don t say goodbye<br>i know you can save us<br>don t wave goodbye<br>but nothing can break us<br>don t say goodbye<br>i know you can save us<br>you can bring us back again<br>don t say goodbye<br>i know you can save us<br>don t wave goodbye<br>but nothing can break us<br>don t say goodbye<br>i know you can save us<br>you can bring us back again<br>you can bring us back again',
'wait a minute my friend<br>don t pass me up for dead<br>as babylon crumbles to sand<br>a sweet flower blossoms in my hand<br>another day is ending for you<br>another day<br>while i m alive you see my rivers flowing<br>don t want to be like you<br>there are no wild beasts in here i know<br>there are no wild beasts in here we know<br>and a voice of the people cries<br>as it drones on in monotone<br>here is the news it s all so sad sad<br>ooh and those black and whites<br>but thy knew it<br>took a few and those panties in acquainted ways<br>come on<br>come on<br>come on away yeah<br>wait a minute my friend<br>don t pass me up for dead<br>as babylon crumbles to sand<br>a sweet flower blossoms in my hand<br>another day is ending for you<br>another day another day<br>i m alive<br>you see my body burning<br>burning up in here<br>there are no others in here i know<br>there are no others in here oh no<br>burning up in here<br>you know you know<br>step a little closer<br>i wonder if you can<br>remember me in this way'
]

function update_data(swap){
	swap = swap.replace(/'/g, '"');
  console.log(swap);
	swap = JSON.parse(swap);
	lyrics = lyrics_base[document.getElementById("song").value].split(" ");
	for(var i=0; i < lyrics.length; i++){
		if (Object.keys(swap).includes(lyrics[i])){
			lyrics[i] = '<b>' + swap[lyrics[i]] + '</b>';
		}
	}
  document.getElementById("new_lyrics").innerHTML = lyrics.join(" ");
}


function query_nn(){
  console.log("Managed to launch NN ! ");
  $.ajax({
    /* URL with name of function*/
		url: '/predict',
    cache : false,
		data: $('form').serialize(),
		type: 'POST',
		success: function(response){
			/*console.log("success " +response);*/
      update_lyrics(response);
		},
		error: function(error){
      console.log(error);
		}
	});
}

function update_lyrics(lyrics){
  document.getElementById("new_lyrics").innerHTML = lyrics;
}
