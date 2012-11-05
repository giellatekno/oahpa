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

TODO: language dropdowns for nob-sme fin-sme, etc., autodetect from browser
      language first, fall back to nob otherwise

###

# Wrap jQuery and add plugin functionality
( jQuery ($) ->

  lookupSelectEvent = (evt, string, element, opts) ->
    # TODO: set source and target language somehow
    #   - use form select widget, or alternatively display some buttons
    #   in the tooltip? 
    #
    # TODO: select this div another way
    result_elem = $('#results')

    # TODO: option for displaying this in tooltip instead
    cleanResponse = (response) =>
      if response.success == false
        # TODO: make error visible to the user
        console.log "No words found."
        return false
      
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
      
      if result_strings.length == 0
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
          placement: 'bottom'
          trigger: 'hover'
        _tooltipTarget.popover().click (e) ->
          $(e).popover('destroy')
        _tooltipTarget.popover('show')
      else
        $(result_elem).html ""
        for _str in result_strings
          $(result_elem).append $("<p />").html(_str)

    if (string.length > 60) or (string.search(' ') > -1)
      return false

    if (string != "")
      source_lang = opts.sourceLanguage
      console.log source_lang
      target_lang = $(opts.targetLanguageSelect).val()
      lookup_string = string

      post_data =
        lookup: lookup_string
        lemmatize: true

      $.ajax
        url: "http://localhost:5000/lookup/#{source_lang}/#{target_lang}/"
        type: "POST"
        dataType: "json"
        data: JSON.stringify post_data
        cache: true
        success: cleanResponse
        fail: () ->
          console.log "omg2"

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
    tooltip: false
    sourceLanguage: "sme"
    targetLanguageSelect: "select[name='target_lang']"


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

      elem.submit () =>
        lookup_value = $(this).find('input[name="lookup"]').val()

        target_lang = $(this).find('select[name="target_lang"]').val()
        source_lang = $(this).find('input[name="source_lang"]').val()

        post_data =
          lookup: lookup_value

        if lookup_value.slice(-1) == '*'
          post_data.type = 'startswith'
          post_data.lookup = post_data.lookup.replace('*', '')

        cleanResponse = (response) ->
          if response.success == false
            console.log "No words found."
          $(result_elem).html ""
          for result in response.result
            for lookup in result.lookups
              $(result_elem).append $("""
                  <p>#{lookup.left} (#{lookup.pos}) &mdash; #{lookup.right}</p>
              """)
        
        $.ajax
          url: "http://localhost:5000/lookup/#{source_lang}/#{target_lang}/"
          type: "POST"
          dataType: "json"
          data: JSON.stringify post_data
          cache: true
          success: cleanResponse
          fail: () ->
            console.log "omg2"

        console.log "submitted"
        return false

  # $.fn.kursaDict.options =
  #   formIDName: "#kursadict"

# End jQuery wrap
) jQuery

