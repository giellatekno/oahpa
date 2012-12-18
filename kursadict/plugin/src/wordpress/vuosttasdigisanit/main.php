<?php
/*
Plugin Name: Vuosttaš Digisánit
Plugin URI: http://giellatekno.uit.no
Description: A plugin for providing access to dictionaries via clicking.
Version: 0.0.1
Author: Ryan Johnson / Giellatekno
Author URI: http://giellatekno.uit.no/
License: GPL2
*/

function load_dict_css () {
    wp_enqueue_style( 'my_style'
                    , plugins_url('/jquery.kursadict.css', __FILE__)
                    );
}

function load_dict_scripts () {
    // NOTE: probably already available wp_enqueue_script('jquery');

    wp_enqueue_script( 'gt-ns-jquery'
                     , plugins_url('/jquery.kursadict.js', __FILE__)
                     , array('jquery')
                     , '1.7.2'
                     ) ;

    wp_enqueue_script( 'gt-ns-main'
                     , plugins_url('/main.js', __FILE__)
                     , array('jquery', 'gt-ns-jquery')
                     ) ;

}


/*
 *  error_reporting(E_ALL);
 *  class NS_SearchForm {
 *    function control(){
 *      echo 'I am a control panel';
 *    }
 *    function widget($args){
 *      $snippet = fopen("search_form_snippet.html", "r");
 *      echo $args['before_widget'];
 *      echo $args['before_title'] . 'Vuosttaš Neahttasánit' . $args['after_title'];
 *      echo $snippet;
 *      echo $args['after_widget'];
 *    }
 *    function register(){
 *      register_sidebar_widget('Vuosttaš Neahttasánit', array('Widget_name', 'widget'));
 *      register_widget_control('Vuosttaš Neahttasánit', array('Widget_name', 'control'));
 *    }
 *  }
 */

function vn_init() {
    add_action("widgets_init", array('Widget_name', 'register'));

    if (!is_admin()) {
        load_dict_css();
        load_dict_scripts();
    }
}

add_action('init', 'vn_init');

?>
