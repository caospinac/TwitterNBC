import React, { Component } from 'react'
import { FormGroup, Button, Input } from 'reactstrap';

export default class InputForm extends Component {

    constructor(props) {
        super(props);
        this.state = {
            text: ""
        }

        this.onChangeText = this.onChangeText.bind(this);
        this.onKeyUp = this.onKeyUp.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
    }

    onChangeText(e) {
        this.setState({
            text: e.target.value
        });
    }

    onKeyUp(e) {
        if (e.ctrlKey && e.keyCode === 13) {
            this.onSubmit();
        }
    }

    onSubmit() {
        if (!this.state.text) {
            return;
        }
        const { onSubmit } = this.props;
        onSubmit && onSubmit(this.state);
        this.setState({
            text: ""
        });
    }

    render() {
        const { text } = this.state;
        const { disabled } = this.props;
        return (
            <div>
                <FormGroup>
                    <Input value={text} type="textarea" required={true} onKeyUp={this.onKeyUp}
                            readOnly={disabled} onChange={this.onChangeText} placeholder="Text" />
                </FormGroup>
                <FormGroup>
                    <div className="pull-right">
                        <small className="light-text" style={{marginRight: "5px"}}>
                            <i className="">Ctrl + Enter to submit</i>
                        </small>
                        <Button onClick={this.onSubmit} disabled={disabled}>Analyze</Button>
                    </div>
                </FormGroup>
            </div>
        )
    }
}
