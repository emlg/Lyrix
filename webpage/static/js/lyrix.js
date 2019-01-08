$(document).ready(function() {

    $("#genre_1").change(function() {
        var val = $(this).val();
        if (val == "rock") {
            $("#song").html("<option value=0>Far From Heroes, 'The tallest tale'</option><option value=1>Blue Cheer, 'Girl next door'</option><option value=2>Blitzkid, 'Making a monster'</option><option value=3>Feeder, 'Save us'</option><option value=4>The cult, 'A flower in the desert'</option>");
        } else if (val == "pop") {
            $("#song").html("<option value=5>Beyonce, 'Single Ladies'</option><option value=6>ABBA, 'Man In The Middle'</option><option value=7>Michael Jackson, 'Thriller'</option><option value=8>The Beatles, 'Yesterday'</option><option value=9>Ariana Grande, 'Boyfriend Material'</option>");

        } else if (val == "metal") {
            $("#song").html("<option value=0>item3: test 1</option><option value=1>item3: test 2</option>");

        } else if (val == "jazz") {
            $("#song").html("<option value=0>item4: test 1</option><option value=1>item4: test 2</option>");

        } else if (val == "country") {
            $("#song").html("<option value=0>item5: test 1</option><option value=1>item5: test 2</option>");

        } else if (val == "hiphop") {
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
'wait a minute my friend<br>don t pass me up for dead<br>as babylon crumbles to sand<br>a sweet flower blossoms in my hand<br>another day is ending for you<br>another day<br>while i m alive you see my rivers flowing<br>don t want to be like you<br>there are no wild beasts in here i know<br>there are no wild beasts in here we know<br>and a voice of the people cries<br>as it drones on in monotone<br>here is the news it s all so sad sad<br>ooh and those black and whites<br>but thy knew it<br>took a few and those panties in acquainted ways<br>come on<br>come on<br>come on away yeah<br>wait a minute my friend<br>don t pass me up for dead<br>as babylon crumbles to sand<br>a sweet flower blossoms in my hand<br>another day is ending for you<br>another day another day<br>i m alive<br>you see my body burning<br>burning up in here<br>there are no others in here i know<br>there are no others in here oh no<br>burning up in here<br>you know you know<br>step a little closer<br>i wonder if you can<br>remember me in this way',
'all the single ladies <br>all the single ladies <br>all the single ladies <br>all the single ladies now put your hands up<br>up in the club  we just broke up  i m doing my own little thing<br>decided to dip and now you wanna trip <br> cause another brother noticed me<br>i m up on him he up on me<br>don t pay him any attention<br>just cried my tears for three good years<br>you can t get mad at me<br> cause if you liked it then you should have put a ring on it<br>if you liked it then you shoulda put a ring on it<br>don t be mad once you see that he want it<br> cause if you liked it then you shoulda put a ring on it<br>oh oh oh oh oh oh oh oh oh oh oh oh <br>if you liked it then you should have put a ring on it<br>if you liked it then you t be mad once you see that he want it<br>don t be mad once you see that he want it<br>if you liked it then you shoulda put a ring on it<br>i got gloss on my lips a man on my hips<br>got me tighter in my carryon jeans<br>acting up drink in my cup<br>i can t care less what you think<br>i need no permission did i mention<br>don t pay him any attention<br> cause you had your turn and now you gonna learn<br>what it really feels like to miss me<br> cause if you liked it then you should have put a ring on it<br>if you liked it then you shoulda put a ring on it<br>don t be mad once you see that he want it<br> cause if you liked it then you shoulda put a ring on it<br>oh oh oh oh oh oh<br>don t treat me to these things of the world<br>i m not that kind of girl<br>your love is what i prefer what i deserve<br>is a man that makes me then takes me<br>and delivers me to a destiny to infinity and beyond<br>pull me into your arms<br>say i m the one you want<br>if you don t you ll be alone<br>and like a ghost i ll be gone<br>all the single ladies<br>all the single ladies <br>all the single ladies <br>all the single ladies now put your hands up<br>oh oh oh oh oh oh<br> cause if you liked it then you should have put a ring on it<br>if you liked it then you shoulda put a ring on it<br>don t be mad once you see that he want it<br>if you liked it then you shoulda put a ring on it<br>oh oh oh<br>if you liked it then you should have put a ring on it<br>if you liked it then you shoulda put a ring on it<br>don t be mad once you see that he want it<br>if you liked it then you shoulda put a ring on it oh oh oh',
'did you see that man in the limousine<br>with the pretty doll he is fifty and the girl s only seventeen<br>but she doesn t care and she never will<br>if he s ninetyfive she don t give a damn<br>just as long as he pays the bill<br>did you see that man with a fat cigar<br>he just left his lunch with a belly full of lobster and caviar<br>he can choose the wine from a vintage year<br>he will drink champagne in his limousine<br>where the rest of the street can peer<br> cause he s the man in the middle never second fiddle<br>just like a spider in a cobweb<br>hard as a hammer not the kind of boss you doublecross<br> cause he s the man in the middle knows the way to diddle<br>he s never bothered by his conscience<br>deals with the devil  cause he wants to be<br>man in the middle the middle the middle<br>in the middle <br>but you see that man made a big mistake<br>even though he s got all his servants and a mansion beside a lake<br>and the money too all that he can spend<br>he can buy the most nearly anything<br>but he can t buy the lot his friend',
'it s close to midnight <br>and something evil s lurking in the dark<br>under the moonlight <br>you see a sight that almost stops your heart<br><br>you try to scream<br>but terror takes the sound before you make it<br>you start to freeze <br>as horror looks you right between the eyes<br>you re paralyzed<br><br> cause this is thriller thriller night<br>and no one s gonna save you from the beast about to strike<br>you know it s thriller thriller night<br>you re fighting for your life inside a killer thriller tonight yeah<br><br>oh oh oh<br><br>you hear the door slam <br>and realize there s nowhere left to run<br>you feel the cold hand <br>and wonder if you ll ever see the sun<br><br>you close your eyes <br>and hope that this is just imagination<br>girl but all the while <br>you hear the creature creepin  up behind<br>you re out of time<br><br> cause this is thriller thriller night<br>there ain t no second chance against the thing with forty eyes girl<br>thriller thriller night<br>you re fighting for your life inside a killer thriller tonight<br><br>night creatures call<br>and the dead start to walk in their masquerade<br>there s no escapin  the jaws of the alien this time <br>this is the end of your life oh<br><br>they re out to get you <br>there s demons closing in on every side<br>they will possess you <br>unless you change that number on your dial<br><br>now is the time <br>for you and i to cuddle close together yeah<br>all through the night <br>i ll save you from the terrors on the screen<br>i ll make you see<br><br>that it s a thriller thriller night<br> cause i can thrill you more than any ghost would ever dare try<br>thriller thriller night<br>so let me hold you tight and share a killer diller <br>chiller thriller here tonight<br><br> cause it s a thriller thriller night<br>girl i can thrill you more than any ghost would ever dare try<br>thriller thriller night<br>so let me hold you tight and share a killer diller<br><br>i m gonna thrill you tonight<br>darkness falls across the land<br>the midnight hour is close at hand<br>creatures crawl in search of blood<br>to terrorize y awl s neighborhood<br>and whosoever shall be found<br>without the soul for getting down<br>must stand and face the hounds of hell<br>and rot inside a corpse s shell<br><br>i m gonna thrill you tonight<br>thriller ohh baby <br>i m gonna thrill you tonight <br>thriller all night oh baby<br>i m gonna thrill you tonight<br>thriller thriller night <br>i m gonna thrill you tonight<br>thriller all night <br>thriller night <br><br>the foulest stench is in the air<br>the funk of forty thousand years<br>and grizzly ghouls from every tomb<br>are closing in to seal your doom<br>and though you fight to stay alive<br>your body starts to shiver<br>for no mere mortal can resist<br>the evil of the thriller',
'yesterday all my troubles seemed so far away<br>now it looks as though they re here to stay<br>oh i believe in yesterday<br><br>suddenly i m not half the man i used to be<br>there s a shadow hanging over me<br>oh yesterday came suddenly<br><br>why she had to go i don t know she wouldn t say<br>i said something wrong now i long for yesterday<br><br>yesterday love was such an easy game to play<br>now i need a place to hide away<br>oh i believe in yesterday<br><br>why she had to go i don t know she wouldn t say<br>i said something wrong now i long for yesterday<br><br>yesterday love was such an easy game to play<br>now i need a place to hide away<br>oh i believe in yesterday<br>mm mm mm mm mm mm mm',
'now i ve been looking for someone<br>trying to find the right boy to wear on my arm<br>i must admit it<br>you simply fit it<br>you were like a cut from the rest<br>that s why you re winning <br>every night when<br>i close my eyes i can see you<br>my perfect type<br>and i never really thought my dreams would come true<br>until i laid eyes on you<br> cause you know you are<br>boyfriend material<br>boyfriend material<br>that s what you re made of<br>it s written on your label<br>boyfriend material ma ma material<br>want everyone to know your my<br>boyfriend material<br>boyfriend material <br>boyfriend material<br>ma ma material<br>want everyone to know that<br>you and your perfect smile<br>are both timeless and never going out of style<br>there s so many reasons you got it together<br>when i m catching feelings<br>you make me look better <br>every night when<br>i close my eyes i can see you<br>my perfect type<br>and i never really thought my dreams would come true<br>until i laid eyes on you<br> cause you know you are<br>boyfriend material<br>boyfriend material<br>that s what you re made of<br>it s written on your label<br>boyfriend material ma ma material<br>want everyone to know your my<br>boyfriend material<br>boyfriend material <br>boyfriend material<br>ma ma material<br>want everyone to know<br>oh there ain t any other<br>it s all the little things<br>that you do make me wanna sing yeah yeah<br>there ain t any other<br>the way you re talking to me i can tell you ve been listening<br>to everything<br>and maybe it s the butterflies<br>i get every time i hear your ringtone <br>and maybe it s  cause every single text boy<br>i told myself you were the one yeah yeah<br>boyfriend material<br> cause i know you re boyfriend material<br>boyfriend material<br>that s what you re made of<br>it s written on your label<br>boyfriend material ma ma material<br>want everyone to know your my<br>boyfriend material  boyfriend material<br>that s what you re made of it s written on your label<br>boyfriend material ma ma material<br>want everyone to know you re my<br>boyfriend material<br>boyfriend material<br>boyfriend material<br>ma ma material<br>want everyone to know that'
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
