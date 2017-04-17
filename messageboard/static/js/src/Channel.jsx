import React, {Component} from 'react'

import {Link} from 'react-router-dom'

class Channel extends Component {

  getTo() {
    return "/" + this.props.name + "/";
  }

  render() {
    return (
      <Link to={this.getTo()}>
        {this.props.name}
      </Link>
    )
  }
}
export default Channel