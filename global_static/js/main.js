
import { postRequest, HttpBadRequestError } from "./network.js";

$(document).ready(function() {
  const toast = new bootstrap.Toast($('#error-toast')[0], { autohide: true, delay: 3000 });
  const $form = $('#summary-form');

  $form.on('submit', async function(e) {
    const $messageEle = $('#message');
    const $submitBtnText = $('#submit-btn-text');
    const $submitBtnSpinner = $('#submit-btn-spinner');
    e.preventDefault();
    const formData = new FormData($form[0])
    $("#summary-form input, #summary-form button").prop("disabled", true);
    $submitBtnSpinner.show();
    $submitBtnText.text("");

    try {
      const response = await postRequest("/summary/", formData);
      window.location = response.success_url;
    } catch (error) {
      let message = "Something went wrong, please try again later.";
      if(error instanceof HttpBadRequestError) {
        message = error.data.message;
      }
      $messageEle.text(message);
      toast.show();
    } finally {
      $submitBtnText.text("Submit");
      $("#summary-form input, #summary-form button").prop("disabled", false);
      $submitBtnSpinner.hide();
    }
  });
});
