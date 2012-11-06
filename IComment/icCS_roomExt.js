//iComment content scripts JS
//Author : Lei Tang

//Define: the extra methods of iCommentRoom which utilizes chrome spec funcions
var chromePort;
var roomID;

function message (from, msg) {
    $('#lines').append($('<p>').append($('<b>').text(from), msg));
}
function clear () {
    $('#message').val('').focus();
};

$(document).ready(function () {
	console.log('01 Page Doc loading compelete');
	//alert('load');
/*
chrome.extension.sendMessage({greeting: "hello"}, function(response) {
  console.log(response.farewell);
});
*/
	chromePort = chrome.extension.connect(); // this will auto trigger the action of joining the room 
	var port =chromePort;

	console.log("02 init conn-ext => join room");
	
	//check whether user has finish login action
	port.postMessage({type:"checkLogin"});


	port.onMessage.addListener(function(evt){
		//console.log("message passing to contentscripts, Evt:"+evt.type)
		if (evt.type=="recvMessage"){
			message(evt.data.from,evt.data.msg)
			console.log("msg:" +evt.data.msg )

		}else if (evt.type=="joinRoom"){
			roomID = evt.data;
			$('#chat').addClass('connected');

		}else if (evt.type=="announcement"){	
    		$('#lines').append($('<p>').append($('<em>').text(evt.data)));
	
		}else if (evt.type=="refreshUserList"){

			nicknames = evt.data;
		    $('#nicknames').empty().append($('<span>Online: </span>'));
		    for (var i in nicknames) {
		    $('#nicknames').append($('<b>').text(nicknames[i]));
		    }

		}else if(evt.type=="checkLogin"){
			if(evt.data==true){
				//user has login, remove set nickname form
				$('#chat').addClass('nickname-set');
				clear();
			}

		}

	})

	// DOM manipulation
	$(function () {

		//only allow user login once on any chatting page 
	    $('#set-nickname').submit(function (evt) {
	        evt.preventDefault();
	        port.postMessage({type:"login",data: $('#nick').val()})

	        LocalUserName = $('#nick').val();
   			clear();

   			//change chat page view 
   			$('#chat').addClass('nickname-set');

	        //todo add error test
/*
	        .emit('nickname', $('#nick').val(), function (set) {
	            if (!set) {
	                clear();
	                return $('#chat').addClass('nickname-set');
	            }
	            $('#nickname-err').css('visibility', 'visible');
	        });
*/

	        return false;
	    });

	    $('#send-message').submit(function (evt) {
	    	evt.preventDefault();   	
	    	//show on sender's page
		    message('me', $('#message').val());

		    //post to server side
		    port.postMessage({type:"newMessage",data: {msg:$('#message').val(),roomID:roomID} } )
    		clear();
/*		   	
		    socket.emit('user message', $('#message').val());
		    clear();
		    
*/
			$('#lines').get(0).scrollTop = 10000000;

		    return false;
	    });


	});


});

