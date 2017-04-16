import React from 'react'

import AJAXComponent from './AJAXComponent.jsx'

class Likes extends AJAXComponent {
  constructor(props) {
    super(props);

    this.state = {
      userLikes: this.props.userLikes
    };
  }

  like(e) {
    e.preventDefault();
    this.getPromise('/api/v1/likes/', {
      body: JSON.stringify({topic_id: this.props.pk})
    }).then(response => {
      if (response.status === 201) {
        this.setState({userLikes: true});
      }
    });
  }

  unlike(e) {
    e.preventDefault();
    this.getPromise('/api/v1/likes/' + this.props.pk + '/', {
      method: "DELETE"
    }).then(response => {
      if(response.status === 204) {
        this.setState({userLikes: false});
      }
    })
  }

  render() {
    if(this.state.userLikes) {
      return (
        <span>
          {this.props.likesCount} people like this topic. You can <a onClick={this.unlike.bind(this)}>unlike</a> it if you want.
        </span>
      )
    } else {
      return (
        <span>{this.props.likesCount} people <a onClick={this.like.bind(this)}>like</a> this topic.</span>
      )
    }
  }
}
export default Likes