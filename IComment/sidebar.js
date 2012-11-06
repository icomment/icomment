//siderbar
/*
var sidebarOpen = false;
function toggleSidebar() {
	if(sidebarOpen) {
		var el = document.getElementById('mySidebar');
		el.parentNode.removeChild(el);
		sidebarOpen = false;
	}
	else {
		var sidebar = document.createElement('div');
		sidebar.id = "mySidebar";
		sidebar.innerHTML = "\
			<h1>Hello</h1>\
			World!\
		";
		sidebar.style.cssText = "\
			position:fixed;\
			top:0px;\
			left:0px;\
			width:30%;\
			height:100%;\
			background:white;\
			box-shadow:inset 0 0 1em black;\
			z-index:999999;\
		";
		document.body.appendChild(sidebar);
		sidebarOpen = true;
	}
}
toggleSidebar();//open it when init
*/


  var sidebar;
  $('body').css({
    'padding-right': '250px'
  });

  sidebar =  $("<div id='icSidebar'> </div>");

  sidebar.css({
    'position': 'fixed',
    'right': '0px',
    'top': '0px',
    'z-index': 9999,
    'width': '250px',
    'height': '100%',
    'background-color': '#ddd'// Confirm it shows up
  });
 
  $('body').append(sidebar);

  $("#icSidebar").html("<div id='chat'>"
  		+"<div id='nickname'>"
	      +"<form id='set-nickname' class='wrap'>"
	        +"<p>Please type in your nickname and press enter.</p>"
	        +"<input id='nick'>"
	        +"<p id='nickname-err'>Nickname already in use</p>"
	      +"</form>"
	    +"</div>"
	    +"<div id='connecting'>"
	      +"<div class='wrap'>Connecting to socket.io server</div>"
	    +"</div>"
	    +"<div id='messages'>+"
	      +"<div id='nicknames'><span>Online:</span></div>"
	      +"<div id='lines'></div>"
	    +"</div>"
	    +"<form id='send-message'>"
	      +"<input id='message'>"
	      +"<button>Send</button>"
	    +"</form>"
	  +"</div>")

console.log('append siderbar')

