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
        console.log($(this).attr("action"))
        console.log($(this).serializeArray())
        var formData = objectifyForm($(this).serializeArray());
        rpc.query({
            model: 'res.users',
            method: 'create_user',
            args: [formData],
        }).then(function (data) {
            $('#confirmModal').modal('show')
        })
    })

    $('#users a.deactivate').on('click', function () {
        deactivate_id = $(this).attr('id');
        $('#confirmDeactivationModal').modal('show');
    })

    $('#confirmDeactivation').on('click', function () {
        rpc.query({
            model: 'res.users',
            method: 'deactivate_user',
            args: [deactivate_id],
        }).then(function (data) {
            location.reload();
        })
    })

});