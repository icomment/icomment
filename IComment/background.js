//iComment background.html (JS)
//Author : Lei Tang


//------init socket IO--------
//Define socket related ======
WEB_SOCKET_DEBUG = true;

// socket.io specific code
//wsHost= "http://localhost:8080" //server& socket port


url_re =/[a-zA-z]+:\/\/([^s]*)/

//wsHost= "http://192.168.1.101:8080" //server& socket port
//wsHost="http://127.0.0.1:8080"
wsHost ="http://50.19.165.203:80"



var socket = io.connect(wsHost);
var isServerOpen=false;



//=== socket passive handlers==========

//if default onConnect evt of socket trigger
socket.on('connect', function () {
    isServerOpen = true;
    console.log("socketIO conn")
});

socket.on('announcement',function (roomID,msg) {
    console.log("recv annoucement")
    var port = icBG.r2p[roomID];
    port.postMessage({type:"announcement",data:msg})
  
});

socket.on('nicknames', function (roomID,nicknames) {
    console.log("recv nicknames")
    var port = icBG.r2p[roomID];
    port.postMessage({type:"refreshUserList",data:nicknames})

});

socket.on('msg_to_room', function (roomID,from,msg) {
    console.log("recv msg2room" )
    var port = icBG.r2p[roomID];
    port.postMessage({type:"recvMessage",data:{from:from, msg:msg} })

});

//Todo fix these three functions
socket.on('reconnect', function () {
    console.log("reconnect to server side!")
    //alert('reconnect')
    //$('#lines').remove();
    //message('System', 'Reconnected to the server');
});

socket.on('reconnecting', function () {
    //alert('reconnecting')
    //message('System', 'Attempting to re-connect to the server');
});

socket.on('error', function (e) {
     alert('System', e ? e : 'A unknown error occurred, server may be not running!')
    //message('System', e ? e : 'A unknown error occurred');
});


//=========================================================
//Define the functions that manage all the tabs/rooms 

var icBG={};

//r2t is roomID to tabID
icBG.r2t={}; 
icBG.t2r={};

//t2p is tabID to port map
icBG.t2p={}; 

//r2t is roomID to related port map
icBG.r2p={}

//t2r is roomID to related port map


icBG.isLogin=false;
icBG.username= undefined; 

/*
chrome.extension.onMessage.addListener(
  function(request, sender, sendResponse) {
    console.log(sender.tab ?
                "from a content script:" + sender.tab.url :
                "from the extension");
    if (request.greeting == "hello")
      sendResponse({farewell: "goodbye"});
  });
console.log('add listener in bg')
*/

function encodeURL2RoomID(url){
  //processing url and return a md5
  
  //remove protocol type of web url
  url_re.test(url)

  var roomID = CryptoJS.MD5(RegExp.$1).toString(CryptoJS.enc.Hex);
  console.log(roomID);
	return roomID
}

 
/* Evt Listener:
  after a new webpage(in the specified domain ) opened in the tab, it trigger this evt to 
    1 record new url, and its port
    2 tell server that it need join that url chat room
    3 define the handler to 
*/
function onConnHandler(port){  
  	console.log('onConnHandler newtab-> sendID:'+port.sender.id+ ',tabID:'+port.sender.tab.id);
    if (isServerOpen ==false) {
      console.log("error: page conn fail due to server status");
      return ;
    }

  	var url = port.sender.tab.url;
    console.log("onConn 2 url:"+url)

  	var roomID= encodeURL2RoomID(url); //roomID should be a md5

    //1 record 
  	icBG.r2t[roomID]=port.sender.tab.id; //TO fix ,if allow 1url --> n tabs
    icBG.t2r[port.sender.tab.id] = roomID;

    icBG.t2r[port.sender.tab.id] = port
  	icBG.r2p[roomID]=port;

    //2 send join room request
    socket.emit('join', url,roomID, function (data) {
        console.log("test return para:"+data)
        
        //onConn room
        port.postMessage({type:"joinRoom",data:roomID});// show connected
    });


    //3 handlers to recv messages from  contentscripts 
    port.onMessage.addListener(function(evt) {

    	if(evt.type == "login"){
        //the login evt only happen once 
        if(icBG.isLogin ==false){
          socket.emit('nickname', evt.data,roomID);

          //todo if login false, or change to SNS account
          icBG.isLogin =true;
          icBG.username = evt.data;

        }      
    	}else if(evt.type == "newMessage"){
        console.log("send newMessage in room:"+evt.data.roomID);
    		socket.emit('user message', evt.data.msg, url); //evt.data.roomID);
    	
      }else if(evt.type == "checkLogin"){
          
        port.postMessage({type:"checkLogin",data:icBG.isLogin})
      }
    });

}
chrome.extension.onConnect.addListener(onConnHandler);



chrome.tabs.onRemoved.addListener(function(tabId,removeInfo) {
    var roomID = icBG.t2r[tabId];
    if(roomID !== undefined){
      socket.emit("leave",roomID)
    }
      

});

//the global socket connected


