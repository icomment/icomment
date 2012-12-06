====IComment Client====

$1 Intro
Client part of this project works as a google's chrome extension. If you are not familar with this and wanna take a quick tour, please spend 15~30 on this video(http://www.youtube.com/watch?v=sO1FujZDT0s). 

Essentially speaking, most of chrome extesion it-self is no more than plain HTML+CSS+JS. They do all their job as client side webpages but run in chrome's process. Normally these extensions will not occupy your screen room of your browser as they only serve certain purposes that common webpages can't do. 

There are two main categorys of them: one is designed to enhance some specific functions and behaviors of chrome browser by calling its intneral API; the other may work as mini app which bring you the convenience to perform some of your frequent online behavior, like checking gmails. And our project is more belong the second kind, which enable some readers on the same page to disscus freely if they want.

$2 Installation
Well, you need a chrome browser, and if you already have one but haven't update it for a looooong time you should check your chrome version(from "About google chrome" ). We need at least version 17 to run our extension since the manifest v2 may not work well in prior chrome (http://developer.chrome.com/extensions/manifest.html#manifest_version).

Method 1:
Use install our packed "*.crx" file:
	Try to double click it. It may work if the associated file process on you computer is pointed to the chrome. Otherwise, start your chrome and open options/Tools/Extensions, then drag our '*.crx' file into the extension page and a promot will show up.
	Make sure you see iCommemt is enabled.
	By this means, when this chatting extenion works it would connect one of our public server whose IP/domain is predefined in the .crx package. And you need install this excat crx file into another chrome browser on the second machine(or VM) to do the communication test between two machine.

Method 2:
 	If you wanna dig into the code, you would prefer deploy the iComment system locally. And you need clone/download client IComment code, then start your chrome and open options/Tools/Extensions. You will see the "Load unpacked extension" button on the top right of extenstion page. Use it to select IComment clide code folder.But you still have to configue the right server IP for this client:
 		1 open background.js file
 		2 set wsHost="http://127.0.0.1:8080" if you plan to run the server in your localhost at port 8080
 		3 save this file, and return to extension page and click the "Reload" of iComment. (Anytime you change any code in your local env, you have to reload it to make chrome update it from local file.)


 	Note for Debug:
 		to debug background code, click 'generated_background_page.html' link of iComment on your extension page.
 		to debuy content script code, use default 'Inspect Element' in mouse rightclick's menu. (or instal firebug extension for your chrome)


$3 Target Pages
Because this is a page level client application, which means it only get showed at selected pages. 
The general setting of content scripts is to put the rule of filter at manifest.json-> content_scripts->matches. But due to the fact that goolge's match pattern is too simple to finish any advanced access restrication, we finially to decide to call the programmatic injection feature in order to use complex reg express to valicate the target pages from background.js.

So,you will find the current main url filter-CNN_Url_Reg in the background.js, and we listen to all chrome tab's update event. Thus if any target webpate get loaded, we can immediately find it and inject our js&css file into it. This injection code will share the same constraint as normal content scripts that defined in hte manifest.

And in a short word, only those CNN's article page may run and show our chatting components right now. 
	FE:
		[you can run it at]		http://whitehouse.blogs.cnn.com/2012/08/29/obama-vows-to-release-his-beer-recipe/
		[you cant run it at]	http://whitehouse.blogs.cnn.com/2012/08/29/


#4 Tech detail
Most of the necessary reference is all on the guide of chrome extension(http://developer.chrome.com/extensions/devguide.html). 

And if you are not familiar with two main js libs-Jquery & SocketIO, you may find their api/reference on their project page.




