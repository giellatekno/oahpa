###
A jQuery plugin for enabling the Kursadict functionality


## TODOs / Bugs

TODO: IE on all OSes seems to select a whole paragraph after a word has been
      selected. There is probably some way to prevent this from occurring.

TODO: IE sometimes still does not notice the first lookup

TODO: prevent window url from updating with form submit params

TODO: lookup timeout -- set on $.ajax, but sometimes seems not to work?

TODO: Opera on Windows - alt+click context window

###

# Wrap jQuery and add plugin functionality
jQuery(document).ready ($) ->

  # API_HOST = "http://testing.oahpa.no/"
  API_HOST = "http://localhost:5000/"

  Templates =
    OptionsMenu: (opts) ->
      # TODO: navmenu fixed at bottom containing language option, and 
      #       lookup button
      return "omg"
    
    OptionsTab: (opts) ->
      languageOption = (data, i) ->
        if i+1 == 1
          checked = "checked"
        else
          checked = ""

        """
        <label class="radio">
          <input type="radio" 
                 name="language_pair" 
                 id="language_pair#{i+1}" 
                 value="#{data.from.iso}#{data.to.iso}" #{checked}>
          #{data.from.name} -> #{data.to.name}
        </label>
        """
    
      el = $("""
      <div id="webdict_options" class="hidden">
        <div class="well">
        <a class="close" href="#" style="display: none;">&times;</a>
        <div class="trigger">
          <h1><a href="#" class="open">Á</a></h1>
        </div>

        <div class="option_panel" style="display: none;">
          <ul class="nav nav-pills">
            <li class="active">
              <a href="#" data-target="#options">Options</a>
            </li>
            <li><a href="#" data-target="#about">About</a></li>
          </ul>
          <div id="options" class="minipanel">
            <form class="">
              <label class="control-label" for="inputEmail">Ordbok</label>
              #{opts.dictionaries.map(languageOption).join('\n')}
              <button type="submit" class="btn" id="save">Save</button>
            </form>
          </div>
          <div id="about" style="display: none;" class="minipanel">
          <p>To look up a word, hold Alt (or Option/⌥ on Macs) and double click a word. If the popup disappears, either hover over the link that is created, or click anywhere on the screen, and then try again.</p>
          <p>To report problems, <a href="mailto:">contact us</a>.</p>
          </div>
        </div>
      </div>
      """)

      el.find('ul.nav-pills a').click (evt) ->
        target_element = $(evt.target).attr('data-target')
        el.find('ul.nav-pills a').parent('li').removeClass('active')
        $(evt.target).parent('li').addClass('active')
        el.find('div.minipanel').hide()
        el.find(target_element).show()
        return false

      el.find('.trigger').click () ->
        optsp = el.find('div.option_panel')
        optsp.toggle()
        el.find('a.close').toggle()

      el.find('a.close').click () ->
        optsp = el.find('div.option_panel')
        optsp.toggle()
        el.find('a.close').toggle()

      el.find('input[name="language_pair"][type="radio"]').click (e) ->
        store_val = $(e.target).val()
        DSt.set('kursadict-select-langpair', store_val)
        return true

      el.find('form').submit () ->
        optsp = el.find('div.option_panel')
        optsp.toggle()
        el.find('a.close').toggle()
        return false
      
      return el

    ErrorBar: (args) ->
      host = args.host
      el = $("""
       <div class="errornav navbar-inverse navbar-fixed-bottom">
         <div class="navbar-inner">
           <div class="container">
             <p><strong>Error!</strong> Could not connect to dictionary server (host: #{host}).
                <a href="#" class="dismiss">Close</a>.</p>
           </div>
         </div>
       </div>
       """)
      el.find('.errornav .dismiss').click () ->
        $(document).find('body .errornav').remove()
        return false
      return el

  initSpinner = (imgPath) ->
    ###
        spinner popup in right corner; `spinner = initSpinner()` to
        create or find, then usual `spinner.show()` or `.hide()` as
        needed.
    ###
    spinnerExists = $(document).find('.spinner')
    if spinnerExists.length == 0
      spinner = $("""<img src="#{imgPath}" class="spinner" />""")
      $(document).find('body').append(spinner)
      return spinner
    return spinnerExists


  ## Some global ajax stuff
  ##
  ## 

  $.ajaxSetup
    type: "GET"
    timeout: 10 * 1000
    beforeSend: (args) ->
      spinner = initSpinner()
      spinner.show()
    complete: (args) ->
      spinner = initSpinner()
      spinner.hide()
    dataType: "json"
    cache: true
    error: () =>
      $(document).find('body').find('.errornav').remove()
      $(document).find('body').append Templates.ErrorBar {
        host: API_HOST
      }


  getActualIndex = (selection) ->
    # Need to adjust the selection index when the user double clicks a
    # word, the selection index returned from the selection event is the
    # character at the point of the click, so, the text of the element
    # needs to be split.  The baseOffset is also the same as the
    # extentOffset.
    #

    [baseOffset, extentOffset] = selection.index
    # regex on _left slice to get length of word that is cut off
    # subtract length, return

    # Doubleclick
    if baseOffset == extentOffset
      _left = $(selection.element).html().slice(0, baseOffset)
      # TODO: hyphen
      last = _left.match /[^\s.]*$/
      if last[0] != ""
        return baseOffset - last[0].length
      else
        return baseOffset
    else
      return baseOffset

    return selection.index[0]
     
  cleanTooltipResponse = (selection, response, opts) ->
    ###
        Clean response from tooltip $.ajax query, and display results
    ###
    if not selection.index
      console.log("no index!")

    string   = selection.string
    element  = selection.element
    index    = getActualIndex(selection)
    indexMax = index + string.length

    # TODO: quick fix for IE, fix the selection event plugin instead
    if not index
      console.log "no index!!"
      index = $(selection.element).html().search(string)
      indexMax = index + string.length
    
    # For tooltip we need to wrap the search word in link, but going
    # based off of the index of the searched word to account for
    # multiple words.
    if opts.tooltip
      _wrapElement = """
      <a style="font-style: italic; border: 1px solid #CEE; padding: 0 2px" 
         class="tooltip_target">#{string}</a>
      """

      _elem_html = $(element).html()

      _left      = _elem_html.slice(0, index)
      _mid       = _elem_html.slice(index, indexMax)
      _right     = _elem_html.slice(indexMax)

      _mid_new   = _mid.replace(string, _wrapElement)
      _new_html  = _left + _mid_new + _right

      $(element).html _new_html

    # Compile result strings
    result_strings = []
    for result in response.result
      for lookup in result.lookups
        if lookup.right.length > 1
          clean_right = []
          for r, i in lookup.right
            clean_right.push "#{i+1}. #{r}"
          right = clean_right.join(', ')
        else
          right = lookup.right[0]

        result_string = "<em>#{lookup.left}</em> (#{lookup.pos}) &mdash; #{right}"
        result_strings.push(result_string)
    
    if result_strings.length == 0 or response.success == false
      if opts.tooltip
        _tooltipTitle = 'Unknown word'

    if opts.tooltip
      if !_tooltipTitle
        _tooltipTitle = string
      
      _tooltipTarget = $(element).find('a.tooltip_target')

      _tooltipTarget.popover
        title: _tooltipTitle
        content: $("<p />").html(result_strings.join('<br />')).html()
        html: true
        placement: () =>
          if _tooltipTarget[0].offsetLeft < 125
            'right'
          else
            'bottom'
        trigger: 'hover'
      
      # Done
      _tooltipTarget.popover('show')

      # Remove selection
      if window.getSelection
        # Chrome
        if window.getSelection().empty
          window.getSelection().empty()
        # Firefox
        else if window.getSelection().removeAllRanges
          window.getSelection().removeAllRanges()
      # IE
      else if document.selection
        document.selection.empty()



  
  lookupSelectEvent = (evt, string, element, index, opts) ->
    result_elem = $(document).find(opts.formResults)

    string = $.trim(string)

    if (string.length > 60) or (string.search(' ') > -1)
      return false

    if (string != "")
      langpair = $(opts.langPairSelect).val()
      source_lang = langpair.slice(0, 3)
      target_lang = langpair.slice(3, 6)
      lookup_string = string

      post_data =
        lookup: lookup_string
        lemmatize: true

      $.ajax
        url: "#{opts.api_host}/kursadict/lookup/#{source_lang}/#{target_lang}/"
        data: post_data
        success: (response) =>
          selection = {
            string: string
            element: element
            index: index
          }
          cleanTooltipResponse(selection, response, opts)
          if document.selection
            console.log "document.selection!"
            document.selection.empty()



  ##
   # $(document).selectToLookup();
   #
   #
   ## 

  $.fn.selectToLookup = (opts) ->
    opts = $.extend {}, $.fn.selectToLookup.options, opts
    spinner = initSpinner(opts.spinnerImg)

    # TODO: device / OptionsMenu
    if opts.displayOptions
      $(document).find('body').append Templates.OptionsTab(opts)
      window.optTab = $(document).find('#webdict_options')

    # Recall stored language pair from session
    previous_langpair = DSt.get('kursadict-select-langpair')
    if previous_langpair
      _select = "input[type=\"radio\"][value=\"#{previous_langpair}\"]"
      _opt = window.optTab.find(_select).attr('checked', 'checked')
    
    holdingOption = (evt, string, element, index) =>
      if evt.altKey
        lookupSelectEvent(evt, string, element, index, opts)
      # TODO: one idea for how to handle lookups wtihout alt/option key
      # else
      #   window.optTab.find('.well').addClass('highlight')
      #   window.optTab.find('.well a.open').click (o) =>
      #     lookupSelectEvent(evt, string, element, index, opts)
      #     return false
      return false
    
    clean = (event) ->
      parents = []
      $(document).find('a.tooltip_target').each () ->
        parents.push $(this).parent()
        $(this).popover('destroy')
        $(this).replaceWith(this.childNodes)
      # Set parent html to be parent html, for some reason this allows
      # all following click/lookup events to be properly registered
      if parents.length > 0
        for parent in parents
          parent.html parent.html()

    $(document).bind('textselect', holdingOption)
    $(document).bind('click', clean)
   
  $.fn.selectToLookup.options =
    api_host: API_HOST
    formResults: "#results"
    spinnerImg: "dev/img/spinner.gif"
    sourceLanguage: "sme"
    langPairSelect: "#webdict_options *[name='language_pair']:checked"
    tooltip: true
    displayOptions: true
    dictionaries: [
      {
        from:
          iso: 'sme'
          name: 'Nordsamisk'
        to:
          iso: 'nob'
          name: 'Norsk (bokmål)'
      },
      {
        from:
          iso: 'nob'
          name: 'Norsk (bokmål)'
        to:
          iso: 'sme'
          name: 'Nordsamisk'
      },
      {
        from:
          iso: 'sme'
          name: 'Nordsamisk'
        to:
          iso: 'fin'
          name: 'Finsk'
      },
    ]


  ##
   # $('#divname').kursadict();
   #
   #
   ## 
    
  $.fn.kursaDict = (opts) ->
    opts = $.extend {}, $.fn.kursaDict.options, opts

    this.each ->
      
      elem = $(this)
      result_elem = $(this).find('#results')

      # set up dropdown events for selecting language pair
      # Also store the default value in localStorage using DSt.js
      #
      $(this).find('#langpairs li a').click (obj) =>
        new_val = $(obj.target).attr('data-value')
        elem.find('button span.val_name').html(
          "#{new_val.slice(0,3)}->#{new_val.slice(3,6)}"
        )
        elem.find('input[name="target_lang"]').val new_val
        DSt.set('kursadict-form-langpair', new_val)
      
      # Recall previous value if stored in session.
      previous_setting = DSt.get('kursadict-form-langpair')
      if previous_setting
        elem.find('input[name="target_lang"]').val previous_setting
        elem.find('button span.val_name').html(
          "#{previous_setting.slice(0,3)}->#{previous_setting.slice(3,6)}"
        )

      elem.find('input[name="lookup"]').keydown (event) ->
        if event.keyCode == 13
          elem.submit()
          return false
        return true

      elem.submit () =>
        lookup_value = elem.find('input[name="lookup"]').val()

        lang_pair = $(this).find('input[name="target_lang"]').val()
        source_lang = lang_pair.slice(0,3)
        target_lang = lang_pair.slice(3,6)

        post_data =
          lookup: lookup_value

        if lookup_value.slice(-1) == '*'
          post_data.type = 'startswith'
          post_data.lookup = post_data.lookup.replace('*', '')

        unknownWord = (response) ->
          $(result_elem).append $("""
            <p xml:lang="no" class="alert">Ukjent ord.</p>
          """)
          return false

        cleanResponse = (response) =>
          $(result_elem).html ""

          if (response.success == false)
            unknownWord()
          else if (response.result.length == 1) and not response.result[0].lookups
            unknownWord()

          for result in response.result
            for lookup in result.lookups
              result_list = lookup.right.join(', ')
              
              $(result_elem).append $("""
                <p>#{lookup.left} (#{lookup.pos}) &mdash; #{result_list}</p>
              """)
        
        $.ajax
          url: "#{opts.api_host}/kursadict/lookup/#{source_lang}/#{target_lang}/"
          data: post_data
          success: cleanResponse

        return false

  $.fn.kursaDict.options =
    api_host: API_HOST
    formIDName: "#kursadict"
    formResults: "#results"

# End jQuery wrap


