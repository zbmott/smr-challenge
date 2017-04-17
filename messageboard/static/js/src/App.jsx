import React, {Component} from 'react';
import Websocket from 'react-websocket';

import {Route, HashRouter} from 'react-router-dom';

import app_config from 'config';

import AJAXComponent from './AJAXComponent.jsx'
import CurrentChannel from './CurrentChannel.jsx'
import NewTopic from './NewTopic.jsx'
import TopicList from './TopicList.jsx'
import Account from './Account.jsx'
import ChannelList from './ChannelList.jsx'

class MessageBoard extends AJAXComponent {
  constructor(props) {
    super(props);

    this.state = {
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

  updateUser(user) {
    this.setState({user: user});
  }

  render() {
    return (
      <div>
        <article className="col-xs-8">
          <CurrentChannel name={this.props.currentChannel} />
          <NewTopic key={this.props.currentChannel} user={this.state.user}
                    currentChannel={this.props.currentChannel} />
          <TopicList key={this.state.user.anonymous}
                     topicList={this.props.topicList} user={this.state.user} />
        </article>
        <aside className="col-xs-4">
          <Account user={this.state.user} updateUser={this.updateUser.bind(this)}/>
          <ChannelList channelList={this.props.channelList} />
        </aside>
      </div>
    );
  }
}

class MessageBoardContainer extends Component {
  constructor(props) {
    super(props);
    this.channelURL = "ws://" + app_config.ws_host + "/_channellist";
    this.state = {
      channelList: [],
      topicList: []
    };
  }

  handleData(data) {
    this.setState(JSON.parse(data));
  }

  topicURL(currentChannel) {
    return "ws://" + app_config.ws_host + "/topics/" + currentChannel;
  }

  render() {
    let currentChannel = this.props.match.params.channelName;

    if(!currentChannel) {
      currentChannel = 'home';
    }

    return (
      <div className="messageboard">
        <MessageBoard currentChannel={currentChannel}
                      channelList={this.state.channelList} topicList={this.state.topicList}/>
        <Websocket key={currentChannel}
                   url={this.topicURL(currentChannel)} onMessage={this.handleData.bind(this)} />
        <Websocket url={this.channelURL} onMessage={this.handleData.bind(this)} />
      </div>
    )
  }
}

class App extends Component {
  render() {
    return (
      <HashRouter>
        <div>
          <Route exact path="/" component={MessageBoardContainer} />
          <Route path="/:channelName" component={MessageBoardContainer} />
        </div>
      </HashRouter>
    )
  }
}

export default App;
