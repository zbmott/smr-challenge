import React, {Component} from 'react'

import Likes from './Likes.jsx'
import TopicContent from './TopicContent.jsx'

class Topic extends Component {
  render() {
    return (
      <div>
        <h4>{this.props.title} / {this.props.created} / {this.props.created_by}</h4>
        <TopicContent content={this.props.content} />
        <Likes key={this.props.pk} pk={this.props.pk} likesCount={this.props.likes}
               anonymousUser={this.props.anonymousUser} userLikes={this.props.userLikes} />
      </div>
    )
  }
}
export default Topic