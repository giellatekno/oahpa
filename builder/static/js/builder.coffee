# TODO: question element form - 

make_elem_form = (args) -> $ """
<form class="form-horizontal word-step-2" id="word-#{args.word_index}" data-word="#{args.word_index}">
  <div class="form-group">
    <label for="elem-name-#{args.word_index}" class="col-sm-5 control-label">Element name</label>
    <div class="col-sm-7">
        <input name="elem-name-#{args.word_index}" type="text" class="form-control"></input>
    </div>
  </div>
  <!--
  <div class="form-group">
      <label for="pos3" class="col-sm-12 control-label">
        <input type="checkbox">
          Task?
        </input>
      </label>
  </div>
  -->
  <div class="form-group">
    <label for="pos-#{args.word_index}" class="col-sm-2 control-label">POS</label>
    <div class="col-sm-8">
      <select class="form-control" name="pos-#{args.word_index}" disabled>
      </select>
    </div>
    <div class="col-sm-2">
       <input type="checkbox" class="enabler" data-field="element-tag-#{args.word_index}">
       </input>
     </div>
  </div>
  <div class="form-group">
    <label for="semtypes-#{args.word_index}" class="col-sm-2 control-label">Semtypes</label>
    <div class="col-sm-8">
      <select multiple class="form-control" name="semtypes-#{args.word_index}">
      </select>
      <p class="small-note">Narrow this down to 1 or 2</p>
    </div>
    <div class="col-sm-2">
       <input type="checkbox" class="enabler" data-field="semtypes-#{args.word_index}" checked>
       </input>
     </div>
  </div>
  <div class="form-group">
    <label for="element-tag-#{args.word_index}" class="col-sm-2 control-label">Tag</label>
    <div class="col-sm-8">
      <select class="form-control" name="element-tag-#{args.word_index}" disabled>
      </select>
    </div>
    <div class="col-sm-2">
       <input type="checkbox" class="enabler" data-field="element-tag-#{args.word_index}">
       </input>
     </div>
  </div>
  <div class="form-group">
    <div class="col-sm-9">
      <button class="btn btn-default" type="generate">Generate</button>
    </div>
  </div>
  <div class="form-group">
    <div class="col-sm-6">
      <ul class="words"></ul>
    </div>
    <div class="col-sm-6">
     <span class="count"></span>
    </div>
  </div>
</form>
"""

generate_results = () ->
  # TODO: use the parameters specified to display example words, and a
  # count
  form = $(this).parents('form')
  elems = form.find('.form-control:enabled')
  vals = {}
  for e in elems
    name = $(e).attr('name').replace(/-\d$/, '')
    if name == 'elem-name'
      continue
    val = $(e).val()
    vals[name] = val

  # semtypes
  # pos
  # element-tag

  
  query_kwargs = {}
  if vals.semtypes
    query_kwargs.semtypes = vals.semtypes.join(',')
  if vals.pos
    query_kwargs.pos = vals.pos
  if vals['element-tag']
    query_kwargs.tag = vals['element-tag']

  uri = 'http://localhost:8000/nuorti/builder/api/words/'

  $.ajax
    url: uri
    data: query_kwargs
    dataType: "json"
    type: "GET"
    success: (result) ->
      console.log result
      lemmas = (w.lemma for w in result.results)
      form.find('.count').html(result.count)
      form.find('.words li').remove()
      for l in lemmas.slice(0, 4)
        form.find('.words').append($("<li>#{l}</li>"))

  return false

toggle_available = () ->
  if $(this).is(':checked')
    $(this).parents('.form-group').find('.form-control[name]').attr('disabled', false)
  else
    $(this).parents('.form-group').find('.form-control[name]').attr('disabled', true)

render_element_form = (to_element, word_index) ->
  # This is a two step thing: request options, then do the get request

  word_tag = $(to_element).find('.word-step-1 :selected').attr('data-tag')
  word_fullform = $(to_element).attr('data-wordform')

  # TODO: populate tag menu with possible tags for POS, select current
  # word form
  #
  # TODO: calculate number of possibilities for this element
  #
  render_results = (options, result) ->
    # if length of results is greater than 1, we have a problem
    wordform = result.results[0]
    
    $(to_element).find('.word-step-1').toggle()

    # make the base form
    form = make_elem_form
      word_index: word_index
    form.find('.enabler').click toggle_available

    $(to_element).append form

    semtypes = (s.semtype for s in wordform.word.semtype)

    semtype_list = form.find("select[name=semtypes-#{word_index}]")
    pos_list = form.find("select[name=pos-#{word_index}]")
    tag_list = form.find("select[name=element-tag-#{word_index}]")

    for word_semtype in semtypes
      semtype_list.append $ "<option selected>#{word_semtype}</option>"

    for available_semtype in options.possible_values.semtypes
      semtype_list.append $ "<option>#{available_semtype}</option>"

    for p in options.possible_values.pos
      if p == wordform.word.pos
        pos_list.append $ "<option selected>#{p}</option>"
      else
        pos_list.append $ "<option>#{p}</option>"

    for t in options.possible_values.tags
      if t == word_tag
        tag_list.append $ "<option selected>#{t}</option>"
      else
        tag_list.append $ "<option>#{t}</option>"

    form.find('button[type=generate]').click generate_results

  uri = 'http://localhost:8000/nuorti/builder/api/forms/'

  params =
    fullform: word_fullform
    tag: word_tag

  get_word = (word_options_result) ->
    $.ajax
      url: uri
      data: params
      dataType: "json"
      type: "GET"
      success: (word_results) ->
        render_results(word_options_result, word_results)


  w_uri = 'http://localhost:8000/nuorti/builder/api/words/'

  $.ajax
    url: w_uri
    data: params
    dataType: "json"
    type: "OPTIONS"
    success: get_word

  return form


render_analysis_choice = () ->
  selected = $(this).find ' :selected'
  console.log selected
  tag = selected.attr('data-tag')
  lemma = selected.attr('data-lemma')
  word_index = $(this).parents('[data-word]').attr('data-word')
  console.log [lemma, tag, word_index]
  render_element_form($(this).parents('.word_column'), word_index)

render_analysis_options = (word_index, word_form) ->
  form_base = $("""
  <form class="word-step-1" data-word=#{word_index}>
      <select name="analysis_choice" class="form-control">
        <option class="note">Choose a matching form.</option>
      </select>
  </form>
  """)

  render_choice = (f) -> $ """
      <option data-lemma="#{f.word.lemma}" data-tag="#{f.tag.string}">#{f.fullform}: #{f.word.lemma} [#{f.tag.string}]</option>
  """

  render_results = (result) ->
    forms = result.results
    select_menu = form_base.find('select')
    if result.count > 0
      for f in forms
        select_menu.append(render_choice(f))
      select_menu.change render_analysis_choice
    else
      form_base.find('p.note').remove()
      form_base.find('select').attr('disabled', true)
      form_base.prepend($("<p>No matching forms</p>"))

  uri = 'http://localhost:8000/nuorti/builder/api/forms/'
  params =
    fullform: word_form

  $.ajax
    url: uri
    data: params
    dataType: "json"
    type: "GET"
    success: render_results

  # TODO: add events for changing the choice menu
  return form_base
  

render_search_menu = () ->
  if $(this).is(':checked')
    word = $(event.target).attr('data-word')
    wordform = $(event.target).attr('data-wordform')
    word_column = $ "div.word_column[data-word=#{word}]"
    word_column.append render_analysis_options(word, wordform)
  else
    word = $(event.target).attr('data-word')
    $(".word-step-1[data-word=#{word}]").remove()
    $(".word-step-2[data-word=#{word}]").remove()
  return false
  

render_question_column = (ws) ->
  for w, i in ws
    column_check_elem = """
      <div class="col-lg-3 col-md-3">
        <input type="checkbox" data-word=#{i} data-wordform="#{w}">
        </input>
      </div>
    """

    column_elem = """
	  <div class="col-lg-3 col-md-3 word_column" data-word=#{i} data-wordform=#{w}>
        <p class="lead q-word">#{w}</p>
	  </div>
    """

    $('#question_row_checks .row').append($(column_check_elem))
    $('#question_row .row').append($(column_elem))

  $('#question_row_checks input').change render_search_menu
  # Register click events
  

search_text = () ->
  $('#question_row_checks .row > div').remove()
  $('#question_row .row > div').remove()
  ws = $('textarea[name="question_text"]').val().split(' ')
  render_question_column(ws)
  return false

$(document).ready () ->
  # on form submit
  search_text()
  $('button[name=search]').click search_text

