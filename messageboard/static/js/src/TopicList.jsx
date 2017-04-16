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
    return (
      <div>
        {this.props.topics.map((topic, idx) =>
          <Topic key={topic.key} userLikes={this.isLiked(topic.pk)}
                 anonymousUser={this.props.user.anonymous} {...topic} />
        )}
      </div>
    )
  }
}
export default TopicList