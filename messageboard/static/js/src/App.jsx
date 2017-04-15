import React, {Component} from 'react';

import CurrentChannel from './CurrentChannel.jsx'
import NewTopic from './NewTopic.jsx'
import TopicList from './TopicList.jsx'
import Account from './Account.jsx'
import ChannelList from './ChannelList.jsx'

class App extends Component {
  constructor() {
    super();
    this.state = {};
  }

  render() {
    return (
      <div>
        <article className="col-xs-8">
          <CurrentChannel />
          <NewTopic />
          <TopicList />
        </article>
        <aside className="col-xs-4">
          <Account />
          <ChannelList />
        </aside>
      </div>
    );
  }
}
export default App;
