import React, {Component} from 'react'

import Topic from './Topic.jsx'

class TopicList extends Component {
  isLiked(key) {
    // Determine if any particular topic in this list is
    // liked by the current user. This is information we
    // need to pass to the Like component deeper in the tree.
    if(this.props.user.likedPosts !== undefined) {
      return this.props.user.likedPosts.includes(parseInt(key))
    } else {
      return false;
    }
  }

  render() {
    if(this.props.topics.length > 0) {
      return (
        <div className="topic-list">
          {this.props.topics.map((topic, idx) =>
              <Topic key={topic.pk} user={this.props.user}
                     userLikes={this.isLiked(topic.pk)} {...topic} />
          )}
        </div>
      )
    } else {
      return null;
    }
  }
}
export default TopicList