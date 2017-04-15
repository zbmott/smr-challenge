import React, {Component} from 'react'

import Topic from './Topic.jsx'

class TopicList extends Component {
  render() {
    return (
      <div>
        <h3>TopicList</h3>
        <ul>
          {this.props.topics.map((topic, idx) =>
            <li>
              <Topic {...topic} />
            </li>
          )}
        </ul>
      </div>
    )
  }
}
export default TopicList