import React, {Component} from 'react'

import TopicList from './TopicList.jsx'
import TopicContent from './TopicContent.jsx'
import TopicControls from './TopicControls.jsx'

class Topic extends Component {
  render() {
    return (
      <div className="topic">
        <h4 className="topic-title">
          {this.props.title} / {this.props.created} / {this.props.created_by}
        </h4>
        <TopicContent content={this.props.content} />
        <TopicControls key={this.props.pk} pk={this.props.pk}
                       likesCount={this.props.likes} user={this.props.user}
                       userLikes={this.props.userLikes} title={this.props.title}
                       channel={this.props.channel} />
        <div className="topic-comments">
          <TopicList key={this.props.user.anonymous} topics={this.props.children} user={this.props.user} />
        </div>
      </div>
    )
  }
}
export default Topic