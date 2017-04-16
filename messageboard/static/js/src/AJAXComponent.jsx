import React, {Component} from 'react'

const DOMAIN = "http://localhost:8000";

class AJAXComponent extends Component {
  getPromise(path, config={}) {
    config = Object.assign({
      method: "POST",
      credentials: "include",
      headers: {"Content-Type": "application/json"},
    }, config);

    return fetch(DOMAIN + path, config);
  };
}
export default AJAXComponent