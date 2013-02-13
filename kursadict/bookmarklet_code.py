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
    var NDS_API_HOST    = 'http://sanit.oahpa.no' ;

    var nds_css      = document.createElement('link');
        nds_css.href = NDS_API_HOST + '/static/css/jquery.neahttadigisanit.css';
        nds_css.rel  = 'stylesheet' ;

    var nds_book      = document.createElement('script');
        nds_book.type = 'text/javascript';
        nds_book.src  = NDS_API_HOST + '/static/js/bookmarklet.min.js' ;

    window.NDS_API_HOST = NDS_API_HOST ;
    if (window.location.hostname == "skuvla.info" && window.frames.length > 0) {
        var d;
        d = window.frames[1];
        d.window.NDS_API_HOST = window.NDS_API_HOST
        d.document.getElementsByTagName('head')[0].appendChild(nds_css);
        d.document.getElementsByTagName('body')[0].appendChild(nds_book);
    } else {
        document.getElementsByTagName('head')[0].appendChild(nds_css) ;
        document.getElementsByTagName('body')[0].appendChild(nds_book) ;
    }
})();
"""

# This is the end product of minifying the above, but note that some of
# this code will need to be urlencoded if support for older browsers is
# desired.
bookmarklet_minified = """(function(){var e="http://sanit.oahpa.no";var t=document.createElement("link");t.href=e+"/static/css/jquery.neahttadigisanit.css";t.rel="stylesheet";document.getElementsByTagName('head')[0].appendChild(t);var n=document.createElement("script");n.type="text/javascript";n.src=e+"/static/js/bookmarklet.min.js";window.NDS_API_HOST=e;document.getElementsByTagName('body')[0].appendChild(n)})()"""

bookmarklet_minified = """(function(){var e="http://sanit.oahpa.no";var t=document.createElement("link");t.href=e+"/static/css/jquery.neahttadigisanit.css";t.rel="stylesheet";var n=document.createElement("script");n.type="text/javascript";n.src=e+"/static/js/bookmarklet.min.js";window.NDS_API_HOST=e;if(window.frames.length==0){document.getElementsByTagName("head")[0].appendChild(t);document.getElementsByTagName("body")[0].appendChild(n)}else{var r,i,s,o;o=window.frames;for(i=0,s=o.length;i<s;i++){r=o[i];r.document.getElementsByTagName("head")[0].appendChild(t);r.document.getElementsByTagName("body")[0].appendChild(n)}}})()"""

# This is because older browsers sometimes have issues with longer
# bookmarks; it may be that this plugin is also not supported on those
# browsers, but just in case...
# http://meyerweb.com/eric/tools/dencoder/

# this version works, but developing new ones...
bookmarklet_escaped = """(function()%7Bvar%20e%3D%22http%3A%2F%2Fsanit.oahpa.no%22%3Bvar%20t%3Ddocument.createElement(%22link%22)%3Bt.href%3De%2B%22%2Fstatic%2Fcss%2Fjquery.neahttadigisanit.css%22%3Bt.rel%3D%22stylesheet%22%3Bdocument.getElementsByTagName('head')%5B0%5D.appendChild(t)%3Bvar%20n%3Ddocument.createElement(%22script%22)%3Bn.type%3D%22text%2Fjavascript%22%3Bn.src%3De%2B%22%2Fstatic%2Fjs%2Fbookmarklet.min.js%22%3Bwindow.NDS_API_HOST%3De%3Bdocument.getElementsByTagName('body')%5B0%5D.appendChild(n)%7D)()"""

bookmarklet_escaped = """(function()%7Bvar%20e%3D%22http%3A%2F%2Fsanit.oahpa.no%22%3Bvar%20t%3Ddocument.createElement(%22link%22)%3Bt.href%3De%2B%22%2Fstatic%2Fcss%2Fjquery.neahttadigisanit.css%22%3Bt.rel%3D%22stylesheet%22%3Bvar%20n%3Ddocument.createElement(%22script%22)%3Bn.type%3D%22text%2Fjavascript%22%3Bn.src%3De%2B%22%2Fstatic%2Fjs%2Fbookmarklet.min.js%22%3Bwindow.NDS_API_HOST%3De%3Bif(window.location.hostname%3D%3D%22skuvla.info%22%26%26window.frames.length%3E0)%7Bvar%20r%3Br%3Dwindow.frames%5B1%5D%3Br.window.NDS_API_HOST%3Dwindow.NDS_API_HOST%3Br.document.getElementsByTagName(%22head%22)%5B0%5D.appendChild(t)%3Br.document.getElementsByTagName(%22body%22)%5B0%5D.appendChild(n)%7Delse%7Bdocument.getElementsByTagName(%22head%22)%5B0%5D.appendChild(t)%3Bdocument.getElementsByTagName(%22body%22)%5B0%5D.appendChild(n)%7D%7D)()"""

prod_host = "sanit.oahpa.no"
demo_host = "localhost%3A5000"


