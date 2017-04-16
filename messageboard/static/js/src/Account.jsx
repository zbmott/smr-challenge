import React, {Component} from 'react'

import t from 'tcomb-form'


class SignInForm extends Component {
  schema = t.struct({
    username: t.String,
    password: t.String
  });

  options = {
    fields: {
      password: {type: 'password'}
    }
  };

  constructor(props) {
    super(props);
    this.state = {
      message: "",
      messageClassName: ""
    }
  }

  onSubmit(e) {
    e.preventDefault();
    let form = this.refs.form.getValue();
    fetch("http://localhost:8000/login/", {
      method: "POST",
      credentials: "include",
      body: JSON.stringify({"username": form.username, "password": form.password})
    }).then(response => {
      return response.json();
    }).then(json => {
      if(parseInt(json.status) === 200) {
        this.props.updateUser(json.user);
      } else if(parseInt(json.status) === 403) {
        this.setState({
          message: "The credentials you provided are invalid.",
          messageClassName: "form-feedback error"
        })
      }
    });
  }

  render() {
    return (
      <div>
        <form onSubmit={this.onSubmit.bind(this)}>
          <t.form.Form ref="form" type={this.schema} options={this.options}/>
          <div className={this.state.messageClassName}>
            <span>{this.state.message}</span>
          </div>
          <button className="btn btn-primary">Sign in</button>
        </form>
      </div>
    )
  }
}

class SignUpFormButtons extends Component {
  render() {
    if(this.props.status === 200) {
      return (
        <button className="btn btn-primary" onClick={this.props.toggleDialog}>I like logging in</button>
      )
    } else {
      return (
        <span>
          <button className="btn btn-primary">Create account</button> or <a onClick={this.props.toggleDialog}>don't create an account</a>
        </span>
      )
    }
  }
}

class SignUpForm extends Component {
  schema = t.struct({
    username: t.String,
    email: t.String,
    password: t.String,
    confirm_password: t.String
  });

  options = {
    fields: {
      password: {type: 'password'},
      confirm_password: {type: 'password'}
    }
  };

  constructor(props) {
    super(props);
    this.state = {
      requestStatus: undefined,
      message: "",
      messageClassName: ""
    };
  }

  onSubmit(e) {
    e.preventDefault();
    this.setState({requestStatus: undefined});
    let form = this.refs.form.getValue();
    fetch('http://localhost:8000/create-account/', {
      method: 'POST',
      credentials: 'include',
      body: JSON.stringify({
        'username': form.username,
        'email': form.email,
        'password': form.password,
        'confirm': form.confirm_password
      })
    }).then(response => {
      return response.json();
    }).then(json => {
      const status = parseInt(json.status);
      if(status === 200) {
        this.setState({
          "requestStatus": status,
          "message": "Your account was successfully created. You may now log in.",
          "messageClassName": "form-feedback success"
        });
      } else if(status === 400) {
        //TODO: Display errors.
      }
    });
  }

  render() {
    return (
      <div id="create-user-account">
        <h4>Create a user account</h4>
        <form onSubmit={this.onSubmit.bind(this)}>
          <t.form.Form ref="form" type={this.schema} options={this.options}/>
          <div className={this.state.messageClassName}>
            <span>{this.state.message}</span>
          </div>
          <SignUpFormButtons status={this.state.requestStatus} toggleDialog={this.props.toggleDialog}/>
        </form>
      </div>
    )
  }
}

class Account extends Component {
  constructor(props) {
    super(props);
    this.state = {
      "showSignUpForm": false
    };
  }

  toggleSignUpForm(e) {
    e.preventDefault();
    this.setState({"showSignUpForm": !this.state['showSignUpForm']})
  }

  userIsAnonymous() {
    return this.props.user.anonymous;
  }

  logout() {
    fetch('http://localhost:8000/logout/', {credentials: 'include'}).then(response => {
      return response.json();
    }).then(json => {
      this.props.updateUser(json.user);
    });
  }

  render() {
    if(this.userIsAnonymous()) {
      return (
        <div className="account">
          <SignInForm updateUser={this.props.updateUser} />
          <span>or <a onClick={this.toggleSignUpForm.bind(this)}>create an account</a></span>
          {this.state.showSignUpForm ? <SignUpForm toggleDialog={this.toggleSignUpForm.bind(this)}/> : null}
        </div>
      )
    } else {
      return (
        <div className="account">
          <span>Welcome, {this.props.user.username}</span><br />
          <a onClick={this.logout.bind(this)}>Logout</a>
        </div>
      )
    }
  }
}
export default Account