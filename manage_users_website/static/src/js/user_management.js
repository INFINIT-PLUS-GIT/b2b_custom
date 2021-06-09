odoo.define('manage_users_website.user_management', ['web.rpc'], function (require) {
    "use strict";

    var rpc = require('web.rpc');
    var deactivate_id;

    function objectifyForm(formArray) {
        var returnArray = {};
        for (var i = 0; i < formArray.length; i++) {
            returnArray[formArray[i]['name']] = formArray[i]['value'];
        }
        return returnArray;
    }

    $('#createUserForm').on('submit', function (e) {
        e.preventDefault();
        $('#loader').modal({
            show: true,
            keyboard: false,
            backdrop: 'static'
        })
        var formData = objectifyForm($(this).serializeArray());
        rpc.query({
            model: 'res.users',
            method: 'create_business_user',
            args: [formData],
        }).then(function (data) {
            $("#loader").removeClass("in");
            $(".modal-backdrop").remove();
            $('#loader').modal('hide')
            $('#confirmModal').modal('show')
            if (data.status === 'not-allowed') $('#modal-message').text("You don't have permission to this action")
        })
    })

    $('#users input[type=checkbox]').change(function () {
        deactivate_id = parseInt($(this).parent().attr('id'));
        $('#loader').modal({
            show: true,
            keyboard: false,
            backdrop: 'static'
        })
        var status = rpc.query({
            model: 'res.users',
            method: 'toggle_user_active',
            args: [deactivate_id],
        });

        status.then(function (data) {
            $("#loader").removeClass("in");
            $(".modal-backdrop").remove();
            $('#loader').modal('hide')
        });
    })

});