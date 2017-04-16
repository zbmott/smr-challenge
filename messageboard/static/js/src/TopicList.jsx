import React, {Component} from 'react'

import Topic from './Topic.jsx'

class TopicList extends Component {
  isLiked(key) {
    if(this.props.user.likedPosts !== undefined) {
      return this.props.user.likedPosts.includes(parseInt(key))
    } else {
      return false;
    }
  }

  render() {
    return (
      <div>
        {this.props.topics.map((topic, idx) =>
          <Topic key={topic.key} userLikes={this.isLiked(topic.pk)} {...topic} />
        )}
      </div>
    )
  }
}
export default TopicList