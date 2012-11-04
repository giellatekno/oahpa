###
A jQuery plugin for enabling the Kursadict functionality

# Installation

HTML header

    <script type='text/javascript' src='jquery.1.7.2.js'></script>
    <script type='text/javascript' src='jquery.kursadict.js'></script>
    <script type='text/javascript' src='jquery.textselect.event.js'></script>
    <script type='text/javascript'>
        jQuery(document).ready(function (){
            // Register the input form with options, replace ID here with ID of form
            jQuery('#kursadict').kursaDict();

            // Enable options for inline clicking, preferably <p /> elements
            jQuery('CSS > selector > to > elements > to > watch').textLookup();

            // May define multiple of these
            jQuery('div.someDiv p').textLookup();

        });
    </script>


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

TODO: inline textLookup option to display result in form lookup div,
      or to use bootstrap popovers

TODO: inline textLookup option to only perform lookup if word is selected with
      CTRL/Option, etc

###

# Wrap jQuery and add plugin functionality
( jQuery ($) ->

  lookupSelectEvent = (evt, string, element) ->
    # TODO: set source and target language somehow
    #
    # TODO: select another way
    result_elem = $('#results')

    # TODO: option for displaying this in tooltip instead
    cleanResponse = (response) ->
      if response.success == false
        console.log "No words found."
      $(result_elem).html ""
      for lookup in response.result.lookups
      	$(result_elem).append $("""
      	    <p>#{lookup.left} (#{lookup.pos}) &mdash; #{lookup.right}</p>
      	""")

    if (string != "")
      source_lang = 'sme'
      target_lang = 'nob'
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
    $(document).bind('textselect', lookupSelectEvent)


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
          for lookup in response.result.lookups
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

  # $.fn.kursaDict = (opts) ->
  #   opts = $.extend {}, $.fn.pullQuote.options, opts
  #   this.each ->
  #     console.log "omg"

  # $.fn.kursaDict.options =
  #   formIDName: "#kursadict"

# End jQuery wrap
) jQuery

