###
A jQuery plugin for enabling the Kursadict functionality

# Installation

HTML header

TODO: clarify how to install this somewhere.


# Development / testing

Install node.js and npm, and then coffeescript.

## building

Must be compiled with --bare, to prevent function wrapping that disables
jQuery.

    coffee --compile --bare jquery.kursadict.coffee

## watch

    coffee --compile --watch --bare jquery.kursadict.coffee

## TODOs

TODO: autodetect from browser language first, fall back to nob otherwise

TODO: debugging for misc browsers where there are issues.

TODO: check globally for wraps instead of just in element, remove them;
      make sure .classname is much more random

TODO: prevent window url from updating with form submit params


###

# Wrap jQuery and add plugin functionality
( jQuery ($) ->

  API_HOST = "http://testing.oahpa.no/"

  initSpinner = () ->
    ###
        spinner popup in right corner; `spinner = initSpinner()` to
        create or find, then usual `spinner.show()` or `.hide()` as
        needed.
    ###
    spinnerExists = $('body').find('spinner')
    if spinnerExists.length == 0
      spinner = $("""<img src="img/spinner.gif" class="spinner" />""")
      spinner.css {
        display: "none"
        position: "absolute"
        top: "0px"
        right: "0px"
      }
      $('body').append(spinner)
      return spinner
    return spinnerExists

  cleanTooltipResponse = (string, element, response, opts) ->
    ###
        Clean response from tooltip $.ajax query, and display results
    ###
    
    # For tooltip we need to wrap the search word in a span.
    if opts.tooltip
      $(element).find('a.tooltip_target').each () ->
        $(this).popover('destroy')
        $(this).replaceWith(this.childNodes)

      _wrapElement = """
      <a style="font-style: italic; border: 1px solid #CEE; padding: 0 2px" 
         class="tooltip_target">#{string}</a>
      """

      _new_html = $(element).html().replace(string, _wrapElement)
      $(element).html(_new_html)

    # Compile result strings
    result_strings = []
    for result in response.result
      for lookup in result.lookups
        result_string = "<em>#{lookup.left}</em> (#{lookup.pos}) &mdash; #{lookup.right}"
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

  
  lookupSelectEvent = (evt, string, element, opts) ->
    result_elem = $(opts.formResults)

    spinner = initSpinner()

    string = string.trim()

    if (string.length > 60) or (string.search(' ') > -1)
      return false

    if (string != "")
      source_lang = opts.sourceLanguage
      target_lang = $(opts.targetLanguageSelect).val()
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
          cleanTooltipResponse(string, element, response, opts)
        error: () ->
          $('body').find('.errornav').remove()
          $('body').append $("""
              <div class="errornav navbar-inverse navbar-fixed-bottom">
                <div class="navbar-inner">
                  <div class="container">
                    <p><strong>Error!</strong> Could not connect to dictionary server. <a href="#" class="dismiss">Close</a>.</p>
                  </div>
                </div>
              </div>
          """)
          $('body').find('.errornav .dismiss').click () ->
            $('body .errornav').remove()
            return false

  ##
   # $(document).selectToLookup();
   #
   #
   ## 

  $.fn.selectToLookup = (opts) ->
    opts = $.extend {}, $.fn.selectToLookup.options, opts

    holdingOption = (evt, string, element) =>
      if evt.altKey
        lookupSelectEvent(evt, string, element, opts)
    
    $(document).bind('textselect', holdingOption)
   
  $.fn.selectToLookup.options =
    api_host: API_HOST
    formResults: "#results"
    sourceLanguage: "sme"
    targetLanguageSelect: "select[name='target_lang']"
    tooltip: false


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
                <strong>Error!</strong> could not connect to dictionary server.
              </div>
            """)

        return false

  $.fn.kursaDict.options =
    api_host: API_HOST
    formIDName: "#kursadict"
    formResults: "#results"

# End jQuery wrap
) jQuery

