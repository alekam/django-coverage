$("#authors a").on('click', function(e){
    var _self = $(this);
    if (_self.hasClass("selected")) {
        return false;
    } else {
        $("#authors a").removeClass("selected");
        _self.addClass("selected");

        var author = _self.html();
        if (author == "全部") {
            $("#source-listing li").removeClass("gray");
        } else {
            $("#source-listing li").addClass("gray");
            $("#source-listing li:contains('" + author + "')").removeClass("gray");
        }
    }
});

