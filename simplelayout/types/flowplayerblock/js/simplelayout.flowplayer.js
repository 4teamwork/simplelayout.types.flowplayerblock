$(function() {
    $(".simplelayout-content:first").bind('refreshed',function(e, $el){
        initFlowpalyer($el);
    });
});