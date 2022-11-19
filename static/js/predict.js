$(document).ready(function () {
    function readURL(input) {
      if (input.files && input.files[0]) {
        var reader = new FileReader();
  
        reader.readAsDataURL(input.files[0]);
      }
    }
    // Inptut Field Name, you can change (change) method
    $("#inputFieldName").change(function () {
      readURL(this);

      var form_data = new FormData($("#formOfInputFieldName")[0]);

      $.ajax({
        type: "GET",
        url: "/predict",
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        async: true,
        success: function (data) {
          // TODO: On Sucess Function
        },
      });
    });
  });