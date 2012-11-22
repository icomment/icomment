// Sexy Tools Textarea jQuery

$(function(){
    $("textarea.icSiderBar-default").each(function(index){
    // HTML Structure
        /*
            <div class='textarea-container'>
                <div class='textarea-top'><div class='top-left'></div><div class='top-center'></div><div class='top-right'></div></div>
                <div class='textarea-center'>
                    <div class='center-left'></div>
                    <div class='center-center'>
                        <textarea class='default' style='width:580px;height:180px;'></textarea>
                    </div>
                    <div class='center-right'></div>
                </div>
                <div class='textarea-bottom'><div class='bottom-left'></div><div class='bottom-center'></div><div class='bottom-right'></div></div>
            </div>
        */

    // Wrap The Textarea
    $("textarea.icSiderBar-default").wrap("<div class='textarea-container'>").after("</div>");
    $("textarea.icSiderBar-default").wrap("<div class='textarea-center'>").after("</div>");
    $("textarea.default").wrap("<div class='center-center'>").after("</div>");
    $(".center-center").before("<div class='center-left'></div>").after("<div class='center-right'></div>");
    $(".textarea-center").before("<div class='textarea-top'><div class='top-left'></div><div class='top-center'></div><div class='top-right'></div></div>");
    $(".textarea-center").after("<div class='textarea-bottom'><div class='bottom-left'></div><div class='bottom-center'></div><div class='bottom-right'></div></div>");

    // Adjust widths based on textarea width
    $(this).each(function(index) {
        var textareaWidth = $(this).width();
        $(this).closest(".textarea-container").css({ "width": textareaWidth + 36 });
        $(this).closest(".textarea-container").children().children(".top-center, .bottom-center, .center-center").css({ "width": textareaWidth + 20 });
        $(this).closest(".textarea-container").children(".textarea-container, .textarea-top, .textarea-bottom, .textarea-bottom").css({ "width": textareaWidth + 36 });
    });

    // Adjust heights based on textarea height
    $(this).each(function(index) {
        var textareaHeight = $(this).height();
        $(this).closest(".textarea-container").children().children(".center-left, .center-center, .center-right").css({ "height": textareaHeight +20 });
    });

    // Add the class focus
    $(this).focus(function () {
        $(this).addClass("focus");
        $(this).closest(".textarea-container").addClass("focus");
    });
    // Remove the class focus on blur
    $(this).blur(function () {
        $(this).removeClass("focus");
        $(this).closest(".textarea-container").removeClass("focus");
    });

 })
});
console.log('append textArea')