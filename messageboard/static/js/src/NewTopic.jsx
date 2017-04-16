import React from 'react'
import t from 'tcomb-form'

import AJAXComponent from './AJAXComponent.jsx'


class NewTopic extends AJAXComponent {
  schema = t.struct({
    channel: t.String,
    title: t.String,
    content: t.String
  });

  options = {
    fields: {
      channel: {
        help: "Valid characters are limited to alphanumerics, " +
              "underscores, and hyphens. Invalid characters will be removed."
      },
      content: {
        type: "textarea",
        help: "Markdown is supported. HTML is not."
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
        <div className="new-topic">
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