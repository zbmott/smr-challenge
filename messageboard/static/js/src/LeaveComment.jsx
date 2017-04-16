import React, {Component} from 'react'
import t from 'tcomb-form'

import AJAXComponent from './AJAXComponent.jsx'

class LeaveComment extends AJAXComponent {
  schema = t.struct({
    title: t.String,
    content: t.String
  });

  options = {
    fields: {
      content: {
        type: "textarea",
        help: "Markdown is supported. HTML is not."
      }
    }
  };

  constructor(props) {
    super(props);
    this.state = {
      formVisible: false,
      defaultValue: {
        title: "Re: " + props.title
      }
    };
  }

  toggleFormVisible(e) {
    if(e) {
      e.preventDefault();
    }
    this.setState({formVisible: !this.state.formVisible});
  }

  onSubmit(e) {
    e.preventDefault();
    let form = this.refs.form.getValue();
    this.getPromise("/api/v1/topics/", {
      body: JSON.stringify({
        title: form.title,
        content: form.content,
        channel: this.props.channel,
        parent: this.props.parent_pk
      })
    }).then(request => {
      if(request.status === 201) {
        this.toggleFormVisible();
      }
    })
  }

  render() {
    if(this.state.formVisible) {
      return (
        <div className="leave-comment">
          <a onClick={this.toggleFormVisible.bind(this)}>Never mind about that comment.</a>
          <form onSubmit={this.onSubmit.bind(this)}>
            <t.form.Form ref="form" type={this.schema} options={this.options} value={this.state.defaultValue} />
            <button className="btn btn-primary">Post</button>
          </form>
        </div>
      )
    } else {
      return (
        <div className="leave-comment">
          <a onClick={this.toggleFormVisible.bind(this)}>Leave a comment!</a>
        </div>
      )
    }
  }
}
export default LeaveComment