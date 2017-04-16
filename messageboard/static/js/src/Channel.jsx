import React, {Component} from 'react'

class Channel extends Component {

  updateChannel(e) {
    e.preventDefault();
    this.props.updateAppChannel(this.props.name);
  }

  render() {
    return (
      <a onClick={this.updateChannel.bind(this)}>
        {this.props.name}
      </a>
    )
  }
}
export default Channel