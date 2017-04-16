import React, {Component} from 'react'

import {markdown} from 'markdown'


class TopicContent extends Component {
  getHTML() {
    return {__html: markdown.toHTML(this.props.content)}
  }

  // dangerouslySetInnerHTML is safe in this instance because
  // the server strips all HTML before the Topic is saved.
  render() {
    return (
      <p dangerouslySetInnerHTML={this.getHTML()} />
    )
  }
}
export default TopicContent