import React, {Component} from 'react'

import Channel from './Channel.jsx'

class ChannelList extends Component {
  render() {
    return (
      <div>
        <h3>Channels</h3>
        <ul>
          {this.props.channels.map((channel, idx) =>
            <li>
              <Channel name={channel.name} />
            </li>
          )}
        </ul>
      </div>
    )
  }
}
export default ChannelList