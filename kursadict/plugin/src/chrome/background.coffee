chrome.contextMenus.create
  title: "Oza '%s' sátnegirjjis",
  contexts: ["page", "selection"]
  onclick: (info, tab) ->
    notification = webkitNotifications.createHTMLNotification(
      "http://testing.oahpa.no/kursadict/notify/sme/nob/#{info.selectionText}.html",
    )
    notification.show()
 
