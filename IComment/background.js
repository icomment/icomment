//iComment background.html (JS)
//Author : Lei Tang


//------init cfg -------
var WEB_SOCKET_DEBUG = true;
var isServerOpen=false;
// socket.io specific code

//wsHost= "http://localhost:8080" //server& socket port

var wsHost ="http://50.19.165.203:8000"
//var wsHost="http://127.0.0.1:8080";

var url_re =/[a-zA-z]+:\/\/(\S+)/ ;
var CNN_Url_Reg= /[a-zA-Z]+:\/\/(\w+\.)+cnn\.com\/20[0-1][0-9]\/[0-1][0-9]\/[0-3][0-9]\/\w+/ ;
//match http://www.cnn.com/2012/11/21/showbiz/celebrity-news-gossip/celebrity-thanksgiving-2012-gallery/index.html?hpt=en_c1



//===> Define the functions that manage all the tabs/rooms 
var icBG={}; // icommentBackground

icBG.r2t={}; //r2t is roomID to tabID
icBG.t2r={}; //t2p is tabID to roomID

icBG.t2p={}; //r2t is roomID to related port map
icBG.r2p={}; //t2r is roomID to related port map

icBG.isLogin=false;
icBG.username= undefined; 



//00 setup websocket conn at the very beginning, if this extension is enabled
var socket = io.connect(wsHost);

//bind onConn 
chrome.extension.onConnect.addListener(onConnHandler);

function formatURL(url){
  url_re.test(url); //remove protocol type 
  return RegExp.$1
}

function encodeURL2RoomID(url){
  return CryptoJS.MD5(url).toString(CryptoJS.enc.Hex);  //processing url and return a md5  
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

    var tabUrl = port.sender.tab.url;

    console.log("tabUrl="+tabUrl);
    var url = formatURL(tabUrl);    

    console.log("onConn 2 url:"+url)

    var roomID= encodeURL2RoomID(url); //roomID should be a md5

    //1 record 
    icBG.r2t[roomID]=port.sender.tab.id; //TO fix ,if allow 1url --> n tabs
    icBG.t2r[port.sender.tab.id] = roomID;

    icBG.t2r[port.sender.tab.id] = port;
    icBG.r2p[roomID]=port;

    //2 send join room request
    socket.emit('join',url,roomID, function (data) {
        //console.log("test return para:"+data)
        
        //onConn room
        port.postMessage({type:"joinRoom",data:roomID});// show connected
    });
    // Log out request


    //3 handlers to recv messages from  contentscripts 

    port.onMessage.addListener(function(evt) {

      if(evt.type == "login"){
        //the login evt only happen once 
        console.log("recieve login")
        if(icBG.isLogin ==false){
          socket.emit('nickname', evt.data,roomID);

          //todo if login false, or change to SNS account
          icBG.isLogin =true;
          icBG.username = evt.data;
          console.log("trigger login")

        }      
      }else if(evt.type == "newMessage"){
        console.log("send newMessage in room:"+evt.data.roomID);
        socket.emit('user message', evt.data.msg, evt.data.roomID); //v0.2 IF pass msg,rID to server 
      
      }else if(evt.type == "checkLogin"){
          
        port.postMessage({type:"checkLogin",data:icBG.isLogin})
      }else if(evt.type == "logout"){

          icBG.isLogin =false;
          console.log("trigger logout")
          socket.emit("leave",roomID)
        //port.postMessage({type:"refreshUserList",data:nicknames})

      }
    });

}

//01 programmatic injection
//any new created/updated tab page will check whether match our filter, 
//if passed & server is open, we inject our content scripts(css+js) into original webpage
chrome.tabs.onUpdated.addListener(function( tabId,  changeInfo, tab) {
    var tabUrl = tab.url;
 
    if (tabUrl == undefined || changeInfo.status != "complete") {
        return ;
    }
    if(CNN_Url_Reg.test(tabUrl)){      // pass reg scan
      
      if ( isServerOpen){
        chrome.tabs.executeScript(tabId, { file: "jqmin.js" }, function() { 
          chrome.tabs.insertCSS(tabId, { file: "icCS.css" });
          chrome.tabs.executeScript(tabId, { file: "sidebar.js" });
          chrome.tabs.executeScript(tabId, { file: "jq_sexy_textarea.js" });
          chrome.tabs.executeScript(tabId, { file: "icCS_roomExt.js" });                                   

        }); 

      }else{
        console.log("Need not do Content Scripts injection, server is down!") 
      }
    }
});

chrome.tabs.onRemoved.addListener(function(tabId,removeInfo) {
    var roomID = icBG.t2r[tabId];
    if(roomID !== undefined){
      socket.emit("leave",roomID)
    }
      

});





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
    console.log("recv nicknames"+nicknames)
    var port = icBG.r2p[roomID];
    port.postMessage({type:"refreshUserList",data:nicknames})

});

socket.on('msg_to_room', function (roomID,from,msg) {
    console.log("recv msg2room" )
    
    var port = icBG.r2p[roomID];
    port.postMessage({type:"recvMessage",data:{from:from, msg:msg} })

});


socket.on('history', function (msgList,roomID) {
    console.log("msgList:"+msgList )

    var port = icBG.r2p[roomID];
    port.postMessage({type:"recvHistoryMsg",data: JSON.parse(msgList) })

});

//Todo fix these three functions
socket.on('reconnect', function () {
    console.log("reconnect to server side!")

});

socket.on('reconnecting', function () {
    //alert('reconnecting')
    //message('System', 'Attempting to re-connect to the server');
});

socket.on('error', function (e) {
     console('System error:A unknown error occurred, server may be not running!')
    //message('System', e ? e : 'A unknown error occurred');
});


//=========================================================






