import React, {Component} from 'react'

import Channel from './Channel.jsx'

class ChannelList extends Component {
  render() {
    return (
      <div>
        <h3>Channels</h3>
        <ul>
          {this.props.channels.map((topic, idx) =>
            <li>
              <Channel name={topic.name} />
            </li>
          )}
        </ul>
      </div>
    )
  }
}
export default ChannelList