import React, {Component} from 'react'

import app_config from 'config';


class AJAXComponent extends Component {
  getPromise(path, promise_config={}) {
    promise_config = Object.assign({
      method: "POST",
      credentials: "include",
      headers: {"Content-Type": "application/json"},
    }, promise_config);

    return fetch('http://' + app_config.api_host + path, promise_config);
  };
}
export default AJAXComponent