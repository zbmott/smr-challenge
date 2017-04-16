import React, {Component} from 'react';

class CurrentChannel extends Component {
  render() {
    return (
      <h1 className="current-channel">{this.props.name}</h1>
    )
  }
}
export default CurrentChannel
