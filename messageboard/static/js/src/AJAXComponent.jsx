import React, {Component} from 'react'

import config from 'config';


class AJAXComponent extends Component {
  getPromise(path, config={}) {
    config = Object.assign({
      method: "POST",
      credentials: "include",
      headers: {"Content-Type": "application/json"},
    }, config);

    return fetch(config.api_host + path, config);
  };
}
export default AJAXComponent