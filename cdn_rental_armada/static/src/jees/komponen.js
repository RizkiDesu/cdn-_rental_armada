odoo.define('cdn_rental_armada.MyWidget', function (require) {
    "use strict";

    var AbstractField = require('web.AbstractField');
    var registry = require('web.field_registry');

    var MyWidget = AbstractField.extend({
        template: 'MyWidgetTemplate',
        events: {
            'click .my_button': '_onClick',
        },

        _onClick: function () {
            alert('Button clicked!');
        },
    });

    registry.add('my_widget', MyWidget);

    return MyWidget;
});
