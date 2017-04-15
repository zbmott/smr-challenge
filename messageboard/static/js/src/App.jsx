import React, {Component} from 'react';
import Websocket from 'react-websocket';

import CurrentChannel from './CurrentChannel.jsx'
import NewTopic from './NewTopic.jsx'
import TopicList from './TopicList.jsx'
import Account from './Account.jsx'
import ChannelList from './ChannelList.jsx'

class App extends Component {
  constructor() {
    super();
    this.state = {
      "currentChannel": "/",
      "channelList": [],
      "topicList": [],
      "user": {
        "anonymous": true
      }
    };
  }

  handleData(data) {
    this.setState(Object.assign(this.state, JSON.parse(data)));
  }

  topicURL() {
    return "ws://localhost:8000/topics" + this.state.currentChannel;
  }

  render() {
    return (
      <div>
        <Websocket url={this.topicURL()} onMessage={this.handleData.bind(this)} />
        <Websocket url="ws://localhost:8000/_channellist" onMessage={this.handleData.bind(this)} />
        <article className="col-xs-8">
          <CurrentChannel name={this.state.currentChannel} />
          <NewTopic />
          <TopicList topics={this.state.topicList} />
        </article>
        <aside className="col-xs-4">
          <Account />
          <ChannelList channels={this.state.channelList} />
        </aside>
      </div>
    );
  }
}
export default App;
