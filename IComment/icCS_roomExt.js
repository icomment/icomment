//iComment content scripts JS
//Author : Lei Tang

//Define: the extra methods of iCommentRoom which utilizes chrome spec funcions
var chromePort;
var roomID;
var isUserEnterRoom=false;
var isShowingLoginWin=false;

//Dom-ID assign
var icRoom={};
var idp = icRoom._idPool={};
idp.container	='#icSideBar';
idp.IDBase		=idp.container+'-';
idp.room 		=idp.IDBase+'chat';

idp.currMsg 	= idp.IDBase+'message';
idp.userList 	= idp.IDBase+'nicknames';
idp.msgBoard 	= idp.IDBase+'lines';
idp.nickName 	= idp.IDBase+'nick';

idp.loginBtn 	= idp.IDBase+'loginBtn';
idp.cancelLoginBtn =idp.IDBase+'cancelLoginBtn'
idp.setNameForm = idp.IDBase+'set-nickname';
idp.sendMsgForm = idp.IDBase+'send-message';


function message (from, msg) {
	var msgList = msg.split('\n');
		//$('<span>').text(msg);
		//$(idp.msgBoard).append(
    var pList=[];// $('<p>');
    	pList.push($('<b>').text(from+': '),'<br>' );
    if( msgList.length<1){
    	pList.push($('<z>').text(msgList[0]))
   	}else{
   		var i=0;
   		for(;i<msgList.length-1;i++){
    		pList.push($('<z>').text(msgList[i]),'<br>' );
    		
    	}
    	pList.push($('<z>').text(msgList[i]) );
    }
    $(idp.msgBoard).append($('<p>').append(pList) );
    //p.innerText +=msgList[0];

}
function clear () {
    $(idp.currMsg).val('').focus();
};

function userWatchRoom(){
	isUserEnterRoom=false;
	isShowingLoginWin=false;
	$(idp.room).removeClass('tryLogin')
	$(idp.room).addClass('notLogin');

	console.log('userWatchRoom');
}
function userTryEnterRoom(){
	isShowingLoginWin=true;
	$(idp.room).removeClass('notLogin')
   	$(idp.room).addClass('tryLogin')

   	console.log('tryEnterRoom');
}
function userEnterRoom(){
	isUserEnterRoom=true;
	isShowingLoginWin=false;
	$(idp.room).removeClass('notLogin');
	$(idp.room).removeClass('tryLogin');

	$(idp.room).addClass('nickname-set');

	clear();
	//change login btn
	$(idp.loginBtn).text('Hi~')	
	console.log('userEnterRoom');
}


//---------init when load whole DOM--------
$(document).ready(function () {
	console.log('01 Page DOM load compeletely');

	//default action
	$(idp.container).css('display','block'); 	//turn one and show
	userWatchRoom();							//close some views
	//renderTextArea();							//re-render textarea

 	//when docInit, make this content script connected to background.js 
 	// this will auto trigger the action of joining the room 
	chromePort = chrome.extension.connect(); 
	var port =chromePort;

	console.log("02 init conn-ext => try to join room");
	
	//check whether user has finish login action
	port.postMessage({type:"checkLogin"});


	port.onMessage.addListener(function(evt){
		//console.log("message passing to contentscripts, Evt:"+evt.type)
		if (evt.type=="recvMessage"){
			message(evt.data.from,evt.data.msg)
			console.log("msg:" +evt.data.msg )

		}else if (evt.type=="joinRoom"){
			roomID = evt.data;

			console.log("join room succ");
			$(idp.room).addClass('connected');

		}else if (evt.type=="announcement"){	
    		$(idp.msgBoard).append($('<p>').append($('<em>').text(evt.data)));
	
		}else if (evt.type=="refreshUserList"){

			nicknames = evt.data;
		    $(idp.userList).empty().append($('<span>Online: </span>'));
		    for (var i in nicknames) {
		    	$(idp.userList).append($('<b>').text(nicknames[i]));
		    }

		}else if(evt.type=="checkLogin"){
			if(evt.data==true){				
				userEnterRoom();
			}else{
				userWatchRoom();
			}

		}

	})

	// bimd DOM based actions&listeners
	$(function () {

		//only allow user login once on any chatting page 
		$(idp.loginBtn).click(function (evt) {
	    	evt.preventDefault();   	
    		if(!isUserEnterRoom && !isShowingLoginWin){
				userTryEnterRoom();
    		}
		    return false;
	    });

		$(idp.cancelLoginBtn).click(function (evt) {
	    	evt.preventDefault();   	
    		if(!isUserEnterRoom && isShowingLoginWin){
				userWatchRoom();
    		}
		    return false;
	    });

		//triggered by clicking doLoginBtn('Enter') or pressing EnterKey in LoginWin 
	    $(idp.setNameForm).submit(function (evt) {
	        evt.preventDefault();


	        LocalUserName = $(idp.nickName).val();
	        port.postMessage({type:"login",data: LocalUserName })

   			clear();

   			//ToFix if login action fail -> add error process
   			//change chat page view 
   			$(idp.room).addClass('nickname-set');
   			userEnterRoom();
	        return false;
	    });

	    $(idp.sendMsgForm).submit(function (evt) {
	    	evt.preventDefault();   	
	    	//show on sender's page
			var currMsg =$(idp.currMsg).val();
			//don't send empty msg
			if($.trim(currMsg)==''){
	    		return false;
	    	}
 			message('me', currMsg);

		    //post to server side
		    port.postMessage({
		    	type:"newMessage",
		    	data: {msg:currMsg,roomID:roomID} 
		    })
    		clear();
/*		   	
		    socket.emit('user message', $('#message').val());
		    clear();
		    
*/
			$(idp.msgBoard).get(0).scrollTop = 10000000;

		    return false;
	    });


	});


});

