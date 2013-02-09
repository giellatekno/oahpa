# TODO: minify and url-encode javascript:blah
# TODO: http://jsbeautifier.org/

# TODO: assuming loading of the above will be asynchronous, any way
# to make sure init triggers only when all the other aboves have
# loaded?
#
# TODO: test for jQuery and version, maybe add it if it doesn't
# exist in the page

# This code works if you copy paste it into the browser's console,
# however in order for it to work as a bookmarklet, it must be URL
# encoded.
bookmarklet = """
(function () {
    var NDS_API_HOST    = 'http://localhost:5000' ;
    
    var nds_css      = document.createElement('link');
        nds_css.href = NDS_API_HOST + '/static/css/jquery.neahttadigisanit.css';
        nds_css.rel  = 'stylesheet' ;

    document.head.appendChild(nds_css) ;
    
    var nds_book      = document.createElement('script');
        nds_book.type = 'text/javascript';
        nds_book.src  = NDS_API_HOST + '/static/js/bookmarklet.min.js' ;

    window.NDS_API_HOST = NDS_API_HOST ;
    document.body.appendChild(nds_book) ;
})();
"""

# This is the end product of minifying the above, but note that some of
# this code will need to be urlencoded if support for older browsers is
# desired.
bookmarklet_minified = """(function(){var e="http://sanit.oahpa.no";var t=document.createElement("link");t.href=e+"/static/css/jquery.neahttadigisanit.css";t.rel="stylesheet";document.head.appendChild(t);var n=document.createElement("script");n.type="text/javascript";n.src=e+"/static/js/bookmarklet.min.js";window.NDS_API_HOST=e;document.body.appendChild(n)})()"""

# This part should be url encoded and inserted within the following
# (function()HERE)()
# This is because older browsers sometimes have issues with longer
# bookmarks; it may be that this plugin is also not supported on those
# browsers, but just in case...
# http://meyerweb.com/eric/tools/dencoder/

bookmarklet_escaped = """(function()%7Bvar%20e%3D%22http%3A%2F%2Fsanit.oahpa.no%22%3Bvar%20t%3Ddocument.createElement(%22link%22)%3Bt.href%3De%2B%22%2Fstatic%2Fcss%2Fjquery.neahttadigisanit.css%22%3Bt.rel%3D%22stylesheet%22%3Bdocument.head.appendChild(t)%3Bvar%20n%3Ddocument.createElement(%22script%22)%3Bn.type%3D%22text%2Fjavascript%22%3Bn.src%3De%2B%22%2Fstatic%2Fjs%2Fbookmarklet.min.js%22%3Bwindow.NDS_API_HOST%3De%3Bdocument.body.appendChild(n)%7D)()"""

