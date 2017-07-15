$(function () {

  $(".js_login_signup_up").click(function () {
    $.ajax({
      url: '/accounts/login_user/',
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-book").modal("show");
      },
      success: function (data) {
        $("#modal-book .modal-content").html(data.html_form);
      }
    });
  });

  $("#modal-book").on("submit", ".js-user-create-form", function () {
    $('#loader').show();

    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#modal-book").modal("hide");
          $("#loading").hide();
          if (!data.loginned) {
          alert("Now confirm your account at the email!");  // <-- This is just a placeholder for now for testing
          }
          else{
            location.reload();
          }
        }
        else {
          $("#loading").hide();
          $("#modal-book .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  });

});