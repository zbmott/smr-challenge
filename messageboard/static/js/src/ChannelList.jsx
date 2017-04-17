import React, {Component} from 'react'

import Channel from './Channel.jsx'

class ChannelList extends Component {
  render() {
    return (
      <div>
        <h3>Channels</h3>
        <ul>
          {this.props.channelList.map((channel, idx) =>
            <li key={channel.key}>
              <Channel {...channel} />
            </li>
          )}
        </ul>
      </div>
    )
  }
}
export default ChannelList