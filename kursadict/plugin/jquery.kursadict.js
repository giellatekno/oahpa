/* ============================================================
 * bootstrap-dropdown.js v2.2.1
 * http://twitter.github.com/bootstrap/javascript.html#dropdowns
 * ============================================================
 * Copyright 2012 Twitter, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ============================================================ */


!function ($) {

  "use strict"; // jshint ;_;


 /* DROPDOWN CLASS DEFINITION
  * ========================= */

  var toggle = '[data-toggle=dropdown]'
    , Dropdown = function (element) {
        var $el = $(element).on('click.dropdown.data-api', this.toggle)
        $('html').on('click.dropdown.data-api', function () {
          $el.parent().removeClass('open')
        })
      }

  Dropdown.prototype = {

    constructor: Dropdown

  , toggle: function (e) {
      var $this = $(this)
        , $parent
        , isActive

      if ($this.is('.disabled, :disabled')) return

      $parent = getParent($this)

      isActive = $parent.hasClass('open')

      clearMenus()

      if (!isActive) {
        $parent.toggleClass('open')
        $this.focus()
      }

      return false
    }

  , keydown: function (e) {
      var $this
        , $items
        , $active
        , $parent
        , isActive
        , index

      if (!/(38|40|27)/.test(e.keyCode)) return

      $this = $(this)

      e.preventDefault()
      e.stopPropagation()

      if ($this.is('.disabled, :disabled')) return

      $parent = getParent($this)

      isActive = $parent.hasClass('open')

      if (!isActive || (isActive && e.keyCode == 27)) return $this.click()

      $items = $('[role=menu] li:not(.divider) a', $parent)

      if (!$items.length) return

      index = $items.index($items.filter(':focus'))

      if (e.keyCode == 38 && index > 0) index--                                        // up
      if (e.keyCode == 40 && index < $items.length - 1) index++                        // down
      if (!~index) index = 0

      $items
        .eq(index)
        .focus()
    }

  }

  function clearMenus() {
    $(toggle).each(function () {
      getParent($(this)).removeClass('open')
    })
  }

  function getParent($this) {
    var selector = $this.attr('data-target')
      , $parent

    if (!selector) {
      selector = $this.attr('href')
      selector = selector && /#/.test(selector) && selector.replace(/.*(?=#[^\s]*$)/, '') //strip for ie7
    }

    $parent = $(selector)
    $parent.length || ($parent = $this.parent())

    return $parent
  }


  /* DROPDOWN PLUGIN DEFINITION
   * ========================== */

  $.fn.dropdown = function (option) {
    return this.each(function () {
      var $this = $(this)
        , data = $this.data('dropdown')
      if (!data) $this.data('dropdown', (data = new Dropdown(this)))
      if (typeof option == 'string') data[option].call($this)
    })
  }

  $.fn.dropdown.Constructor = Dropdown


  /* APPLY TO STANDARD DROPDOWN ELEMENTS
   * =================================== */

  $(document)
    .on('click.dropdown.data-api touchstart.dropdown.data-api', clearMenus)
    .on('click.dropdown touchstart.dropdown.data-api', '.dropdown form', function (e) { e.stopPropagation() })
    .on('click.dropdown.data-api touchstart.dropdown.data-api'  , toggle, Dropdown.prototype.toggle)
    .on('keydown.dropdown.data-api touchstart.dropdown.data-api', toggle + ', [role=menu]' , Dropdown.prototype.keydown)

}(window.jQuery);/* ===========================================================
 * bootstrap-tooltip.js v2.2.1
 * http://twitter.github.com/bootstrap/javascript.html#tooltips
 * Inspired by the original jQuery.tipsy by Jason Frame
 * ===========================================================
 * Copyright 2012 Twitter, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ========================================================== */


!function ($) {

  "use strict"; // jshint ;_;


 /* TOOLTIP PUBLIC CLASS DEFINITION
  * =============================== */

  var Tooltip = function (element, options) {
    this.init('tooltip', element, options)
  }

  Tooltip.prototype = {

    constructor: Tooltip

  , init: function (type, element, options) {
      var eventIn
        , eventOut

      this.type = type
      this.$element = $(element)
      this.options = this.getOptions(options)
      this.enabled = true

      if (this.options.trigger == 'click') {
        this.$element.on('click.' + this.type, this.options.selector, $.proxy(this.toggle, this))
      } else if (this.options.trigger != 'manual') {
        eventIn = this.options.trigger == 'hover' ? 'mouseenter' : 'focus'
        eventOut = this.options.trigger == 'hover' ? 'mouseleave' : 'blur'
        this.$element.on(eventIn + '.' + this.type, this.options.selector, $.proxy(this.enter, this))
        this.$element.on(eventOut + '.' + this.type, this.options.selector, $.proxy(this.leave, this))
      }

      this.options.selector ?
        (this._options = $.extend({}, this.options, { trigger: 'manual', selector: '' })) :
        this.fixTitle()
    }

  , getOptions: function (options) {
      options = $.extend({}, $.fn[this.type].defaults, options, this.$element.data())

      if (options.delay && typeof options.delay == 'number') {
        options.delay = {
          show: options.delay
        , hide: options.delay
        }
      }

      return options
    }

  , enter: function (e) {
      var self = $(e.currentTarget)[this.type](this._options).data(this.type)

      if (!self.options.delay || !self.options.delay.show) return self.show()

      clearTimeout(this.timeout)
      self.hoverState = 'in'
      this.timeout = setTimeout(function() {
        if (self.hoverState == 'in') self.show()
      }, self.options.delay.show)
    }

  , leave: function (e) {
      var self = $(e.currentTarget)[this.type](this._options).data(this.type)

      if (this.timeout) clearTimeout(this.timeout)
      if (!self.options.delay || !self.options.delay.hide) return self.hide()

      self.hoverState = 'out'
      this.timeout = setTimeout(function() {
        if (self.hoverState == 'out') self.hide()
      }, self.options.delay.hide)
    }

  , show: function () {
      var $tip
        , inside
        , pos
        , actualWidth
        , actualHeight
        , placement
        , tp

      if (this.hasContent() && this.enabled) {
        $tip = this.tip()
        this.setContent()

        if (this.options.animation) {
          $tip.addClass('fade')
        }

        placement = typeof this.options.placement == 'function' ?
          this.options.placement.call(this, $tip[0], this.$element[0]) :
          this.options.placement

        inside = /in/.test(placement)

        $tip
          .detach()
          .css({ top: 0, left: 0, display: 'block' })
          .insertAfter(this.$element)

        pos = this.getPosition(inside)

        actualWidth = $tip[0].offsetWidth
        actualHeight = $tip[0].offsetHeight

        switch (inside ? placement.split(' ')[1] : placement) {
          case 'bottom':
            tp = {top: pos.top + pos.height, left: pos.left + pos.width / 2 - actualWidth / 2}
            break
          case 'top':
            tp = {top: pos.top - actualHeight, left: pos.left + pos.width / 2 - actualWidth / 2}
            break
          case 'left':
            tp = {top: pos.top + pos.height / 2 - actualHeight / 2, left: pos.left - actualWidth}
            break
          case 'right':
            tp = {top: pos.top + pos.height / 2 - actualHeight / 2, left: pos.left + pos.width}
            break
        }

        $tip
          .offset(tp)
          .addClass(placement)
          .addClass('in')
      }
    }

  , setContent: function () {
      var $tip = this.tip()
        , title = this.getTitle()

      $tip.find('.tooltip-inner')[this.options.html ? 'html' : 'text'](title)
      $tip.removeClass('fade in top bottom left right')
    }

  , hide: function () {
      var that = this
        , $tip = this.tip()

      $tip.removeClass('in')

      function removeWithAnimation() {
        var timeout = setTimeout(function () {
          $tip.off($.support.transition.end).detach()
        }, 500)

        $tip.one($.support.transition.end, function () {
          clearTimeout(timeout)
          $tip.detach()
        })
      }

      $.support.transition && this.$tip.hasClass('fade') ?
        removeWithAnimation() :
        $tip.detach()

      return this
    }

  , fixTitle: function () {
      var $e = this.$element
      if ($e.attr('title') || typeof($e.attr('data-original-title')) != 'string') {
        $e.attr('data-original-title', $e.attr('title') || '').removeAttr('title')
      }
    }

  , hasContent: function () {
      return this.getTitle()
    }

  , getPosition: function (inside) {
      return $.extend({}, (inside ? {top: 0, left: 0} : this.$element.offset()), {
        width: this.$element[0].offsetWidth
      , height: this.$element[0].offsetHeight
      })
    }

  , getTitle: function () {
      var title
        , $e = this.$element
        , o = this.options

      title = $e.attr('data-original-title')
        || (typeof o.title == 'function' ? o.title.call($e[0]) :  o.title)

      return title
    }

  , tip: function () {
      return this.$tip = this.$tip || $(this.options.template)
    }

  , validate: function () {
      if (!this.$element[0].parentNode) {
        this.hide()
        this.$element = null
        this.options = null
      }
    }

  , enable: function () {
      this.enabled = true
    }

  , disable: function () {
      this.enabled = false
    }

  , toggleEnabled: function () {
      this.enabled = !this.enabled
    }

  , toggle: function (e) {
      var self = $(e.currentTarget)[this.type](this._options).data(this.type)
      self[self.tip().hasClass('in') ? 'hide' : 'show']()
    }

  , destroy: function () {
      this.hide().$element.off('.' + this.type).removeData(this.type)
    }

  }


 /* TOOLTIP PLUGIN DEFINITION
  * ========================= */

  $.fn.tooltip = function ( option ) {
    return this.each(function () {
      var $this = $(this)
        , data = $this.data('tooltip')
        , options = typeof option == 'object' && option
      if (!data) $this.data('tooltip', (data = new Tooltip(this, options)))
      if (typeof option == 'string') data[option]()
    })
  }

  $.fn.tooltip.Constructor = Tooltip

  $.fn.tooltip.defaults = {
    animation: true
  , placement: 'top'
  , selector: false
  , template: '<div class="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>'
  , trigger: 'hover'
  , title: ''
  , delay: 0
  , html: false
  }

}(window.jQuery);/* ===========================================================
 * bootstrap-popover.js v2.2.1
 * http://twitter.github.com/bootstrap/javascript.html#popovers
 * ===========================================================
 * Copyright 2012 Twitter, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * =========================================================== */


!function ($) {

  "use strict"; // jshint ;_;


 /* POPOVER PUBLIC CLASS DEFINITION
  * =============================== */

  var Popover = function (element, options) {
    this.init('popover', element, options)
  }


  /* NOTE: POPOVER EXTENDS BOOTSTRAP-TOOLTIP.js
     ========================================== */

  Popover.prototype = $.extend({}, $.fn.tooltip.Constructor.prototype, {

    constructor: Popover

  , setContent: function () {
      var $tip = this.tip()
        , title = this.getTitle()
        , content = this.getContent()

      $tip.find('.popover-title')[this.options.html ? 'html' : 'text'](title)
      $tip.find('.popover-content > *')[this.options.html ? 'html' : 'text'](content)

      $tip.removeClass('fade top bottom left right in')
    }

  , hasContent: function () {
      return this.getTitle() || this.getContent()
    }

  , getContent: function () {
      var content
        , $e = this.$element
        , o = this.options

      content = $e.attr('data-content')
        || (typeof o.content == 'function' ? o.content.call($e[0]) :  o.content)

      return content
    }

  , tip: function () {
      if (!this.$tip) {
        this.$tip = $(this.options.template)
      }
      return this.$tip
    }

  , destroy: function () {
      this.hide().$element.off('.' + this.type).removeData(this.type)
    }

  })


 /* POPOVER PLUGIN DEFINITION
  * ======================= */

  $.fn.popover = function (option) {
    return this.each(function () {
      var $this = $(this)
        , data = $this.data('popover')
        , options = typeof option == 'object' && option
      if (!data) $this.data('popover', (data = new Popover(this, options)))
      if (typeof option == 'string') data[option]()
    })
  }

  $.fn.popover.Constructor = Popover

  $.fn.popover.defaults = $.extend({} , $.fn.tooltip.defaults, {
    placement: 'right'
  , trigger: 'click'
  , content: ''
  , template: '<div class="popover"><div class="arrow"></div><div class="popover-inner"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'
  })

}(window.jQuery);var DSt=(function(){var a={version:0.002005,get:function(b){var c=localStorage.getItem(b);if(c===undefined||c===null){c="null"}else{c=c.toString()}return JSON.parse(c)},set:function(b,c){return localStorage.setItem(b,JSON.stringify(c))},store:function(b){if(typeof(b)=="string"){b=document.getElementById(b)}if(!b||b.name==""){return this}var c=a._form_elt_key(b);if(b.type=="checkbox"){a.set(c,b.checked?1:0)}else{if(b.type=="radio"){a.set(c,a._radio_value(b))}else{a.set(c,b.value||"")}}return this},recall:function(b){if(typeof(b)=="string"){b=document.getElementById(b)}if(!b||b.name==""){return this}var c=a._form_elt_key(b);var d=a.get(c);if(b.type=="checkbox"){b.checked=!!d}else{if(b.type=="radio"){if(b.value==d){b.checked=true}}else{b.value=d||""}}return this},_form_elt_key:function(b){return"_form_"+b.form.name+"_field_"+b.name},_radio_value:function(e){if(typeof(e)=="string"){e=document.getElementById(e)}var f=e.form.elements[e.name];var b=f.length;var d=null;for(var c=0;c<b;c++){if(f[c].checked){d=f[c].value}}return d},recall_form:function(b){return a._apply_fn_to_form_inputs(b,a.recall)},store_form:function(b){return a._apply_fn_to_form_inputs(b,a.store)},_apply_fn_to_form_inputs:function(e,c){if(typeof(e)=="string"){e=document.getElementById(e)}var f=e.elements.length;for(var b=0;b<f;b++){var d=e.elements[b];if(d.tagName=="TEXTAREA"||d.tagName=="INPUT"&&d.type!="file"&&d.type!="button"&&d.type!="image"&&d.type!="password"&&d.type!="submit"&&d.type!="reset"){c(d)}}return this},_storage_types:function(){var b="";for(var c in window){if(c=="sessionStorage"||c=="globalStorage"||c=="localStorage"||c=="openDatabase"){b+=b?(" "+c):c}}return b},javascript_accepts_trailing_comma:false};return a})();﻿/*!
 * Copyright Andrée Hansson, 2009
 * Licensed under the MIT license
 * http://www.opensource.org/licenses/mit-license.php
 *
 * Contact: E-mail:  peolanha _AT gmail _DOT com
 *          Twitter: peolanha
 *          Website: http://andreehansson.se/
 */
(function ($) {
    var
        // Will contain the last events' string and element, used for comparison
        selObj = { str : "", el : undefined },

        // Cache selection range methods
        docSel = document.selection,
        winSel = window.getSelection && window.getSelection(),

        // Events to be bound for our handler
        bindEvents = ['mouseup', 'keyup'],

        // Helper to grab currently selected text
        getSelected = function (evt) {

            // If the called event originates from a inputbox/form element (in FF), use that
            // to get the selected text (FF doesn't trigger getSelection() on input
            // elements natively)
            // TODO: if user clicks on radio, and event fails, do
            // something else
            var el = $(evt.originalEvent.target).is(':input') ?
                evt.originalEvent.target :
                undefined;

            return el && +el.selectionEnd ? 
                $(el).val().substring(el.selectionStart, el.selectionEnd) :
                (winSel || docSel.createRange().text || "").toString();
        },

        // Helper to grab index of currently selected text
        getSelectedIndex = function (evt) {

            var el = $(evt.originalEvent.target).is(':input') ?
                evt.originalEvent.target :
                undefined;

            if (el && +el.selectionEnd) {
            	var thing = el.selectionStart;
            	var index = el.selectionStart;
            } else {
            	var thing = winSel || docSel.createRange() || "",
            	    index = thing.baseOffset && thing.extentOffset ? 
            	            [thing.baseOffset, thing.extentOffset] :
            	            [thing.anchorOffset, thing.focusOffset] ;
            }
            return index ;
        },

        // Helper to grab which common ancestor the text has
        getOrigin = function (input) {
            return docSel && docSel.createRange().parentElement()
                || input
                || winSel && winSel.getRangeAt(0).commonAncestorContainer
                || document.body;
        },

        // Create our custom event namespace
        $me = $.event.special.textselect = {

            // Do stuff when it is bound
            setup: function () {
                var that = this;
    
                // Hook mouseup to fire our custom event
                $(bindEvents).each(function (i, o) {
                    $(that).bind(o, $me.handler);
                });
            },
    
            // Do stuff when it is unbound
            teardown: function () {
                var that = this;
    
                $(bindEvents).each(function (i, o) {
                    $(that).unbind(o, $me.handler);
                });
            },
    
            // Do stuff when the event is triggered
            handler: function (evt) {
    
                // Since we're not letting jQuery handle this object (due to our return
                // parameters, we "fix" the event object to be cross-browser compliant
                // manually
                evt = $.event.fix(evt);
    
                // Grab currently selected text and its common ancestor element
                var
                    curText = getSelected(evt),
                    curIndex = getSelectedIndex(evt),
                    conElement = $(evt.originalEvent.target).is(':input') ?
                        getOrigin(evt.originalEvent.target) :
                        getOrigin();

                if (conElement.nodeType === 3) conElement = conElement.parentNode;

                // If it differs from the old selected text, trigger event
                if (selObj.str !== curText || selObj.el !== conElement) {
    
                    // Set currently selected text (and element) to the actual currently
                    // selected text and element
                    selObj = { str : curText, el : conElement, index : curIndex };
    
                    // Change event type to our custom event
                    evt.type = 'textselect';
    
                    // Fire the simulated event
                    $.event.trigger(evt, [selObj.str, selObj.el, selObj.index]);
                }
            }
        };
})(jQuery);
// Generated by CoffeeScript 1.4.0
/*
A jQuery plugin for enabling the Kursadict functionality


## TODOs / Bugs

TODO: IE on all OSes seems to select a whole paragraph after a word has been
      selected. There is probably some way to prevent this from occurring.

TODO: IE sometimes still does not notice the first lookup

TODO: prevent window url from updating with form submit params

TODO: lookup timeout -- set on $.ajax, but sometimes seems not to work?

TODO: Opera on Windows - alt+click context window
*/

jQuery(document).ready(function($) {
  var API_HOST, Templates, cleanTooltipResponse, getActualIndex, initSpinner, lookupSelectEvent,
    _this = this;
  API_HOST = "http://testing.oahpa.no/";
  Templates = {
    OptionsMenu: function(opts) {
      return "omg";
    },
    OptionsTab: function(opts) {
      var el, makeLanguageOption;
      makeLanguageOption = function(options) {
        var checked, data, i, options_block, _i, _len;
        options_block = [];
        for (i = _i = 0, _len = options.length; _i < _len; i = ++_i) {
          data = options[i];
          if (i + 1 === 1) {
            checked = "checked";
          } else {
            checked = "";
          }
          options_block.push("<label class=\"radio\">\n  <input type=\"radio\" \n         name=\"language_pair\" \n         id=\"language_pair" + (i + 1) + "\" \n         value=\"" + data.from.iso + data.to.iso + "\" " + checked + ">\n  " + data.from.name + " -> " + data.to.name + "\n</label>");
        }
        return options_block.join('\n');
      };
      el = $("<div id=\"webdict_options\" class=\"hidden\">\n  <div class=\"well\">\n  <a class=\"close\" href=\"#\" style=\"display: none;\">&times;</a>\n  <div class=\"trigger\">\n    <h1><a href=\"#\" class=\"open\">Á</a></h1>\n  </div>\n\n  <div class=\"option_panel\" style=\"display: none;\">\n    <ul class=\"nav nav-pills\">\n      <li class=\"active\">\n        <a href=\"#\" data-target=\"#options\">Options</a>\n      </li>\n      <li><a href=\"#\" data-target=\"#about\">About</a></li>\n    </ul>\n    <div id=\"options\" class=\"minipanel\">\n      <form class=\"\">\n        <label class=\"control-label\" for=\"inputEmail\">Ordbok</label>\n        " + (makeLanguageOption(opts.dictionaries)) + "\n        <button type=\"submit\" class=\"btn\" id=\"save\">Save</button>\n      </form>\n    </div>\n    <div id=\"about\" style=\"display: none;\" class=\"minipanel\">\n    <p>To look up a word, hold Alt (or Option/⌥ on Macs) and double click a word. If the popup disappears, either hover over the link that is created, or click anywhere on the screen, and then try again.</p>\n    <p>To report problems, <a href=\"mailto:\">contact us</a>.</p>\n    </div>\n  </div>\n</div>");
      el.find('ul.nav-pills a').click(function(evt) {
        var target_element;
        target_element = $(evt.target).attr('data-target');
        el.find('ul.nav-pills a').parent('li').removeClass('active');
        $(evt.target).parent('li').addClass('active');
        el.find('div.minipanel').hide();
        el.find(target_element).show();
        return false;
      });
      el.find('.trigger').click(function() {
        var optsp;
        optsp = el.find('div.option_panel');
        optsp.toggle();
        return el.find('a.close').toggle();
      });
      el.find('a.close').click(function() {
        var optsp;
        optsp = el.find('div.option_panel');
        optsp.toggle();
        return el.find('a.close').toggle();
      });
      el.find('input[name="language_pair"][type="radio"]').click(function(e) {
        var store_val;
        store_val = $(e.target).val();
        DSt.set('kursadict-select-langpair', store_val);
        return true;
      });
      el.find('form').submit(function() {
        var optsp;
        optsp = el.find('div.option_panel');
        optsp.toggle();
        el.find('a.close').toggle();
        return false;
      });
      return el;
    },
    ErrorBar: function(args) {
      var el, host;
      host = args.host;
      el = $("<div class=\"errornav navbar-inverse navbar-fixed-bottom\">\n  <div class=\"navbar-inner\">\n    <div class=\"container\">\n      <p><strong>Error!</strong> Could not connect to dictionary server (host: " + host + ").\n         <a href=\"#\" class=\"dismiss\">Close</a>.</p>\n    </div>\n  </div>\n</div>");
      el.find('.errornav .dismiss').click(function() {
        $(document).find('body .errornav').remove();
        return false;
      });
      return el;
    }
  };
  initSpinner = function(imgPath) {
    /*
            spinner popup in right corner; `spinner = initSpinner()` to
            create or find, then usual `spinner.show()` or `.hide()` as
            needed.
    */

    var spinner, spinnerExists;
    spinnerExists = $(document).find('.spinner');
    if (spinnerExists.length === 0) {
      spinner = $("<img src=\"" + imgPath + "\" class=\"spinner\" />");
      $(document).find('body').append(spinner);
      return spinner;
    }
    return spinnerExists;
  };
  $.ajaxSetup({
    type: "GET",
    timeout: 10 * 1000,
    beforeSend: function(args) {
      var spinner;
      spinner = initSpinner();
      return spinner.show();
    },
    complete: function(args) {
      var spinner;
      spinner = initSpinner();
      return spinner.hide();
    },
    dataType: "json",
    cache: true,
    error: function() {
      $(document).find('body').find('.errornav').remove();
      return $(document).find('body').append(Templates.ErrorBar({
        host: API_HOST
      }));
    }
  });
  getActualIndex = function(selection) {
    var baseOffset, extentOffset, last, _left, _ref;
    _ref = selection.index, baseOffset = _ref[0], extentOffset = _ref[1];
    if (baseOffset === extentOffset) {
      _left = $(selection.element).html().slice(0, baseOffset);
      last = _left.match(/[^\s.]*$/);
      if (last[0] !== "") {
        return baseOffset - last[0].length;
      } else {
        return baseOffset;
      }
    } else {
      return baseOffset;
    }
    return selection.index[0];
  };
  cleanTooltipResponse = function(selection, response, opts) {
    /*
            Clean response from tooltip $.ajax query, and display results
    */

    var clean_right, element, i, index, indexMax, lookup, r, result, result_string, result_strings, right, string, _elem_html, _i, _j, _k, _left, _len, _len1, _len2, _mid, _mid_new, _new_html, _ref, _ref1, _ref2, _right, _tooltipTarget, _tooltipTitle, _wrapElement,
      _this = this;
    if (!selection.index) {
      console.log("no index!");
    }
    string = selection.string;
    element = selection.element;
    index = getActualIndex(selection);
    indexMax = index + string.length;
    if (!index) {
      console.log("no index!!");
      index = $(selection.element).html().search(string);
      indexMax = index + string.length;
    }
    if (opts.tooltip) {
      _wrapElement = "<a style=\"font-style: italic; border: 1px solid #CEE; padding: 0 2px\" \n   class=\"tooltip_target\">" + string + "</a>";
      _elem_html = $(element).html();
      _left = _elem_html.slice(0, index);
      _mid = _elem_html.slice(index, indexMax);
      _right = _elem_html.slice(indexMax);
      _mid_new = _mid.replace(string, _wrapElement);
      _new_html = _left + _mid_new + _right;
      $(element).html(_new_html);
    }
    result_strings = [];
    _ref = response.result;
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      result = _ref[_i];
      _ref1 = result.lookups;
      for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
        lookup = _ref1[_j];
        if (lookup.right.length > 1) {
          clean_right = [];
          _ref2 = lookup.right;
          for (i = _k = 0, _len2 = _ref2.length; _k < _len2; i = ++_k) {
            r = _ref2[i];
            clean_right.push("" + (i + 1) + ". " + r);
          }
          right = clean_right.join(', ');
        } else {
          right = lookup.right[0];
        }
        result_string = "<em>" + lookup.left + "</em> (" + lookup.pos + ") &mdash; " + right;
        result_strings.push(result_string);
      }
    }
    if (result_strings.length === 0 || response.success === false) {
      if (opts.tooltip) {
        _tooltipTitle = 'Unknown word';
      }
    }
    if (opts.tooltip) {
      if (!_tooltipTitle) {
        _tooltipTitle = string;
      }
      _tooltipTarget = $(element).find('a.tooltip_target');
      _tooltipTarget.popover({
        title: _tooltipTitle,
        content: $("<p />").html(result_strings.join('<br />')).html(),
        html: true,
        placement: function() {
          if (_tooltipTarget[0].offsetLeft < 125) {
            return 'right';
          } else {
            return 'bottom';
          }
        },
        trigger: 'hover'
      });
      _tooltipTarget.popover('show');
      if (window.getSelection) {
        if (window.getSelection().empty) {
          return window.getSelection().empty();
        } else if (window.getSelection().removeAllRanges) {
          return window.getSelection().removeAllRanges();
        }
      } else if (document.selection) {
        return document.selection.empty();
      }
    }
  };
  lookupSelectEvent = function(evt, string, element, index, opts) {
    var langpair, lookup_string, post_data, result_elem, source_lang, target_lang,
      _this = this;
    result_elem = $(document).find(opts.formResults);
    string = $.trim(string).replace(/\b[-.,()&$#!\[\]{}"]+\B|\B[-.,()&$#!\[\]{}"]+\b/g, "");
    if ((string.length > 60) || (string.search(' ') > -1)) {
      return false;
    }
    if (string !== "") {
      langpair = $(opts.langPairSelect).val();
      source_lang = langpair.slice(0, 3);
      target_lang = langpair.slice(3, 6);
      lookup_string = string;
      post_data = {
        lookup: lookup_string,
        lemmatize: true
      };
      return $.ajax({
        url: "" + opts.api_host + "/kursadict/lookup/" + source_lang + "/" + target_lang + "/",
        data: post_data,
        success: function(response) {
          var selection;
          selection = {
            string: string,
            element: element,
            index: index
          };
          cleanTooltipResponse(selection, response, opts);
          if (document.selection) {
            console.log("document.selection!");
            return document.selection.empty();
          }
        }
      });
    }
  };
  $.fn.selectToLookup = function(opts) {
    var clean, holdingOption, previous_langpair, spinner, _opt, _select,
      _this = this;
    opts = $.extend({}, $.fn.selectToLookup.options, opts);
    spinner = initSpinner(opts.spinnerImg);
    if (opts.displayOptions) {
      $(document).find('body').append(Templates.OptionsTab(opts));
      window.optTab = $(document).find('#webdict_options');
    }
    previous_langpair = DSt.get('kursadict-select-langpair');
    if (previous_langpair) {
      _select = "input[type=\"radio\"][value=\"" + previous_langpair + "\"]";
      _opt = window.optTab.find(_select).attr('checked', 'checked');
    }
    holdingOption = function(evt, string, element, index) {
      if (evt.altKey) {
        lookupSelectEvent(evt, string, element, index, opts);
      }
      return false;
    };
    clean = function(event) {
      var parent, parents, _i, _len, _results;
      parents = [];
      $(document).find('a.tooltip_target').each(function() {
        parents.push($(this).parent());
        $(this).popover('destroy');
        return $(this).replaceWith(this.childNodes);
      });
      if (parents.length > 0) {
        _results = [];
        for (_i = 0, _len = parents.length; _i < _len; _i++) {
          parent = parents[_i];
          _results.push(parent.html(parent.html()));
        }
        return _results;
      }
    };
    $(document).bind('textselect', holdingOption);
    return $(document).bind('click', clean);
  };
  $.fn.selectToLookup.options = {
    api_host: API_HOST,
    formResults: "#results",
    spinnerImg: "dev/img/spinner.gif",
    sourceLanguage: "sme",
    langPairSelect: "#webdict_options *[name='language_pair']:checked",
    tooltip: true,
    displayOptions: true,
    dictionaries: [
      {
        from: {
          iso: 'sme',
          name: 'Nordsamisk'
        },
        to: {
          iso: 'nob',
          name: 'Norsk (bokmål)'
        }
      }, {
        from: {
          iso: 'nob',
          name: 'Norsk (bokmål)'
        },
        to: {
          iso: 'sme',
          name: 'Nordsamisk'
        }
      }, {
        from: {
          iso: 'sme',
          name: 'Nordsamisk'
        },
        to: {
          iso: 'fin',
          name: 'Finsk'
        }
      }
    ]
  };
  $.fn.kursaDict = function(opts) {
    opts = $.extend({}, $.fn.kursaDict.options, opts);
    return this.each(function() {
      var elem, previous_setting, result_elem,
        _this = this;
      elem = $(this);
      result_elem = $(this).find('#results');
      $(this).find('#langpairs li a').click(function(obj) {
        var new_val;
        new_val = $(obj.target).attr('data-value');
        elem.find('button span.val_name').html("" + (new_val.slice(0, 3)) + "->" + (new_val.slice(3, 6)));
        elem.find('input[name="target_lang"]').val(new_val);
        return DSt.set('kursadict-form-langpair', new_val);
      });
      previous_setting = DSt.get('kursadict-form-langpair');
      if (previous_setting) {
        elem.find('input[name="target_lang"]').val(previous_setting);
        elem.find('button span.val_name').html("" + (previous_setting.slice(0, 3)) + "->" + (previous_setting.slice(3, 6)));
      }
      elem.find('input[name="lookup"]').keydown(function(event) {
        if (event.keyCode === 13) {
          elem.submit();
          return false;
        }
        return true;
      });
      return elem.submit(function() {
        var cleanResponse, lang_pair, lookup_value, post_data, source_lang, target_lang, unknownWord;
        lookup_value = elem.find('input[name="lookup"]').val();
        lang_pair = $(_this).find('input[name="target_lang"]').val();
        source_lang = lang_pair.slice(0, 3);
        target_lang = lang_pair.slice(3, 6);
        post_data = {
          lookup: lookup_value
        };
        if (lookup_value.slice(-1) === '*') {
          post_data.type = 'startswith';
          post_data.lookup = post_data.lookup.replace('*', '');
        }
        unknownWord = function(response) {
          $(result_elem).append($("<p xml:lang=\"no\" class=\"alert\">Ukjent ord.</p>"));
          return false;
        };
        cleanResponse = function(response) {
          var lookup, result, result_list, _i, _len, _ref, _results;
          $(result_elem).html("");
          if (response.success === false) {
            unknownWord();
          } else if ((response.result.length === 1) && !response.result[0].lookups) {
            unknownWord();
          }
          _ref = response.result;
          _results = [];
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            result = _ref[_i];
            _results.push((function() {
              var _j, _len1, _ref1, _results1;
              _ref1 = result.lookups;
              _results1 = [];
              for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
                lookup = _ref1[_j];
                result_list = lookup.right.join(', ');
                _results1.push($(result_elem).append($("<p>" + lookup.left + " (" + lookup.pos + ") &mdash; " + result_list + "</p>")));
              }
              return _results1;
            })());
          }
          return _results;
        };
        $.ajax({
          url: "" + opts.api_host + "/kursadict/lookup/" + source_lang + "/" + target_lang + "/",
          data: post_data,
          success: cleanResponse
        });
        return false;
      });
    });
  };
  return $.fn.kursaDict.options = {
    api_host: API_HOST,
    formIDName: "#kursadict",
    formResults: "#results"
  };
});
