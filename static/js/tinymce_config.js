tinymce.init({
    selector: 'textarea',
    plugins: 'image link media code',
    toolbar: 'undo redo | styles | bold italic | alignleft aligncenter alignright alignjustify | outdent indent | link image media | code',
    image_title: true,
    automatic_uploads: true,
    images_upload_url: '/upload_image/',
    file_picker_types: 'image',
    file_picker_callback: function (cb, value, meta) {
      var input = document.createElement('input');
      input.setAttribute('type', 'file');
      input.setAttribute('accept', 'image/*');
      input.onchange = function () {
        var file = this.files[0];
        var reader = new FileReader();
        reader.onload = function () {
          cb(reader.result, {
            title: file.name
          });
        };
        reader.readAsDataURL(file);
      };
      input.click();
    }
  });
  