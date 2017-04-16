import React, {Component} from 'react'

import t from 'tcomb-form'


class NewTopic extends Component {
  schema = t.struct({
    channel: t.String,
    title: t.String,
    content: t.String
  });

  options = {
    fields: {
      content: {
        type: "textarea"
      }
    }
  };

  constructor(props) {
    super(props);
    this.state = {
      message: "",
      messageClassName: "",
      defaultValue: {
        channel: props.currentChannel
      }
    };
  }

  onSubmit(e) {
    e.preventDefault();
    let form = this.refs.form.getValue();
    fetch("http://localhost:8000/api/v1/topics/", {
      method: "POST",
      credentials: "include",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        title: form.title,
        content: form.content,
        channel: {
          name: form.channel
        }
      })
    }).then(response => {
      return response.json();
    }).then(json => {
    });
  }

  render() {
    if(this.props.user.anonymous === false) {
      return (
        <div>
          <form onSubmit={this.onSubmit.bind(this)}>
            <t.form.Form ref="form" type={this.schema} options={this.options} value={this.state.defaultValue}/>
            <div className={this.state.messageClassName}>
              <span>{this.state.message}</span>
            </div>
            <button className="btn btn-primary">Post</button>
          </form>
        </div>
      )
    } else {
      return null;
    }
  }
}
export default NewTopic