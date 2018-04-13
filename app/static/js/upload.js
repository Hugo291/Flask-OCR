$(document).ready(function() {

	$('form').on('submit', function(event) {

		event.preventDefault();

		$("#submit-upload").prop("disabled",true);

        let formData = new FormData($('form')[0]);

        $.ajax({

			xhr : function() {

				var xhr = new window.XMLHttpRequest();

                xhr.upload.addEventListener('progress', function(e) {

					if (e.lengthComputable) {

                        var percent = Math.round((e.loaded / e.total) * 100);

                        $('#progressBar').attr('aria-valuenow', percent).css('width', percent + '%').text(percent + '%');

					}

				});

				return xhr;
			},
			type : 'POST',
			url : '/scan/upload',
			data : formData,
			processData : false,
			contentType : false,

			success : function(data) {
				alert(data);
				if(data.url !== undefined){
					console.log('redirect');
					window.location=data.url;
				} else  if(data.error !== undefined){
					console.log('error detected');
					alert(data.error);
				} else{
					alert('Données inconnues : '+data)
				}
			}

		});

	});

});




