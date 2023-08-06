jQuery(function ($) {

  function split( val ) {
    return val.split( /[;,\s]+/ );
  };

  autocomplete_fields.forEach( function (field) {
    $(field).autocomplete({
      source: subjects_href,
      select: function (event, ui) {
        $( this ).val( ui.item[0] );
        return false;
      }
    });
  });

  autocomplete_fields_multi.forEach( function (field) {
    $(field)
      .on( 'keydown', function( event ) {
        if ( event.keyCode === $.ui.keyCode.TAB &&
            $( this ).autocomplete( 'instance' ).menu.active ) {
          event.preventDefault();
        }
      })
      .autocomplete({
        source: subjects_href,
        delay: 100,
        focus : function () {
          return false;  // prevent value inserted on focus
        },
        select: function (event, ui) {
          var items = split( this.value );
          items.pop();  // remove current input
          items.push( ui.item[0] );  // add selected item
          items.push( "" );  // add placeholder to get separator at end
          this.value = items.join( " " );
          return false;
        }
      });
  });

  $('.ui-autocomplete-input').each(function() {
    $(this).data('ui-autocomplete')._renderItem = function (ul, item) {
      var name = item[1] ? item[1] : item[0];
      var email = item[2] ? ("<" + item[2] + ">") : "";
      return $('<li>')
        .data('ui-autocomplete-item', item[0])
        .append($.htmlFormat('$1 $2', name, email))
        .appendTo(ul);
    }
  });
});
