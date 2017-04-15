import React, {Component} from 'react'

import t from 'tcomb-form'


class NewTopic extends Component {
  schema = t.struct({
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
      messageClassName: ""
    };
  }

  onSubmit(e) {
    e.preventDefault();
    let form = this.refs.form.getValue();
  }

  render() {
    if(this.props.user.anonymous === false) {
      return (
        <div>
          <form onSubmit={this.onSubmit.bind(this)}>
            <t.form.Form ref="form" type={this.schema} options={this.options} />
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