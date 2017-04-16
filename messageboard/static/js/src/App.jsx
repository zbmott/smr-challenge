import React, {Component} from 'react';
import Websocket from 'react-websocket';

import app_config from 'config';

import AJAXComponent from './AJAXComponent.jsx'
import CurrentChannel from './CurrentChannel.jsx'
import NewTopic from './NewTopic.jsx'
import TopicList from './TopicList.jsx'
import Account from './Account.jsx'
import ChannelList from './ChannelList.jsx'

class App extends AJAXComponent {
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

    this.getPromise("/whoami/", {method: "GET"}).then(response => {
      return response.json();
    }).then(json => {
      this.setState({user: json.user});
    });

  }

  handleData(data) {
    this.setState(JSON.parse(data));
  }

  topicURL() {
    return "ws://" + app_config.ws_host + "/topics/" + this.state.currentChannel;
  }

  channelURL() {
    return "ws://" + app_config.ws_host + "/_channellist";
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
        <Websocket url={this.channelURL()} onMessage={this.handleData.bind(this)} />
        <article className="col-xs-8">
          <CurrentChannel name={this.state.currentChannel} />
          <NewTopic key={this.state.currentChannel} user={this.state.user} currentChannel={this.state.currentChannel} />
          <TopicList key={this.state.user.anonymous} topics={this.state.topicList} user={this.state.user} />
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
