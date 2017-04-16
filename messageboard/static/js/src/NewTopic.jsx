import React from 'react'

import AJAXComponent from './AJAXComponent.jsx'

import t from 'tcomb-form'


class NewTopic extends AJAXComponent {
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
    this.getPromise("/api/v1/topics/", {
      body: JSON.stringify({
        title: form.title,
        content: form.content,
        channel: {
          name: form.channel
        }
      })
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