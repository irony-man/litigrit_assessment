
import { postRequest, HttpBadRequestError, HttpServerError } from "./network.js";

$(document).ready(function() {
  const toast = new bootstrap.Toast($('#errorToast')[0], { autohide: true, delay: 3000 });
  if($('#history').length) {
    $ ('html, body') .animate ({
      scrollTop: $ ("#history") .offset().top + $("#history")[0].scrollHeight
    }, 0);
  }

  const $form = $('#summaryForm');

  // Makes api call as opposed to default form POST, we can use default but I just wanted to showcase my skill

  $form.on('submit', async function(e) {
    const $submitBtnText = $('#submitBtnText');
    const $submitBtnSpinner = $('#submitBtnSpinner');
    const $attachmentError = $('#attachmentError');
    const $summaryLengthError = $('#summaryLengthError');
    e.preventDefault();
    const formData = new FormData($form[0])
    $("#summaryForm input, #summaryForm select, #summaryForm button").prop("disabled", true);
    $submitBtnSpinner.show();
    $submitBtnText.text("Loading");
    $attachmentError.hide();
    $summaryLengthError.hide();

    try {
      const response = await postRequest("/summary/", formData);
      window.location = `/summary/${response.uid}`;
    } catch (error) {
      let message = "";
      if(error instanceof HttpBadRequestError) {
        const errors = error.data;
        if(errors?.attachment) {
          $attachmentError.text(errors?.attachment?.join(' '));
          $attachmentError.show();
        }
        if(errors?.summary_length) {
          $summaryLengthError.text(errors?.summary_length?.join(' '));
          $summaryLengthError.show();
        }
        if(errors?.non_field_errors || errors?.detail) {
          message = errors.non_field_errors || errors?.detail;
        }
      } else if (error instanceof HttpServerError) {
        message = error
      }
      if(message) {
        $('#message').text(message);
        toast.show();
      }
    } finally {
      $submitBtnText.text("Submit");
      $("#summaryForm input, #summaryForm select, #summaryForm button").prop("disabled", false);
      $submitBtnSpinner.hide();
    }
  });
});
