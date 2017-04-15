import React, {Component} from 'react'

class Channel extends Component {
  render() {
    return (
      <a href={this.props.name}>{this.props.name}</a>
    )
  }
}
export default Channel