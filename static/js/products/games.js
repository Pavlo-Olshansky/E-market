$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-game").modal("show");
      },
      success: function (data) {
        $("#modal-game .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#game-table tbody").html(data.html_game_list);
          $("#modal-game").modal("hide");
        }
        else {
          $("#modal-game .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create game
  $(".js-create-game").click(loadForm);
  $("#modal-game").on("submit", ".js-game-create-form", saveForm);

  // Update game
  $("#game-table").on("click", ".js-update-game", loadForm);
  $("#modal-game").on("submit", ".js-game-update-form", saveForm);

  // Delete game
  $("#game-table").on("click", ".js-delete-game", loadForm);
  $("#modal-game").on("submit", ".js-game-delete-form", saveForm);

});