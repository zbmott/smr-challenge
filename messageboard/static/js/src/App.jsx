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
      "currentChannel": "home",
      "channelList": [],
      "topicList": [],
      "user": {
        "anonymous": true
      }
    };

    fetch('http://localhost:8000/whoami/', {credentials: 'include'}).then(response => {
      return response.json();
    }).then(json => {
      this.setState({user: json.user});
    });

  }

  handleData(data) {
    this.setState(Object.assign(this.state, JSON.parse(data)));
  }

  topicURL() {
    return "ws://localhost:8000/topics/" + this.state.currentChannel;
  }

  updateUser(user) {
    this.setState({user: user});
  }

  updateChannel(channel) {
    this.setState({currentChannel: channel});
  }

  render() {
    return (
      <div>
        <Websocket key={this.state.currentChannel} url={this.topicURL()} onMessage={this.handleData.bind(this)} />
        <Websocket url="ws://localhost:8000/_channellist" onMessage={this.handleData.bind(this)} />
        <article className="col-xs-8">
          <CurrentChannel name={this.state.currentChannel} />
          <NewTopic key={this.state.currentChannel} user={this.state.user} currentChannel={this.state.currentChannel} />
          <TopicList topics={this.state.topicList} />
        </article>
        <aside className="col-xs-4">
          <Account user={this.state.user} updateUser={this.updateUser.bind(this)}/>
          <ChannelList channels={this.state.channelList} updateChannel={this.updateChannel.bind(this)} />
        </aside>
      </div>
    );
  }
}
export default App;
