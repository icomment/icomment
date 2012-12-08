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

  sidebar =  $("<div id='icSideBar' class='icSideBarCls'> </div>");

  sidebar.css({
    'position': 'fixed',
    'right': '0px',
    'top': '0px',
    'z-index': 9999,
    'width': '240px',
    'height': '100%',
    'background': 'transparent',
    'display':'none'
  });
 
  $('body').append(sidebar);

logoImgSrc = chrome.extension.getURL("logo.png"); 

//+"<span id='loginBtn'> LoginFB <span/>"
//	    
  $("#icSideBar").html("<div id='icSideBar-chat'>"
  		+"<div id='icSideBar-logobar'>"
  			+"<div id='icSideBar-logo'>"
  				+"<img src='"+logoImgSrc+"' />"
  			+"</div>"
  			+"<div id='icSideBar-login'>"
  				+"<button id='icSideBar-loginBtn' >Login</button>"
  			+"</div>"
  		+"</div>"

  		+"<div id='icSideBar-content'>"


			+"<div id='icSideBar-nickname'>"

		      +"<form id='icSideBar-set-nickname' class='wrap'>"
		        +"<p>Type your nickname.</p>"
		        +"<input id='icSideBar-nick'> <br>"
				
		        +"<button id='icSideBar-cancelLoginBtn'> Back </button><button id='icSideBar-doLoginBtn'> Enter </button>"
		        +"<p id='icSideBar-nickname-err'>Nickname already in use</p>"
		      +"</form>"
		    +"</div>"
		    +"<div id='icSideBar-connecting'>"
		      +"<div class='wrap'>Connecting to socket.io server</div>"
		    +"</div>"
		    +"<div id='icSideBar-messages'>"
		      +"<div id='icSideBar-nicknames'><span>Online:</span></div>"
		      +"<div id='icSideBar-lines'></div>"
		    +"</div>"
		    +"<a id='icSideBar-btnShowMore' href='javascript:void()'> Show More</a>"
		    +"<form id='icSideBar-send-message'>"
		      
		      +"<textarea id='icSideBar-message' class='icSiderBar-default' style='width:234px;height:80px;'></textarea>"
		      +"<button id='icSideBar-sendMsgBtn'>Send</button>"
		    +"</form>"
		+"<div>"
	  +"</div>")

//<input id='icSideBar-message'>

console.log('append siderbar')

