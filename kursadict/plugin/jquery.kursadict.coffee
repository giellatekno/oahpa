###
A jQuery plugin for enabling the Kursadict functionality

# Installation

HTML header

TODO: clarify how to install this somewhere.


# Development / testing

Install node.js and npm, and then coffeescript.

TODO: write more

## building

Must be compiled with --bare, to prevent function wrapping that disables
jQuery.

    coffee --compile --bare jquery.kursadict.coffee

## watch

    coffee --compile --watch --bare jquery.kursadict.coffee

Or.

    ./compile_and_watch.sh


## TODOs / Features

TODO: need an interface for managing options that isn't the search form,
      maybe a little tab popping out of the side like with the user voice /
      feedback app thing.

      - Icon?
        http://www.iconeasy.com/icon/png/System/Sticker%20Pack%202/Dictionary.png
        http://upload.wikimedia.org/wikipedia/en/d/d1/Dictionary_Icon.png

        maybe one with ášŋ or some clearly sámi symbols

        maybe just make my own without an additional .png requirement?

     - options:

       - target language
       - detail level of information display
       - place of display: tooltip/banner
       - device options: tablet / normal computer


TODO: autodetect from browser language first, fall back to nob otherwise


## TODOs / Bugs

TODO: Når ordet er nesten på enden av nettlesarvindaugo, hengjer popup
      litt utafor vindaugo, so er det vanskeleg å lesa. 
TODO: IE on all OSes seems to select a whole paragraph after a word has been
      selected. There is probably some way to prevent this from occurring.
TODO: prevent window url from updating with form submit params
TODO: lookup timeout


###

# Wrap jQuery and add plugin functionality
jQuery(document).ready ($) ->

  API_HOST = "http://testing.oahpa.no/"
  # if window.location.hostname == 'localhost'
  #   API_HOST = "http://localhost:5000/"
  # else if window.location.hostname == 'testing.oahpa.no'
  #   API_HOST = "http://#{window.location.hostname}/"

  Templates =
    OptionsTab: (args) ->
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
                <a href="#">Options</a>
              </li>
              <li><a href="#">About</a></li>
            </ul>
            <form class="">
              <label class="control-label" for="inputEmail">Dictionary</label>
               <label class="radio">
                <input type="radio" name="language_pair" id="language_pair1" value="smenob" checked>
                Northern Sámi -> Norwegian
              </label>
              <label class="radio">
                <input type="radio" name="language_pair" id="language_pair2" value="smefin">
                Northern Sámi -> Finnish
              </label> 
              <br />
              <label class="checkbox">
               <input type="checkbox" name="detail_level" />
               Extra info
              </label>
              <button type="submit" class="btn">Save</button>
            </div>
          </div>
          </form>
        </div>
      """)

      el.find('.trigger').click () ->
        optsp = el.find('div.option_panel')
        optsp.toggle()
        el.find('a.close').toggle()

      el.find('a.close').click () ->
        optsp = el.find('div.option_panel')
        optsp.toggle()
        el.find('a.close').toggle()

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

  initSpinner = () ->
    ###
        spinner popup in right corner; `spinner = initSpinner()` to
        create or find, then usual `spinner.show()` or `.hide()` as
        needed.
    ###
    spinnerExists = $(document).find('.spinner')
    if spinnerExists.length == 0
      spinner = $("""<img src="img/spinner.gif" class="spinner" />""")
      spinner.css {
        display: "none"
        position: "absolute"
        top: "0px"
        right: "0px"
      }
      $(document).find('body').append(spinner)
      return spinner
    return spinnerExists




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

    if baseOffset == extentOffset
      _left = $(selection.element).html().slice(0, baseOffset)
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

    if not index
      index = selection.element.html().search(string)
      indexMax = index + string.length
    
    # For tooltip we need to wrap the search word in a span.
    if opts.tooltip
      $(element).find('a.tooltip_target').each () ->
        $(this).popover('destroy')
        $(this).replaceWith(this.childNodes)

      _wrapElement = """
      <a style="font-style: italic; border: 1px solid #CEE; padding: 0 2px" 
         class="tooltip_target">#{string}</a>
      """

      console.log [index, indexMax]
      [_left, _mid, _right] = [$(element).html().slice(0, index),
                               $(element).html().slice(index, indexMax),
                               $(element).html().slice(indexMax)]
      console.log _left

      _mid_new = _mid.replace(string, _wrapElement)
      _new_html = _left + _mid_new + _right
      $(element).html(_new_html)

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

    # Use either bootstrap tooltip, or display in dictionary #results
    # div.
    if opts.tooltip
      if !_tooltipTitle
        _tooltipTitle = string
      _tooltipTarget = $(element).find('a.tooltip_target')
      _tooltipTarget.popover
        title: _tooltipTitle
        content: $("<p />").html(result_strings.join('<br />')).html()
        html: true
        placement: 'bottom'
        trigger: 'hover'
      
      _tooltipTarget.popover('show')
    else
      $(result_elem).html ""
      for _str in result_strings
        $(result_elem).append $("<p />").html(_str)



  
  lookupSelectEvent = (evt, string, element, index, opts) ->
    result_elem = $(opts.formResults)

    spinner = initSpinner()

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
        beforeSend: (args) ->
          spinner.show()
        complete: (args) ->
          spinner.hide()
        url: "#{opts.api_host}/kursadict/lookup/#{source_lang}/#{target_lang}/"
        type: "GET"
        dataType: "json"
        data: post_data
        cache: true
        success: (response) =>
          selection = {
            string: string
            element: element
            index: index
          }
          cleanTooltipResponse(selection, response, opts)
        error: () =>
          $(document).find('body').find('.errornav').remove()
          $(document).find('body').append Templates.ErrorBar {
            host: opts.hostname
          }



  ##
   # $(document).selectToLookup();
   #
   #
   ## 



  $.fn.selectToLookup = (opts) ->
    opts = $.extend {}, $.fn.selectToLookup.options, opts

    if opts.displayOptions
      $(document).find('body').append Templates.OptionsTab()
    # TODO: defaults if otherwise
    
    holdingOption = (evt, string, element, index) =>
      if evt.altKey
        lookupSelectEvent(evt, string, element, index, opts)
      return false
    
    clean = (event) ->
      parents = []
      $(document).find('a.tooltip_target').each () ->
        parents.push $(this).parent()
        $(this).popover('destroy')
        $(this).replaceWith(this.childNodes)
      # Set parent html to be parent html, for some reason this allows
      # all following click/lookup events to be properly registered
      for parent in parents
        parent.html parent.html()

    $(document).bind('textselect', holdingOption)
    $(document).bind('click', clean)
   
  $.fn.selectToLookup.options =
    api_host: API_HOST
    formResults: "#results"
    sourceLanguage: "sme"
    langPairSelect: "#webdict_options *[name='language_pair']:checked"
    tooltip: true
    displayOptions: true


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

      spinner = initSpinner()

      elem.submit () =>
        lookup_value = $(this).find('input[name="lookup"]').val()

        target_lang = $(this).find('input[name="target_lang"]:checked').val()
        source_lang = $(this).find('input[name="source_lang"]').val()

        post_data =
          lookup: lookup_value

        if lookup_value.slice(-1) == '*'
          post_data.type = 'startswith'
          post_data.lookup = post_data.lookup.replace('*', '')

        unknownWord = (response) ->
          $(result_elem).append $("""
            <p>Unknown word.</p>
          """)
          return false

        cleanResponse = (response) =>
          $(result_elem).html ""

          if (response.success == false)
            unknownWord()
          if (response.result.length == 1) and not response.result[0].lookups
            unknownWord()

          for result in response.result
            for lookup in result.lookups
              $(result_elem).append $("""
                <p>#{lookup.left} (#{lookup.pos}) &mdash; #{lookup.right}</p>
              """)
        
        $.ajax
          beforeSend: (args) ->
            spinner.show()
          complete: (args) ->
            spinner.hide()
          url: "#{opts.api_host}/kursadict/lookup/#{source_lang}/#{target_lang}/"
          type: "GET"
          data: post_data
          dataType: "json"
          cache: true
          success: cleanResponse
          error: () ->
            $(result_elem).find('.alert').remove()
            $(result_elem).append $("""
              <div class="alert">
                <strong>Error!</strong> could not connect to dictionary server (#{opts.api_host}).
              </div>
            """)

        return false

  $.fn.kursaDict.options =
    api_host: API_HOST
    formIDName: "#kursadict"
    formResults: "#results"

# End jQuery wrap


