function getCsrfToken() {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    let cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      if (cookie.substring(0, 10) === "csrftoken=") {
        cookieValue = decodeURIComponent(cookie.substring(10));
        break;
      }
    }
  }
  return cookieValue;
}

class BaseHttpError extends Error {
  constructor(message, data, statusCode) {
    super(message);
    this.data = data;
    this.statusCode = statusCode;
    this.name = this.constructor.name;
    this.message = message;
    if (typeof Error.captureStackTrace === "function") {
      Error.captureStackTrace(this, this.constructor);
    } else {
      this.stack = new Error(message).stack;
    }
  }
}

class HttpBadRequestError extends BaseHttpError {}

class HttpNotFound extends BaseHttpError {}

class HttpServerError extends BaseHttpError {}


async function execute(url, options) {
  let data;
  let response;
  const msg = "Error in processing request. Try later or contact support";

  try {
    response = await fetch(url, options);
    if (options.method !== "delete" && response.status !== 204) {
      const content = response.headers.get("Content-Type");
      if (content === "application/json") {
        data = await response.json();
        // data['statusCode'] = response?.status
      } else {
        data = response.text();
      }
    }
  } catch (e) {
    alert(msg);
  }

  if (response) {
    if (response.status === 400) {
      throw new HttpBadRequestError("Http 400 [BadRequest]", data, response.status);
    } else if (response.status === 404) {
      throw new HttpNotFound("Http 404 [Not found]", data, response.status);
    } else if (response?.status >= 500) {
      if(data.detail) {
        throw new HttpServerError(data.detail);
      }
      throw new HttpServerError(
       'Server Error: please contact support.'
      );
    }
    return data;
  }
}

const formDataRequest = async (method, url, formData = null) => {
  const options = {
    method: method,
    credentials: "same-origin",
    headers: {
      Accept: "application/json",
      "X-CSRFToken": getCsrfToken(window.location.href),
      "X-Requested-With": "XMLHttpRequest",
    },
  };

  const isFormData = formData instanceof FormData;
  if (isFormData) {
    options.body = formData;
  } else {
    // JSON request
    options.body = JSON.stringify(formData);
    options.headers["Content-Type"] = "application/json";
  }

  return await execute(url, options);
};

const postRequest = async (url, formData = null) => {
  return await formDataRequest("POST", url, formData);
};

const patchRequest = async (url, formData = null) => {
  return await formDataRequest("PATCH", url, formData);
};

const deleteRequest = async (url) => {
  return await formDataRequest("DELETE", url, null);
};

const getRequest = async (url, queryParams = null) => {
  const options = {
    method: "GET",
    credentials: "same-origin",
    headers: {
      Accept: "application/json",
    },
  };

  let reqUrl = url;
  let paramsObj = queryParams;

  if (queryParams) {
    const isSearchParam = queryParams instanceof URLSearchParams;
    if (!isSearchParam) {
      paramsObj = new URLSearchParams();
      Object.keys(queryParams).forEach((key) => {
        paramsObj.append(key, queryParams[key]);
      });
    }
    reqUrl = `${url}?${paramsObj.toString()}`;
  }

  return await execute(reqUrl, options);
};

export { getRequest, postRequest, patchRequest, deleteRequest, HttpBadRequestError, HttpNotFound, HttpServerError };
